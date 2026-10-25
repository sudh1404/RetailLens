# RevenueGuard — Retail Revenue & Customer Intelligence

RevenueGuard is an end-to-end retail analytics project built to explore sales performance, identify data quality issues, and understand customer purchasing behaviour using Python, PostgreSQL, SQL, and Power BI.

## Project Objectives

- Analyse retail revenue and order performance.
- Identify duplicate records, cancellations, and missing customer information.
- Explore product and geographic sales performance.
- Segment customers using RFM-based analysis.
- Present business insights through an interactive Power BI dashboard.

## Tech Stack

- **Python:** Data cleaning, profiling, and validation.
- **PostgreSQL:** Data storage and querying.
- **SQL:** Business KPIs, revenue trends, duplicate audits, customer segmentation, and product analysis.
- **Power BI:** Interactive dashboard and KPI visualisation.
- **pytest:** Automated data validation tests.

## Project Structure

- `src/` — Data cleaning, database loading, and profiling scripts.
- `sql/` — SQL scripts for business metrics and analytical queries.
- `tests/` — Automated data validation tests.
- `reports/` — Generated data quality and profiling reports.
- `dashboard/` — Power BI dashboard.
- `requirements.txt` — Python dependencies.

## Data Quality & Validation

The project includes checks for transaction classification, revenue calculations, missing customer IDs, duplicate detection, and record ID uniqueness.

**Latest test result:** 6 tests passed.

## Dashboard

The Power BI dashboard presents:

- Total revenue and order KPIs.
- Monthly revenue trends.
- Top products by revenue.
- Revenue by country.
- Revenue by customer segment.
- Customer distribution by RFM segment.

## Running the Project

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Follow the database setup instructions and configure PostgreSQL.
5. Run the relevant scripts in `src/`.
6. Run the automated tests with `python -m pytest -v`.

## Project Status

The initial analytics pipeline, SQL analysis, automated validation tests, and Power BI dashboard have been developed. Further improvements may include additional time-period comparisons and expanded customer analytics.