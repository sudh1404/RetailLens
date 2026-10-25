
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_FILE = BASE_DIR / "data" / "raw" / "online_retail_II.xlsx"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COLUMN_MAP = {
    "Invoice": "invoice",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "Price": "unit_price",
    "Customer ID": "customer_id",
    "Country": "country",
}


def load_data():
    print("Loading raw transaction data...")

    workbook = pd.ExcelFile(RAW_FILE)
    frames = []

    for sheet in workbook.sheet_names:
        df = pd.read_excel(
            workbook,
            sheet_name=sheet,
            dtype={
                "Invoice": str,
                "StockCode": str,
                "Customer ID": str,
            },
        )

        df = df.rename(columns=COLUMN_MAP)
        df["source_sheet"] = sheet
        frames.append(df)

    return pd.concat(frames, ignore_index=True)


def clean_data(df):
    print("Standardizing and classifying records...")

    df = df.copy()

    # Preserve original row order for traceability.
    df.insert(0, "record_id", range(1, len(df) + 1))

    text_columns = [
        "invoice", "stock_code", "description", "country"
    ]

    for col in text_columns:
        df[col] = df[col].astype("string").str.strip()

    df["customer_id"] = (
        df["customer_id"]
        .astype("string")
        .str.replace(r"\.0$", "", regex=True)
        .str.strip()
    )

    df["invoice_date"] = pd.to_datetime(
        df["invoice_date"], errors="coerce"
    )

    df["quantity"] = pd.to_numeric(
        df["quantity"], errors="coerce"
    )

    df["unit_price"] = pd.to_numeric(
        df["unit_price"], errors="coerce"
    )

    df["is_duplicate"] = df.drop(
        columns=["record_id"]
    ).duplicated(keep="first")

    df["is_cancellation"] = (
        df["invoice"]
        .str.upper()
        .str.startswith("C")
        .fillna(False)
    )

    df["has_customer_id"] = (
        df["customer_id"].notna()
        & df["customer_id"].ne("")
    ).fillna(False)

    df["line_value"] = (
        df["quantity"] * df["unit_price"]
    )

    conditions = [
        df["is_cancellation"],
        df["quantity"].isna() | df["unit_price"].isna(),
        df["quantity"] < 0,
        df["quantity"] == 0,
        df["unit_price"] <= 0,
        df["quantity"] > 0,
    ]

    choices = [
        "cancellation",
        "invalid_numeric",
        "negative_adjustment",
        "zero_quantity",
        "non_positive_price",
        "sale",
    ]

    import numpy as np

    df["transaction_type"] = np.select(
        conditions,
        choices,
        default="other"
    )

    # Only ordinary positive-value sales contribute
    # to our primary gross sales metric.
    df["gross_sales_value"] = (
        df["line_value"]
        .where(df["transaction_type"] == "sale", 0)
    )

    return df


def main():
    df = load_data()
    clean = clean_data(df)

    output_file = OUTPUT_DIR / "retail_transactions.csv"

    clean.to_csv(output_file, index=False)

    print("\n===== CLEANING SUMMARY =====")
    print(f"Total rows preserved: {len(clean):,}")

    print("\nTransaction classifications:")
    print(clean["transaction_type"].value_counts())

    print(
        "\nDuplicate rows flagged:",
        f"{clean['is_duplicate'].sum():,}"
    )

    print(
        "Rows with customer IDs:",
        f"{clean['has_customer_id'].sum():,}"
    )

    print(
        "\nGross sales value (before duplicate review):",
        f"{clean['gross_sales_value'].sum():,.2f}"
    )

    print(f"\nSaved cleaned data to: {output_file}")


if __name__ == "__main__":
    main()
