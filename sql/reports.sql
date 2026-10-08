-- Mamaearth Returns & Growth Intelligence Pipeline
-- Part 1: SQL Relational Layer & Reporting

-- 1(a) Order totals, total revenue and average order value

SELECT
    COUNT(*) AS total_orders,
    ROUND(SUM(
        o.quantity * p.price *
        (1 - COALESCE(o.discount_pct, 0) / 100.0)
    ), 2) AS total_revenue,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        ) / COUNT(*),
        2
    ) AS average_order_value
FROM orders o
JOIN products p
    ON o.product_id = p.product_id;


-- 1(b) Rating completeness

SELECT
    COUNT(*) AS total_orders,
    COUNT(rating) AS rated_orders,
    COUNT(*) - COUNT(rating) AS missing_ratings
FROM orders;


-- 1(c) Customers with no orders - LEFT JOIN

SELECT
    c.customer_id,
    c.name
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;


-- 1(c) Customers with no orders - NOT IN

SELECT
    customer_id,
    name
FROM customers
WHERE customer_id NOT IN (
    SELECT customer_id
    FROM orders
);


-- 1(d) Return rate by city

SELECT
    c.city,
    COUNT(o.order_id) AS total_orders,
    SUM(o.returned) AS returned_orders,
    ROUND(
        100.0 * SUM(o.returned) / COUNT(o.order_id),
        1
    ) AS return_rate_pct
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.city
HAVING return_rate_pct > 20
ORDER BY return_rate_pct DESC;


-- 1(e) Top 5 customers by total spending

SELECT
    c.customer_id,
    c.name,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        ), 2
    ) AS total_spend
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN products p
    ON o.product_id = p.product_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC, c.customer_id ASC
LIMIT 5;


-- 1(e) Ranks 3 to 5

SELECT
    c.customer_id,
    c.name,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        ), 2
    ) AS total_spend
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN products p
    ON o.product_id = p.product_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC, c.customer_id ASC
LIMIT 3 OFFSET 2;


-- 1(f) Category performance

SELECT
    p.category,
    COUNT(o.order_id) AS total_orders,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        ), 2
    ) AS total_revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- 1(g) Customer names starting with A

SELECT
    customer_id,
    name
FROM customers
WHERE name LIKE 'A%';


-- 1(h) Distinct acquisition sources

SELECT DISTINCT acquisition_source
FROM customers
ORDER BY acquisition_source;


-- 1(i) Add loyalty tier

ALTER TABLE customers
ADD COLUMN loyalty_tier VARCHAR(10);


-- Populate loyalty tier

UPDATE customers
SET loyalty_tier =
    CASE
        WHEN city_tier = 1 THEN 'Gold'
        ELSE 'Silver'
    END;


-- Verify loyalty tier counts

SELECT
    loyalty_tier,
    COUNT(*) AS customer_count
FROM customers
GROUP BY loyalty_tier
ORDER BY loyalty_tier;

