# FRED Economic Indicators Pipeline

A lightweight data engineering project that builds an ETL pipeline for U.S. macroeconomic indicators 
from the [FRED API](https://fred.stlouisfed.org/docs/api/fred/).

## 📊 What it does
- **Extracts** economic data from FRED (Federal Funds Rate, CPI, Unemployment).
- **Transforms** it with Pandas: cleans, casts, and computes Month-over-Month (MoM) and Year-over-Year (YoY) changes.
- **Loads** the results into a SQLite database for persistent storage.
- **Outputs** stakeholder-friendly CSVs and a trend visualization.

## 🛠️ Stack
- Python 3.9+
- Pandas
- Requests
- SQLite (built-in)
- Matplotlib

## 📂 Repo Structure
fred-pipeline/
├── pipeline_fred.py # Main pipeline script
├── config/settings_example.env
├── data/ # Database + outputs
└── docs/architecture.png # Diagram of pipeline flow
