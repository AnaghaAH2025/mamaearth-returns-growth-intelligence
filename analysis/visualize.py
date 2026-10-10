"""Regenerate required figures directly from the raw CSV files."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "visualizations"
OUT.mkdir(parents=True, exist_ok=True)

orders = pd.read_csv(DATA / "orders.csv")
products = pd.read_csv(DATA / "products.csv")
customers = pd.read_csv(DATA / "customers.csv")
natural_key = ["customer_id", "product_id", "order_date", "quantity", "discount_pct", "payment_method", "rating", "returned"]
orders = orders.drop_duplicates(subset=natural_key, keep="first").copy()
orders["payment_method"] = orders["payment_method"].astype(str).str.strip().str.upper()
orders["discount_pct"] = orders["discount_pct"].fillna(0)
orders["rating"] = orders["rating"].fillna(orders["rating"].median())
merged = orders.merge(products, on="product_id", how="left").merge(customers[["customer_id", "city_tier"]], on="customer_id", how="left")
merged["order_value"] = merged["quantity"] * merged["price"] * (1 - merged["discount_pct"] / 100)
merged["is_outlier"] = (merged["quantity"] < -0.5) | (merged["quantity"] > 3.5)

rates = (merged.groupby("payment_method")["returned"].mean() * 100).sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(rates.index, rates.values)
ax.set_ylabel("Return rate (%)")
ax.set_xlabel("Payment method")
ax.set_title(f"COD Returns at {rates.loc['COD']:.1f}% — {rates.loc['COD']/rates.loc['CARD']:.1f}x Card")
ax.set_ylim(0, max(rates.values) * 1.22)
for bar, value in zip(bars, rates.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8, f"{value:.1f}%", ha="center", va="bottom")
fig.tight_layout()
fig.savefig(OUT / "return_rate_by_payment.png", dpi=160, bbox_inches="tight")
plt.close(fig)

merged["order_date"] = pd.to_datetime(merged["order_date"])
merged["year_month"] = merged["order_date"].dt.to_period("M").astype(str)
monthly = merged.loc[~merged["is_outlier"]].groupby("year_month")["order_value"].sum().sort_index()
peak_month = monthly.idxmax()
peak_label = pd.Period(peak_month).strftime("%B %Y")
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(monthly.index, monthly.values, marker="o", linewidth=2)
ax.set_xlabel("Month")
ax.set_ylabel("Outlier-corrected revenue (INR ₹)")
ax.set_title(f"Outlier-Corrected Monthly Revenue — Peak: {peak_label}")
ax.grid(True, alpha=0.3)
ax.tick_params(axis="x", rotation=30)
for month, value in monthly.items():
    ax.annotate(f"₹{value:,.0f}", (month, value), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "monthly_revenue_trend.png", dpi=160, bbox_inches="tight")
plt.close(fig)

print("Saved visualizations/return_rate_by_payment.png")
print("Saved visualizations/monthly_revenue_trend.png")
print("Return rates (%):", {k: round(float(v), 1) for k, v in rates.items()})
print("Outlier-corrected monthly revenue:")
for month, value in monthly.items():
    print(f"{month}: ₹{value:,.2f}")
print(f"Actual peak month: {peak_month} (₹{monthly.loc[peak_month]:,.2f})")
