
-- RevenueGuard: Product and Geographic Performance
-- Positive sales only; flagged duplicates retained.

CREATE OR REPLACE VIEW analytics.vw_product_performance AS
SELECT
    stock_code,
    MAX(description) AS product_description,
    COUNT(DISTINCT invoice) AS orders_containing_product,
    SUM(quantity) AS units_sold,
    ROUND(SUM(gross_sales_value), 2) AS gross_sales,
    ROUND(
        SUM(gross_sales_value)
        / NULLIF(SUM(quantity), 0),
        2
    ) AS average_realized_unit_price
FROM analytics.retail_transactions
WHERE transaction_type = 'sale'
  AND stock_code IS NOT NULL
GROUP BY stock_code;

CREATE OR REPLACE VIEW analytics.vw_country_performance AS
SELECT
    country,
    COUNT(DISTINCT invoice) AS total_orders,
    COUNT(DISTINCT customer_id)
        FILTER (WHERE has_customer_id)
        AS identifiable_customers,
    SUM(quantity) AS units_sold,
    ROUND(SUM(gross_sales_value), 2) AS gross_sales,
    ROUND(
        SUM(gross_sales_value)
        / NULLIF(COUNT(DISTINCT invoice), 0),
        2
    ) AS average_order_value
FROM analytics.retail_transactions
WHERE transaction_type = 'sale'
GROUP BY country;
