import pandas as pd
from datetime import date

# --------------------------
# Load Data
# --------------------------
# This should be generated fresh each day before running this script
holdings = pd.read_csv("customer_holdings_valued.csv")

# --------------------------
# Summarize Portfolio Value Per Customer
# --------------------------
daily_summary = holdings.groupby("Customer ID")["Current Value"].sum().reset_index()
daily_summary["Date"] = date.today()

# --------------------------
# Append to Portfolio History
# --------------------------
try:
    history = pd.read_csv("portfolio_history.csv")
    history = pd.concat([history, daily_summary], ignore_index=True)
except FileNotFoundError:
    history = daily_summary

# --------------------------
# Save Updated History
# --------------------------
history.to_csv("portfolio_history.csv", index=False)
print("✅ Daily portfolio snapshot saved.")
