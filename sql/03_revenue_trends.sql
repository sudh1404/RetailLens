
-- RevenueGuard: Monthly Sales Performance
-- Provisional gross positive sales-line values
-- Exact duplicates are currently retained.

SELECT
    DATE_TRUNC('month', invoice_date)::date AS month,
    COUNT(DISTINCT invoice) AS total_orders,
    COUNT(DISTINCT customer_id)
        FILTER (WHERE has_customer_id)
        AS active_customers,
    ROUND(SUM(gross_sales_value), 2) AS gross_sales,
    SUM(quantity) AS units_sold,
    ROUND(
        SUM(gross_sales_value)
        / NULLIF(COUNT(DISTINCT invoice), 0),
        2
    ) AS average_order_value
FROM analytics.retail_transactions
WHERE transaction_type = 'sale'
GROUP BY 1
ORDER BY 1;
