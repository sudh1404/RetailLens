
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.retail_transactions (
    record_id BIGINT PRIMARY KEY,
    invoice TEXT,
    stock_code TEXT,
    description TEXT,
    quantity INTEGER,
    invoice_date TIMESTAMP,
    unit_price NUMERIC(18, 4),
    customer_id TEXT,
    country TEXT,
    source_sheet TEXT,
    is_duplicate BOOLEAN,
    is_cancellation BOOLEAN,
    has_customer_id BOOLEAN,
    line_value NUMERIC(20, 4),
    transaction_type TEXT,
    gross_sales_value NUMERIC(20, 4)
);
