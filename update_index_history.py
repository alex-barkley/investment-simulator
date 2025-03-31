import yfinance as yf
import pandas as pd
from datetime import date, timedelta

# === CONFIG ===
ticker = "^GSPC"
start_date = date.today() - timedelta(days=30)
end_date = date.today() + timedelta(days=1)

# === DOWNLOAD DATA ===
print(f"📥 Fetching data for {ticker} from {start_date} to {end_date}...")
raw_data = yf.download(ticker, start=start_date, end=end_date)

if raw_data.empty:
    print("❌ No index data returned.")
    exit()

# === FLATTEN MULTIINDEX IF PRESENT ===
if isinstance(raw_data.columns, pd.MultiIndex):
    raw_data.columns = raw_data.columns.get_level_values(0)

# === CLEAN AND PREPARE DATA ===
data = raw_data.reset_index()[["Date", "Close"]]
data = data.rename(columns={"Close": "Index Value"})
data["Date"] = pd.to_datetime(data["Date"]).dt.date

# === LOAD EXISTING HISTORY OR START FRESH ===
try:
    history = pd.read_csv("index_history.csv")
    history["Date"] = pd.to_datetime(history["Date"]).dt.date
except FileNotFoundError:
    history = pd.DataFrame(columns=["Date", "Index Value"])

# === COMBINE, REMOVE DUPLICATES, SORT ===
combined = pd.concat([history, data], ignore_index=True)
combined = combined.drop_duplicates(subset="Date")
combined = combined.sort_values("Date")

# === SAVE TO FILE ===
combined.to_csv("index_history.csv", index=False)

# Ensure only valid date values before printing summary
valid_dates = pd.to_datetime(combined["Date"], errors="coerce").dropna().dt.date
print(f"\n✅ Index history updated: {min(valid_dates)} to {max(valid_dates)}")

