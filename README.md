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

## Project Structure

fred-pipeline/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── fred_pipeline.py # Main ETL script
├── config/
│ └── settings_example.env # Example environment variables file
├── data/ # Output directory (created after running)
│ ├── econ.db # SQLite database with data
│ ├── history.csv # Full historical time series data
│ ├── indicators.csv # Latest snapshot with MoM/YoY calculations
│ └── indicators.png # Visualization of key economic indicators
└── docs/
└── architecture.png # Optional diagram of pipeline architecture

## Setup Instructions

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
pip install -r requirements.txt
```
4. **Configure environment variables**
cp config/settings_example.env config/settings.env
-Edit config/settings.env and replace <YOUR_API_KEY> with your actual FRED API key.
```
5. **Run the ETL pipeline**
python fred_pipeline.py
-This will create a data/ directory with:
  -econ.db SQLite database
  -CSV reports (history.csv, indicators.csv)
  -A plot image (indicators.png)

