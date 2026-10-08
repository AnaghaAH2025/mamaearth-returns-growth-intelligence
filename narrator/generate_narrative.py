import json
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
FINDINGS_FILE = BASE_DIR / "narrator" / "findings.json"

# Load verified Python findings
with open(FINDINGS_FILE, "r") as file:
    findings = json.load(file)

# Extract findings
data_quality = findings["data_quality"]
returns = findings["overall_returns"]
payment = findings["return_rate_by_payment"]
monthly = findings["monthly_revenue"]

# Find highest and lowest payment return rates
highest_payment = max(
    payment,
    key=lambda method: payment[method]["return_rate_pct"]
)

lowest_payment = min(
    payment,
    key=lambda method: payment[method]["return_rate_pct"]
)

# Find highest and lowest revenue months
highest_month = max(monthly, key=monthly.get)
lowest_month = min(monthly, key=monthly.get)

# Generate narrative
narrative = f"""
Mamaearth Returns & Growth Intelligence Summary

Data quality:
The analysis started with {data_quality["raw_orders"]} orders.
After removing {data_quality["duplicate_orders_removed"]} duplicate orders,
the cleaned dataset contained {data_quality["cleaned_orders"]} orders.
There were {data_quality["missing_discounts_filled"]} missing discount values,
which were treated as 0%, while {data_quality["missing_ratings"]} ratings
remained unavailable.

Returns:
The cleaned dataset contained {returns["total_orders"]} orders, of which
{returns["returned_orders"]} were returned. The overall return rate was
{returns["return_rate_pct"]:.2f}%.

Payment-method insight:
{highest_payment} had the highest return rate at
{payment[highest_payment]["return_rate_pct"]:.2f}%, while
{lowest_payment} had the lowest return rate at
{payment[lowest_payment]["return_rate_pct"]:.2f}%.
COD therefore shows a substantially higher return rate than CARD and UPI.

Revenue trend:
Monthly revenue was highest in {highest_month}, reaching
₹{monthly[highest_month]:,.2f}. The lowest monthly revenue occurred in
{lowest_month}, at ₹{monthly[lowest_month]:,.2f}.

Overall:
The analysis indicates that payment method is associated with noticeably
different return rates, with COD showing the highest observed return rate.
Revenue also varied considerably across the six months in the dataset.
These findings can help regional operations and finance teams investigate
return-related risks and changes in monthly revenue performance.
"""

print(narrative)

