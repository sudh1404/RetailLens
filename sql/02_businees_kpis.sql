
-- RevenueGuard: Business KPI Layer
-- Gross sales represent positive-value sale lines.
-- All metrics are provisional until duplicate review.

CREATE OR REPLACE VIEW analytics.vw_business_kpis AS

WITH sales AS (
    SELECT *
    FROM analytics.retail_transactions
    WHERE transaction_type = 'sale'
),

sales_metrics AS (
    SELECT
        COUNT(*) AS sales_line_count,
        COUNT(DISTINCT invoice) AS total_orders,
        COUNT(DISTINCT customer_id)
            FILTER (WHERE has_customer_id)
            AS identifiable_customers,
        COUNT(DISTINCT stock_code) AS products_sold,
        COUNT(DISTINCT country) AS countries_served,
        SUM(gross_sales_value) AS gross_sales_value,
        SUM(quantity) AS units_sold
    FROM sales
),

cancellation_metrics AS (
    SELECT
        COUNT(*) AS cancellation_line_count,
        COUNT(DISTINCT invoice) AS cancellation_invoices,
        SUM(ABS(line_value))
            FILTER (WHERE line_value < 0)
            AS cancellation_value_magnitude
    FROM analytics.retail_transactions
    WHERE transaction_type = 'cancellation'
)

SELECT
    s.*,
    c.cancellation_line_count,
    c.cancellation_invoices,
    COALESCE(
        c.cancellation_value_magnitude, 0
    ) AS cancellation_value_magnitude,
    ROUND(
        s.gross_sales_value
        / NULLIF(s.total_orders, 0),
        2
    ) AS average_order_value
FROM sales_metrics s
CROSS JOIN cancellation_metrics c;
