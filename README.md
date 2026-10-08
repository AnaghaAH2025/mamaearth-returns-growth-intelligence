# Mamaearth Returns & Growth Intelligence Pipeline

## Project Overview

This project analyzes Mamaearth order data through a three-layer pipeline:

1. SQL Relational Layer
2. Python Cleaning and Analysis Layer
3. GenAI Narrative Layer

The purpose is to identify return patterns and revenue trends that can support regional operations and finance decisions.

---

## Repository Structure

```text
mamaearth-capstone/
│
├── README.md
│
├── sql/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── reports.sql
│
├── data/
│   ├── customers.csv
│   ├── products.csv
│   └── orders.csv
│
├── analysis/
│   ├── clean_and_eda.py
│   └── visualize.py
│
├── visualizations/
│   ├── return_rate_by_payment.png
│   └── monthly_revenue_trend.png
│
├── narrator/
│   ├── findings.json
│   └── generate_narrative.py
│
└── mamaearth.db

