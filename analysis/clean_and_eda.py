import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Load source CSV files
customers = pd.read_csv(DATA_DIR / "customers.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")

print("Raw data loaded successfully")
print("Customers:", len(customers))
print("Products:", len(products))
print("Orders:", len(orders))

print("\nMissing values:")
print("Discount:", orders["discount_pct"].isna().sum())
print("Rating:", orders["rating"].isna().sum())

print("\nPayment methods:")
print(orders["payment_method"].value_counts())

print("\nPotential duplicate orders:")
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

print(orders.duplicated(subset=duplicate_columns).sum())

# Standardize payment method names
orders["payment_method"] = orders["payment_method"].str.upper()

print("\nStandardized payment methods:")
print(orders["payment_method"].value_counts())

# Remove duplicate orders
orders = orders.drop_duplicates(
    subset=duplicate_columns,
    keep="first"
)

print("\nAfter removing duplicates:")
print("Orders:", len(orders))

# Fill missing discounts with 0%
orders["discount_pct"] = orders["discount_pct"].fillna(0)

print("\nMissing discounts after cleaning:")
print(orders["discount_pct"].isna().sum())

# Keep missing ratings as missing
print("\nRating values after cleaning:")
print("Missing ratings:", orders["rating"].isna().sum())
print("Average rating:", orders["rating"].mean())

# Return rate by payment method
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

print("\nReturn rate by payment method:")
print(return_by_payment)

# Merge product prices with orders
orders = orders.merge(
    products[["product_id", "price"]],
    on="product_id",
    how="left"
)

# Calculate revenue for each order
orders["revenue"] = (
    orders["quantity"]
    * orders["price"]
    * (1 - orders["discount_pct"] / 100)
)

# Convert order date to datetime
orders["order_date"] = pd.to_datetime(orders["order_date"])

# Calculate monthly revenue
monthly_revenue = (
    orders.groupby(orders["order_date"].dt.to_period("M"))["revenue"]
    .sum()
)

print("\nMonthly revenue:")
print(monthly_revenue)

# Overall return rate
total_orders = len(orders)
total_returns = orders["returned"].sum()
overall_return_rate = total_returns / total_orders * 100

print("\nOverall return rate:")
print("Total orders:", total_orders)
print("Returned orders:", total_returns)
print("Return rate:", overall_return_rate)

