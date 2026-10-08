.mode csv
.import data/customers.csv customers
.import data/products.csv products
.import data/orders.csv orders

UPDATE orders
SET discount_pct = NULL
WHERE discount_pct = '';

UPDATE orders
SET rating = NULL
WHERE rating = '';
