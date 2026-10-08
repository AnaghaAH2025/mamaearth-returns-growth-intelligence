import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "visualizations"

OUTPUT_DIR.mkdir(exist_ok=True)

# Load data
products = pd.read_csv(DATA_DIR / "products.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")

# Standardize payment methods
orders["payment_method"] = orders["payment_method"].str.upper()

# Remove duplicate orders
duplicate_columns = [
    "customer_id",
    "product_id",
    "order_date",
    "quantity",
    "discount_pct",
    "payment_method",
    "rating",
    "returned"
]

orders = orders.drop_duplicates(
    subset=duplicate_columns,
    keep="first"
)

# Calculate return rate
return_by_payment = (
    orders.groupby("payment_method")
    .agg(
        total_orders=("order_id", "count"),
        returned_orders=("returned", "sum")
    )
)

return_by_payment["return_rate_pct"] = (
    return_by_payment["returned_orders"]
    / return_by_payment["total_orders"]
    * 100
)

# Create chart
return_by_payment["return_rate_pct"].plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Return Rate by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Return Rate (%)")
plt.xticks(rotation=0)
plt.tight_layout()

# Save chart
plt.savefig(
    OUTPUT_DIR / "return_rate_by_payment.png",
    dpi=300
)

plt.close()

print("Created: visualizations/return_rate_by_payment.png")

# Calculate monthly revenue

# Fill missing discounts with 0%
orders["discount_pct"] = orders["discount_pct"].fillna(0)

# Merge product prices
orders = orders.merge(
    products[["product_id", "price"]],
    on="product_id",
    how="left"
)

# Calculate revenue
orders["revenue"] = (
    orders["quantity"]
    * orders["price"]
    * (1 - orders["discount_pct"] / 100)
)

# Convert dates
orders["order_date"] = pd.to_datetime(orders["order_date"])

# Group revenue by month
monthly_revenue = (
    orders.groupby(orders["order_date"].dt.to_period("M"))["revenue"]
    .sum()
)

# Create monthly revenue chart
monthly_revenue.plot(
    kind="line",
    marker="o",
    figsize=(9, 5)
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

# Save chart
plt.savefig(
    OUTPUT_DIR / "monthly_revenue_trend.png",
    dpi=300
)

plt.close()

print("Created: visualizations/monthly_revenue_trend.png")

