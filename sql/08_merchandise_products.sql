
-- RevenueGuard: Merchandise Product Reporting
-- Excludes selected known non-merchandise stock codes.
-- This is an explicit, provisional classification rule.
-- It does not guarantee every remaining code is merchandise.

CREATE OR REPLACE VIEW analytics.vw_merchandise_products AS

SELECT
    stock_code,
    product_description,
    orders_containing_product,
    units_sold,
    gross_sales,
    average_realized_unit_price

FROM analytics.vw_product_performance

WHERE UPPER(TRIM(stock_code)) NOT IN (
    'M',
    'DOT',
    'POST',
    'POSTAGE',
    'BANK CHARGES',
    'C2',
    'D',
    'CRUK',
    'AMAZONFEE',
    'S',
    'B',
    'PADS'
);
