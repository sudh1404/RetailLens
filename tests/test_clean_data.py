
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from clean_data import clean_data


def sample_data():
    return pd.DataFrame({
        "invoice": ["10001", "C10002", "10003", "10004"],
        "stock_code": ["A", "B", "C", "D"],
        "description": ["Product A", "Product B", "Product C", "Product D"],
        "quantity": [2, -1, -3, 1],
        "invoice_date": ["2011-01-01"] * 4,
        "unit_price": [10.0, 10.0, 5.0, 0.0],
        "customer_id": ["12345", "12345", None, "12346"],
        "country": ["United Kingdom"] * 4,
        "source_sheet": ["Test"] * 4,
    })


def test_all_rows_preserved():
    result = clean_data(sample_data())
    assert len(result) == 4


def test_transaction_classification():
    result = clean_data(sample_data())

    assert result["transaction_type"].tolist() == [
        "sale",
        "cancellation",
        "negative_adjustment",
        "non_positive_price",
    ]


def test_gross_sales_only_includes_sales():
    result = clean_data(sample_data())

    assert result["gross_sales_value"].sum() == 20.0


def test_missing_customer_id():
    result = clean_data(sample_data())

    assert result["has_customer_id"].tolist() == [
        True, True, False, True
    ]


def test_duplicate_detection():
    data = sample_data()
    data = pd.concat(
        [data, data.iloc[[0]]],
        ignore_index=True
    )

    result = clean_data(data)

    assert result["is_duplicate"].sum() == 1


def test_record_ids_are_unique():
    result = clean_data(sample_data())

    assert result["record_id"].is_unique
