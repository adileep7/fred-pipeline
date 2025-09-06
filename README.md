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
## 💼 Business Use Case
Economic analysts often need to monitor inflation, unemployment, and interest rates over time. Manual downloads from the FRED website are slow and error-prone. This pipeline automates ingestion, transformation, and storage of these indicators, making them ready for analysis and visualization.

---
## 🏗️ Architecture Design
┌────────────┐
│  FRED API  │
└────┬───────┘
     │
     ▼
┌────────────────────────────┐
│     Extract (Python)       │
│  - requests library        │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│    Transform (pandas)      │
│  - Clean & format data     │
│  - Calculate MoM / YoY     │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│ Load                       │
│ - SQLite DB                │
│ - CSV / Parquet files      │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│ Visualize                  │
│ - Matplotlib charts        │
└────────────────────────────┘

---
## 🛠️ Tools & Rationale
- **Python**: for scripting ETL logic and transformations.
- **requests**: to fetch data securely via API.
- **pandas**: for MoM/YoY calculations and data cleaning.
- **SQLite**: lightweight relational DB, quick local analytics.
- **Matplotlib**: simple data visualization for end-users.
- **dotenv**: for key management and reproducibility.
---
## 📦 How to Run

### Prerequisites
- Python 3.9+
- A free FRED API key (get one: https://fred.stlouisfed.org/docs/api/api_key.html)

## Instructions

1. **Clone the repository**

```bash
git clone https://github.com/janedoe7/fred-pipeline.git
cd fred-pipeline
```
2. **Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows use: .\venv\Scripts\activate
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Configure environment variables**
```bash
cp config/settings_example.env config/settings.env
-Edit config/settings.env and replace <YOUR_API_KEY> with your actual FRED API key.
```
5. **Run the ETL pipeline**
```bash
python fred_pipeline.py
- This will create a `data/` directory with:
  1. SQLite database: `econ.db`
  2. CSV reports: `history.csv`, `indicators.csv`
  3. Plot image: `indicators.png`
```
