# FRED Economic Indicators Pipeline

A lightweight data engineering project that builds an ETL pipeline for U.S. macroeconomic indicators 
from the [FRED API](https://fred.stlouisfed.org/docs/api/fred/).

---

## 🧠 What this project does
A small, end-to-end data engineering project that builds an ETL pipeline for U.S. macroeconomic indicators using the FRED API. It ingests data, stores 10 years of history in SQLite, computes Month-over-Month (MoM) and Year-over-Year (YoY) changes, and publishes a CSV + PNG chart.

- **Extract** monthly indicators from FRED:
  - `FEDFUNDS` — Federal Funds Rate
  - `CPIAUCSL` — CPI, All Urban Consumers
  - `UNRATE` — Unemployment Rate
- **Transform** with Pandas:
  - Type casting, monthly alignment, MoM and YoY calculations
- **Load** into SQLite with idempotent upserts and a simple load log
- **Publish** outputs for stakeholders:
  - `history.csv`, `indicators.csv`, and `indicators.png`

---

## 📦 Quick Start

### Prerequisites
- Python 3.9+
- A free FRED API key (get one: https://fred.stlouisfed.org/docs/api/api_key.html)

### 1) Clone and set up
```bash
git clone https://github.com/<your-username>/fred-pipeline.git
cd fred-pipeline

python -m venv venv
# mac/linux
source venv/bin/activate
# windows (PowerShell)
# .\venv\Scripts\Activate.ps1

pip install -r requirements.txt

