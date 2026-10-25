
-- RevenueGuard: Customer Concentration and Repeat Purchases
-- Historical positive sales, identifiable customers only.

WITH ranked_customers AS (
    SELECT
        customer_id,
        monetary_value,
        frequency,
        ROW_NUMBER() OVER (
            ORDER BY monetary_value DESC, customer_id
        ) AS customer_rank,
        COUNT(*) OVER () AS total_customers,
        SUM(monetary_value) OVER () AS total_customer_sales
    FROM analytics.vw_customer_rfm
)

SELECT
    COUNT(*) AS customers_analyzed,

    COUNT(*) FILTER (
        WHERE frequency > 1
    ) AS repeat_customers,

    ROUND(
        100.0 * COUNT(*) FILTER (WHERE frequency > 1)
        / NULLIF(COUNT(*), 0),
        2
    ) AS repeat_customer_percentage,

    ROUND(
        100.0 * SUM(monetary_value) FILTER (
            WHERE customer_rank <= CEIL(total_customers * 0.10)
        )
        / NULLIF(MAX(total_customer_sales), 0),
        2
    ) AS top_10_percent_sales_share,

    ROUND(
        100.0 * SUM(monetary_value) FILTER (
            WHERE customer_rank <= CEIL(total_customers * 0.20)
        )
        / NULLIF(MAX(total_customer_sales), 0),
        2
    ) AS top_20_percent_sales_share

FROM ranked_customers;
