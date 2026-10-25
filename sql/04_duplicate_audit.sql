
-- RevenueGuard: Duplicate Impact Audit

SELECT
    COUNT(*) AS total_records,

    COUNT(*) FILTER (
        WHERE is_duplicate
    ) AS flagged_duplicate_rows,

    COUNT(*) FILTER (
        WHERE is_duplicate
        AND transaction_type = 'sale'
    ) AS flagged_duplicate_sale_rows,

    ROUND(
        COALESCE(
            SUM(gross_sales_value) FILTER (
                WHERE is_duplicate
            ), 0
        ), 2
    ) AS duplicate_flagged_sales_value,

    ROUND(
        SUM(gross_sales_value), 2
    ) AS gross_sales_all_rows,

    ROUND(
        SUM(gross_sales_value) FILTER (
            WHERE NOT is_duplicate
        ), 2
    ) AS gross_sales_excluding_flagged_duplicates,

    ROUND(
        100.0 * COALESCE(
            SUM(gross_sales_value) FILTER (
                WHERE is_duplicate
            ), 0
        ) / NULLIF(SUM(gross_sales_value), 0),
        2
    ) AS duplicate_flagged_sales_percentage

FROM analytics.retail_transactions;
