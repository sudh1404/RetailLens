# RevenueGuard — Retail Revenue & Data Quality Analytics

### A reproducible analytics workflow for cleaning, validating and analysing 1M+ retail transaction records.

<div align="center">

![Python](https://img.shields.io/badge/Python-Data%20Processing-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Analytics%20Database-4169E1?logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Interactive%20Reporting-F2C811?logo=powerbi&logoColor=black)
![pytest](https://img.shields.io/badge/pytest-6%20tests%20passing-0A9EDC?logo=pytest&logoColor=white)

</div>

---

## Table of Contents

1. [Overview](#overview)
2. [Project Objectives](#project-objectives)
3. [Dataset](#dataset)
4. [Data Quality Snapshot](#data-quality-snapshot)
5. [Analysis Areas](#analysis-areas)
6. [Workflow & Methodology](#workflow--methodology)
7. [Power BI Dashboard](#power-bi-dashboard)
8. [Repository Structure](#repository-structure)
9. [Getting Started](#getting-started)
10. [Data Validation & Testing](#data-validation--testing)
11. [Data Notes & Assumptions](#data-notes--assumptions)
12. [Limitations & Future Improvements](#limitations--future-improvements)
13. [Author](#author)

---

## Overview

Retail transaction data can contain duplicate records, missing customer identifiers, cancellations, negative quantities and inconsistent values. If these issues are not understood before analysis, they can affect revenue calculations, customer metrics and business reporting.

**RevenueGuard** is an end-to-end retail analytics project built around the [Online Retail II dataset](https://archive.ics.uci.edu/dataset/502/online+retail+ii). It establishes a repeatable workflow to inspect and prepare transaction data, load it into PostgreSQL, investigate business performance with SQL, and present the results through Power BI.

The project brings together two connected areas of work:

- **Data quality:** profile source data, identify potential issues, classify transaction records and run validation checks.
- **Business analytics:** analyse sales performance, customer segments, product performance and geographic trends.

### Project at a Glance

| Stage | Tools | Purpose |
|---|---|---|
| Data profiling | Python, pandas | Inspect source data and produce a quality summary |
| Data preparation | Python, pandas, NumPy | Standardise fields, classify transactions and create analysis-ready data |
| Database loading | PostgreSQL, psycopg | Load records into a structured analytics table |
| Business analysis | SQL, PostgreSQL | Query KPIs, revenue trends, customer segments and product performance |
| Quality assurance | pytest, SQL | Test transformation rules and inspect data consistency |
| Reporting | Power BI | Communicate business metrics and analytical findings |

> **Scope:** This is a descriptive analytics and data-quality project. It analyses historical transaction records; it does not forecast future sales or establish causal relationships.

## Project Objectives

The project is designed to answer the following questions:

1. What does the source dataset contain, and where are the main data-quality concerns?
2. How many records are duplicated or have missing customer information?
3. How should sales, cancellations, negative adjustments and invalid records be distinguished?
4. What are the overall sales and order performance patterns?
5. Which customers contribute most to purchasing activity under an RFM framework?
6. How are revenue and product performance distributed across countries?
7. How can the reliability of the preparation and reporting workflow be checked?

## Dataset

| Attribute | Details |
|---|---|
| Dataset | Online Retail II |
| Source | [UCI Machine Learning Repository — Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii) |
| Original format | Excel workbook |
| Source sheets | Year 2009–2010 and Year 2010–2011 |
| Combined records | **1,067,371** |
| Source columns | 8 transaction fields, plus a source-sheet tracking field during profiling |
| Time period | 1 December 2009 – 9 December 2011 |
| Business context | Online retail transactions |

The original workbook is not stored in this repository. Download it from the UCI source and place it at the path described in [Getting Started](#getting-started).

## Data Quality Snapshot

The profiling workflow generates `reports/data_quality_summary.json` with record counts, missing-value statistics, duplicate counts and transaction characteristics.

### Source Data Profile

| Check | Result |
|---|---:|
| Total transaction rows | **1,067,371** |
| Duplicate rows identified in source profile | **12,133** |
| Rows missing customer ID | **243,007 (22.77%)** |
| Rows missing description | **4,382 (0.41%)** |
| Cancellation invoice rows | **19,494** |
| Rows with negative quantity | **22,950** |
| Rows with zero unit price | **6,202** |
| Rows with negative unit price | **5** |
| Unique invoice numbers | **53,628** |
| Unique products / stock codes | **5,305** |
| Unique customers with an ID | **5,942** |
| Countries represented | **43** |

### What These Checks Mean

- **Duplicate records:** potential repeated transaction lines are flagged for review rather than silently removed.
- **Missing customer IDs:** customer-level analysis must account for transactions that cannot be attributed to an identified customer.
- **Cancellations:** invoice numbers beginning with `C` are classified separately from ordinary sales.
- **Negative quantities:** these are retained and classified as negative adjustments unless identified as cancellation invoices.
- **Non-positive prices and invalid numeric values:** these are separated from ordinary positive-value sales for the primary gross-sales calculation.

> **Important:** These are source-profile counts. A flagged record is not automatically an error; cancellations, adjustments and incomplete customer identifiers can be legitimate characteristics of transaction data.

## Analysis Areas

### 1. Transaction Quality & Classification

The preparation workflow standardises column names and data types, preserves source-row traceability, and creates fields used to review transaction quality.

Key fields added during preparation include:

- `record_id` — sequential identifier for traceability.
- `is_duplicate` — flags repeated transaction rows.
- `is_cancellation` — identifies cancellation invoices.
- `has_customer_id` — indicates whether a usable customer identifier is present.
- `line_value` — quantity multiplied by unit price.
- `transaction_type` — classifies the transaction record.
- `gross_sales_value` — includes only records classified as ordinary sales.

### 2. Business KPI Analysis

SQL views and queries are used to investigate:

- Sales line count and total orders.
- Identifiable customer and product counts.
- Gross sales value and units sold.
- Cancellation invoice counts and cancellation value magnitude.
- Average order value.
- Monthly and other time-based revenue trends.

The KPI layer documents that gross sales are based on positive-value sale lines and remain provisional until duplicate records have been reviewed.

### 3. Customer Intelligence

RFM-based analysis examines customers using:

- **Recency:** how recently a customer made a purchase.
- **Frequency:** how often a customer purchased.
- **Monetary value:** the value of the customer's purchases.

This provides a structured way to compare customer purchasing behaviour and identify customer segments.

### 4. Product & Geographic Performance

Additional SQL analyses explore product-level performance and revenue distribution across countries, supporting comparisons of merchandise and geographic contribution.

## Workflow & Methodology

### 1. Data Profiling — Python

The source workbook is read sheet by sheet and combined into a single dataset. The profiling script calculates:

- Dataset dimensions and source-sheet row counts.
- Missing values and missing-value percentages by column.
- Duplicate-row count.
- Cancellation, negative-quantity and non-positive-price counts.
- Unique invoice, product, customer and country counts.
- Earliest and latest transaction timestamps.

The results are saved as a JSON quality summary and a column-level CSV profile in `reports/`.

### 2. Data Cleaning & Classification — Python

The cleaning script:

- Renames source columns to consistent lowercase names.
- Preserves the original row order using a sequential record identifier.
- Standardises text fields and customer identifiers.
- Converts invoice dates, quantities and unit prices to appropriate data types.
- Flags duplicate rows without deleting them.
- Identifies cancellation invoices and customer-ID availability.
- Calculates line values and classifies transaction records.
- Calculates gross sales value only for records classified as ordinary sales.

The processed output is written to `data/processed/retail_transactions.csv`.

### 3. Database Loading — PostgreSQL

The database schema is created using `sql/01_create_tables.sql`. The loading script then:

1. Connects to PostgreSQL using environment-based configuration.
2. Creates a temporary staging table.
3. Copies the processed CSV into staging.
4. Checks the staged row count.
5. Replaces the analytical table within a transaction.
6. Verifies that the final row count matches the staged row count.

This staging approach helps prevent a failed load from leaving a partially replaced analytical table.

### 4. SQL Analysis — PostgreSQL

The SQL scripts create the analytical table and build queries for business KPIs, revenue trends, duplicate audits, RFM segmentation, customer concentration, product performance and geographic analysis.

### 5. Reporting — Power BI

The Power BI report connects the analytical data to business-facing measures and visualisations. It is intended to make revenue, order, customer and product patterns easier to review.

## Power BI Dashboard

The Power BI report is available at:

[`dashboard/RevenueGuard_dashboard.pbix`](dashboard/RevenueGuard_dashboard.pbix)

The dashboard focuses on the project's retail performance and customer intelligence outputs, including:

- Revenue and order KPIs.
- Monthly revenue trends.
- Product and country performance.
- Customer RFM segments.
- Customer distribution and purchasing patterns.

Open the PBIX file in Power BI Desktop. If the report uses a local PostgreSQL connection, update the connection settings for your own database.

## Repository Structure

```text
RevenueGuard/
│
├── src/
│   ├── profile_data.py          # Source data profiling and quality report
│   ├── clean_data.py            # Data cleaning and transaction classification
│   └── load_database.py         # PostgreSQL staging and data load
│
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_businees_kpis.sql
│   ├── 03_revenue_trends.sql
│   ├── 04_duplicate_audit.sql
│   ├── 05_customer_rfm.sql
│   ├── 06_customer_concentration.sql
│   ├── 07_product_geography.sql
│   └── 08_merchandise_products.sql
│
├── tests/
│   └── test_clean_data.py       # Data transformation tests
│
├── reports/
│   └── data_quality_summary.json
│
├── dashboard/
│   └── RevenueGuard_dashboard.pbix
│
├── requirements.txt
├── .gitignore
└── README.md
```

Generated data files are kept outside version control and are created locally when the workflow is run.

## Getting Started

### Prerequisites

- Python 3.10 or later
- PostgreSQL
- Power BI Desktop
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/sudh1404/RevenueGuard.git
cd RevenueGuard
```

### 2. Create a Virtual Environment

**Windows (Command Prompt):**

```bat
python -m venv .venv
.venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the Dataset

Download the Online Retail II workbook from the [UCI dataset page](https://archive.ics.uci.edu/dataset/502/online+retail+ii).

Create the following directory and place the downloaded workbook there:

```text
data/
└── raw/
    └── online_retail_II.xlsx
```

Keep the original workbook unchanged. The raw and processed data directories are excluded from Git.

### 5. Generate the Data Quality Profile

From the repository root, run:

```bash
python src/profile_data.py
```

This generates:

- `reports/data_quality_summary.json`
- `reports/column_profile.csv`

### 6. Clean and Prepare the Transactions

```bash
python src/clean_data.py
```

The processed dataset is written to:

```text
data/processed/retail_transactions.csv
```

### 7. Configure PostgreSQL

Create a PostgreSQL database named `revenueguard` (or use another name and set it in the environment).

Create a local `.env` file in the repository root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=revenueguard
DB_USER=postgres
DB_PASSWORD=your_local_password
```

Do not commit the `.env` file or share database credentials.

Run the table-creation script in PostgreSQL:

```sql
-- Execute the contents of:
sql/01_create_tables.sql
```

### 8. Load the Processed Data

```bash
python src/load_database.py
```

The loader expects the table `analytics.retail_transactions` to exist. It stages the CSV, checks the row count and then loads the analytical table.

### 9. Run the SQL Analysis

Execute the SQL scripts in the `sql/` directory using pgAdmin or another PostgreSQL client. Run the KPI and analysis scripts after the data has been loaded.

### 10. Run the Tests

```bash
python -m pytest -v
```

The test suite covers row preservation, transaction classification, gross-sales calculation, customer-ID availability, duplicate detection and record-ID uniqueness.

### 11. Open the Power BI Report

Open `dashboard/RevenueGuard_dashboard.pbix` in Power BI Desktop and configure the PostgreSQL connection if prompted.

## Data Validation & Testing

The project includes automated tests for core cleaning and classification behaviour.

| Test area | What it checks |
|---|---|
| Row preservation | Cleaning does not unexpectedly drop source rows |
| Transaction classification | Sales, cancellations, negative adjustments and non-positive-price rows are classified as expected |
| Gross sales calculation | Only ordinary sale records contribute to gross sales value |
| Customer identifier flag | Missing customer IDs are identified correctly |
| Duplicate detection | Repeated rows are flagged |
| Record ID uniqueness | Generated record identifiers are unique |

**Latest recorded test result: 6 tests passed.**

These tests validate selected transformation rules; they do not replace a full reconciliation of every business metric against the original workbook.

## Data Notes & Assumptions

- The original Online Retail II workbook contains two yearly sheets that are combined during ingestion.
- The profiling summary describes the raw source data before the cleaning and classification workflow.
- Duplicate records are flagged for review and retained in the processed dataset; they are not automatically removed.
- Invoice identifiers beginning with `C` are treated as cancellation invoices.
- Negative quantities outside cancellation invoices are classified as negative adjustments.
- Ordinary sales require positive quantity and positive unit price, with no cancellation flag or invalid numeric values.
- Gross sales value is calculated before duplicate review. Interpret it as a provisional analytical measure, not a final reconciled financial figure.
- Missing customer IDs limit customer-level attribution but do not necessarily make a transaction invalid.
- Customer and RFM analyses include only records that can be associated with a customer identifier where required.

## Limitations & Future Improvements

Potential next steps include:

- Add a documented duplicate-resolution policy and quantify the impact on key KPIs.
- Add source-to-database row-count and aggregate reconciliation checks.
- Expand automated tests to cover SQL views and end-to-end loading.
- Add repeatable database setup and configuration examples.
- Include dashboard screenshots and a concise business-insights summary.
- Add cohort and repeat-purchase analysis to deepen customer intelligence.

---

## Author

**Sudharshana Suryanarayanan**  
B.Tech — Data Science and Artificial Intelligence, IIIT Dharwad

[GitHub Profile](https://github.com/sudh1404) · [RevenueGuard Repository](https://github.com/sudh1404/RevenueGuard)

---

<div align="center">

*Built to demonstrate practical skills in data quality, Python data preparation, PostgreSQL, SQL analytics and business intelligence.*

</div>
