
from pathlib import Path
import json

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_FILE = BASE_DIR / "data" / "raw" / "online_retail_II.xlsx"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

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


def load_dataset():
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_FILE}"
        )

    print("Reading Excel workbook...")
    workbook = pd.ExcelFile(RAW_FILE)

    frames = []

    for sheet in workbook.sheet_names:
        print(f"Loading sheet: {sheet}")

        frame = pd.read_excel(
            workbook,
            sheet_name=sheet,
            dtype={
                "Invoice": str,
                "StockCode": str,
                "Customer ID": str,
            },
        )

        frame = frame.rename(columns=COLUMN_MAP)
        frame["source_sheet"] = sheet

        frames.append(frame)

    df = pd.concat(frames, ignore_index=True)

    print(f"Loaded {len(df):,} rows.")
    return df


def profile_dataset(df):
    print("\nAnalyzing data quality...")

    invoice = df["invoice"].astype("string")
    quantity = pd.to_numeric(df["quantity"], errors="coerce")
    price = pd.to_numeric(df["unit_price"], errors="coerce")

    cancellation_mask = invoice.str.upper().str.startswith("C").fillna(False)

    missing_values = {
        col: int(df[col].isna().sum())
        for col in df.columns
    }

    missing_percentages = {
        col: round(float(df[col].isna().mean() * 100), 2)
        for col in df.columns
    }

    summary = {
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "source_sheets": df["source_sheet"].value_counts().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": missing_values,
        "missing_percentages": missing_percentages,
        "cancellation_invoice_rows": int(cancellation_mask.sum()),
        "negative_quantity_rows": int((quantity < 0).sum()),
        "zero_quantity_rows": int((quantity == 0).sum()),
        "zero_price_rows": int((price == 0).sum()),
        "negative_price_rows": int((price < 0).sum()),
        "missing_customer_id_rows": int(df["customer_id"].isna().sum()),
        "unique_invoice_numbers": int(df["invoice"].nunique()),
        "unique_products": int(df["stock_code"].nunique()),
        "unique_customers": int(df["customer_id"].nunique()),
        "unique_countries": int(df["country"].nunique()),
        "earliest_transaction": str(df["invoice_date"].min()),
        "latest_transaction": str(df["invoice_date"].max()),
    }

    column_profile = pd.DataFrame({
        "column": df.columns,
        "data_type": [str(df[c].dtype) for c in df.columns],
        "missing_count": [missing_values[c] for c in df.columns],
        "missing_percentage": [
            missing_percentages[c] for c in df.columns
        ],
        "unique_values": [
            int(df[c].nunique()) for c in df.columns
        ],
    })

    return summary, column_profile


def main():
    df = load_dataset()

    summary, column_profile = profile_dataset(df)

    summary_path = REPORT_DIR / "data_quality_summary.json"
    columns_path = REPORT_DIR / "column_profile.csv"

    with open(summary_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    column_profile.to_csv(columns_path, index=False)

    print("\n========== DATA QUALITY REPORT ==========")

    for key, value in summary.items():
        if key not in ("missing_values", "missing_percentages"):
            print(f"{key}: {value}")

    print("\nMissing values:")
    for col, count in summary["missing_values"].items():
        print(f"  {col}: {count:,}")

    print("\nReports saved:")
    print(summary_path)
    print(columns_path)


if __name__ == "__main__":
    main()
