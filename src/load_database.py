
from pathlib import Path
import os
import time

import psycopg
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
CSV_FILE = BASE_DIR / "data" / "processed" / "retail_transactions.csv"

load_dotenv(BASE_DIR / ".env")


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "revenueguard"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
    )


def load_transactions():
    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"Processed CSV not found: {CSV_FILE}"
        )

    print("Connecting to PostgreSQL...")
    start_time = time.time()

    with get_connection() as conn:
        with conn.cursor() as cur:

            # Confirm that the destination table exists.
            cur.execute(
                "SELECT to_regclass('analytics.retail_transactions')"
            )
            if cur.fetchone()[0] is None:
                raise RuntimeError(
                    "Destination table does not exist. "
                    "Run 01_create_tables.sql first."
                )

            # Load into a temporary staging table.
            # The main table stays unchanged if loading fails.
            cur.execute("""
                CREATE TEMP TABLE staging_transactions
                (LIKE analytics.retail_transactions INCLUDING ALL)
                ON COMMIT DROP
            """)

            print("Loading CSV into staging table...")

            with cur.copy("""
                COPY staging_transactions (
                    record_id,
                    invoice,
                    stock_code,
                    description,
                    quantity,
                    invoice_date,
                    unit_price,
                    customer_id,
                    country,
                    source_sheet,
                    is_duplicate,
                    is_cancellation,
                    has_customer_id,
                    line_value,
                    transaction_type,
                    gross_sales_value
                )
                FROM STDIN
                WITH (FORMAT CSV, HEADER TRUE, NULL '')
            """) as copy:
                with open(CSV_FILE, "rb") as file:
                    while chunk := file.read(1024 * 1024):
                        copy.write(chunk)

            cur.execute(
                "SELECT COUNT(*) FROM staging_transactions"
            )
            staged_count = cur.fetchone()[0]

            print(f"Staged records: {staged_count:,}")

            # Replace the analytical dataset atomically.
            # Re-running this script will not duplicate records.
            cur.execute(
                "TRUNCATE TABLE analytics.retail_transactions"
            )

            cur.execute("""
                INSERT INTO analytics.retail_transactions
                SELECT * FROM staging_transactions
            """)

            cur.execute(
                "SELECT COUNT(*) FROM analytics.retail_transactions"
            )
            final_count = cur.fetchone()[0]

            if final_count != staged_count:
                raise RuntimeError(
                    "Row count mismatch after database load!"
                )

            print(f"Database records: {final_count:,}")

        # The transaction commits here only if all steps succeed.

    elapsed = time.time() - start_time

    print("\n========== LOAD COMPLETE ==========")
    print(f"Rows loaded: {final_count:,}")
    print(f"Elapsed time: {elapsed:.2f} seconds")
    print("Database load successful!")


if __name__ == "__main__":
    load_transactions()
