
-- RevenueGuard: Historical RFM Customer Segmentation
-- Uses positive sale transactions with known customer IDs.
-- Snapshot date: 2011-12-10, one day after the final transaction.
-- Monetary amounts are gross positive sales-line values.
-- Flagged duplicate records are retained in this reporting scenario.

CREATE OR REPLACE VIEW analytics.vw_customer_rfm AS

WITH customer_metrics AS (
    SELECT
        customer_id,

        (DATE '2011-12-10' - MAX(invoice_date)::date)
            AS recency_days,

        COUNT(DISTINCT invoice)
            AS frequency,

        ROUND(SUM(gross_sales_value), 2)
            AS monetary_value,

        MIN(invoice_date)::date
            AS first_purchase_date,

        MAX(invoice_date)::date
            AS last_purchase_date

    FROM analytics.retail_transactions

    WHERE transaction_type = 'sale'
      AND has_customer_id = TRUE
      AND customer_id IS NOT NULL
      AND invoice_date < TIMESTAMP '2011-12-10'

    GROUP BY customer_id
),

rfm_scores AS (
    SELECT
        *,

        6 - NTILE(5) OVER (
            ORDER BY recency_days ASC, customer_id
        ) AS r_score,

        NTILE(5) OVER (
            ORDER BY frequency ASC, customer_id
        ) AS f_score,

        NTILE(5) OVER (
            ORDER BY monetary_value ASC, customer_id
        ) AS m_score

    FROM customer_metrics
),

customer_segments AS (
    SELECT
        *,

        CASE
            WHEN r_score >= 4 AND f_score >= 4
                THEN 'Champions'

            WHEN r_score >= 3 AND f_score >= 4
                THEN 'Loyal Customers'

            WHEN r_score >= 4 AND f_score BETWEEN 2 AND 3
                THEN 'Potential Loyalists'

            WHEN r_score >= 4 AND f_score = 1
                THEN 'Recent Customers'

            WHEN r_score <= 2 AND f_score >= 4
                THEN 'At Risk'

            WHEN r_score <= 2 AND f_score <= 2
                THEN 'Hibernating'

            ELSE 'Needs Attention'
        END AS customer_segment

    FROM rfm_scores
)

SELECT
    customer_id,
    recency_days,
    frequency,
    monetary_value,
    r_score,
    f_score,
    m_score,
    customer_segment,
    first_purchase_date,
    last_purchase_date

FROM customer_segments;
