import os, time, sqlite3, requests, pandas as pd, datetime as dt
from dotenv import load_dotenv

load_dotenv("config/settings.env")

API = "https://api.stlouisfed.org/fred"
API_KEY = os.getenv("FRED_API_KEY")

SERIES = [
    ("FEDFUNDS", "Federal Funds Rate"),
    ("CPIAUCSL", "CPI, All Urban Consumers"),
    ("UNRATE", "Unemployment Rate"),
]

DB_PATH = "data/econ.db"

def _ten_year_start():
    today = pd.Timestamp.today().normalize()
    ten_years_ago = today - pd.DateOffset(years=10)
    return ten_years_ago.replace(day=1).date().isoformat()

START = _ten_year_start()
END = dt.date.today().isoformat()

def get_json(url, params, tries=3, backoff=1.6):
    for i in range(tries):
        r = requests.get(url, params=params, timeout=20)
        if r.ok:
            return r.json()
        time.sleep(backoff ** i)
    r.raise_for_status()

def fetch_series_meta(series_id):
    js = get_json(f"{API}/series", {
        "series_id": series_id, "api_key": API_KEY, "file_type": "json"
    })
    return js["seriess"][0]

def fetch_observations(series_id, start=START, end=END):
    js = get_json(f"{API}/series/observations", {
        "series_id": series_id, "api_key": API_KEY, "file_type": "json",
        "observation_start": start, "observation_end": end
    })
    obs = pd.DataFrame(js["observations"])
    if obs.empty:
        return obs
    obs = obs[["date", "value"]].rename(columns={"date": "obs_date"})
    obs["series_id"] = series_id
    # Convert '.' to NA, then to numeric NaN
    obs["value"] = pd.to_numeric(obs["value"].replace(".", pd.NA), errors="coerce")
    # Handle missing values by forward-fill then backward-fill
    obs["value"] = obs["value"].fillna(method="ffill").fillna(method="bfill")
    obs["obs_date"] = pd.to_datetime(obs["obs_date"]).dt.date
    return obs[["series_id", "obs_date", "value"]]

def init_db(conn):
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS series(
        series_id TEXT PRIMARY KEY,
        title TEXT,
        frequency TEXT,
        units TEXT,
        seasonal_adjustment TEXT,
        last_updated TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS observations(
        series_id TEXT,
        obs_date DATE,
        value REAL,
        PRIMARY KEY (series_id, obs_date),
        FOREIGN KEY (series_id) REFERENCES series(series_id)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS load_log(
        run_ts TEXT,
        series_id TEXT,
        rows_loaded INTEGER,
        status TEXT,
        message TEXT
    )""")
    conn.commit()

def upsert_series(conn, meta):
    row = (
        meta["id"], meta.get("title"), meta.get("frequency"), meta.get("units"),
        meta.get("seasonal_adjustment"), meta.get("last_updated")
    )
    conn.execute("""
        INSERT INTO series(series_id,title,frequency,units,seasonal_adjustment,last_updated)
        VALUES (?,?,?,?,?,?)
        ON CONFLICT(series_id) DO UPDATE SET
          title=excluded.title,
          frequency=excluded.frequency,
          units=excluded.units,
          seasonal_adjustment=excluded.seasonal_adjustment,
          last_updated=excluded.last_updated
    """, row)
    conn.commit()

def upsert_observations(conn, df):
    if df.empty:
        return 0
    rows = df.values.tolist()
    conn.executemany("""
        INSERT OR REPLACE INTO observations(series_id, obs_date, value)
        VALUES (?, ?, ?)
    """, rows)
    conn.commit()
    return len(rows)

def log(conn, series_id, rows, status, msg=""):
    conn.execute("""
        INSERT INTO load_log(run_ts, series_id, rows_loaded, status, message)
        VALUES (?, ?, ?, ?, ?)
    """, (dt.datetime.utcnow().isoformat(timespec="seconds"), series_id, rows, status, msg))
    conn.commit()

def compute_outputs(conn):
    q = """
    SELECT obs_date as date, series_id, value
    FROM observations
    WHERE obs_date >= date('now','-10 years')
    """
    df = pd.read_sql_query(q, conn, parse_dates=["date"])
    if df.empty:
        return None, None, None

    wide = df.pivot(index="date", columns="series_id", values="value").sort_index()
    wide = wide.resample("MS").last()

    mom = wide.pct_change(1)
    yoy = wide.pct_change(12)

    latest = pd.concat([
        wide.tail(1),
        mom.tail(1).add_suffix("_MoM"),
        yoy.tail(1).add_suffix("_YoY"),
    ], axis=1)

    return wide, mom, latest

def main():
    if not API_KEY:
        raise RuntimeError("Set FRED_API_KEY in config/settings.env")

    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    for sid, _ in SERIES:
        try:
            meta = fetch_series_meta(sid)
            upsert_series(conn, meta)
            obs = fetch_observations(sid, START, END)
            rows = upsert_observations(conn, obs)
            log(conn, sid, rows, "OK", f"Loaded {rows}")
        except Exception as e:
            log(conn, sid, 0, "ERROR", str(e))

    wide, mom, latest = compute_outputs(conn)
    if wide is not None:
        wide.to_csv("data/history.csv", index=True, date_format="%Y-%m")
        latest.round(4).to_csv("data/indicators.csv", index=False)

        import matplotlib.pyplot as plt
        ax = wide.tail(120).plot(figsize=(10, 6))
        ax.set_title("Key U.S. Indicators (FRED) — Last 10 Years")
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        plt.tight_layout()
        plt.savefig("data/indicators.png", dpi=150)
        plt.close()

    conn.close()

if __name__ == "__main__":
    main()
