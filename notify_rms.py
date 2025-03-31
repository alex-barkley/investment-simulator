import pandas as pd
from datetime import timedelta
import smtplib
from email.message import EmailMessage

# === CONFIG ===
ALERT_THRESHOLD = 0.10  # 10% relative move
INDEX_FILE = "index_history.csv"
PORTFOLIO_FILE = "portfolio_history.csv"
CUSTOMERS_FILE = "customers_with_rm.csv"
RMS_FILE = "relationship_managers.csv"

# === LOAD DATA ===
portfolio = pd.read_csv(PORTFOLIO_FILE)
index = pd.read_csv(INDEX_FILE)
customers = pd.read_csv(CUSTOMERS_FILE)
rms = pd.read_csv(RMS_FILE)

# Clean date columns
portfolio["Date"] = pd.to_datetime(portfolio["Date"]).dt.date
index["Date"] = pd.to_datetime(index["Date"]).dt.date

# Use most recent portfolio snapshot date
today = max(portfolio["Date"])
week_ago = today - timedelta(days=7)

# Get latest available index dates for both
available_index_dates = sorted(index["Date"])
index_today = max([d for d in available_index_dates if d <= today])
index_week_ago = max([d for d in available_index_dates if d <= week_ago])

# Get index values
index_today_value = index[index["Date"] == index_today]["Index Value"].values[0]
index_week_ago_value = index[index["Date"] == index_week_ago]["Index Value"].values[0]
index_return = (index_today_value - index_week_ago_value) / index_week_ago_value

# Portfolio returns
p_today = portfolio[portfolio["Date"] == today]
p_week_ago = portfolio[portfolio["Date"] == week_ago]
returns = p_today.merge(p_week_ago, on="Customer ID", suffixes=("_Today", "_WeekAgo"))

returns["Portfolio Return"] = (
    (returns["Current Value_Today"] - returns["Current Value_WeekAgo"]) / returns["Current Value_WeekAgo"]
)
returns["Relative Move"] = returns["Portfolio Return"] - index_return

# Add RM info
returns = returns.merge(customers[["Customer ID", "RM ID"]], on="Customer ID", how="left")
returns = returns.merge(rms, on="RM ID", how="left")

# Filter clients with significant movement
alerts = returns[returns["Relative Move"].abs() > ALERT_THRESHOLD]

if alerts.empty:
    print("✅ No alerts to send today.")
    exit()

# === GROUP ALERTS PER RM ===
grouped = alerts.groupby("RM ID")

for rm_id, group in grouped:
    rm_name = f"{group['First Name'].iloc[0]} {group['Last Name'].iloc[0]}"
    to_email = group["Email"].iloc[0] if "Email" in group.columns else "rm@example.com"

    subject = f"🚨 Portfolio Alert: Significant Client Movements"

    body_lines = [
        f"Dear {rm_name},\n",
        f"The following clients had portfolio movements of more than ±10% relative to the S&P 500 between {index_week_ago} and {index_today}:\n"
    ]

    for _, row in group.iterrows():
        cid = row["Customer ID"]
        port_ret = row["Portfolio Return"] * 100
        rel_ret = row["Relative Move"] * 100
        body_lines.append(f" - Customer {cid}: Portfolio Return = {port_ret:.2f}%, Relative to S&P 500 = {rel_ret:.2f}%")

    body_lines.append("\nPlease review their portfolios.\n\nBest,\nYour Automated Alert System")
    body = "\n".join(body_lines)

    # === Print instead of sending
    print(f"\n--- Email to: {to_email} ---")
    print(f"Subject: {subject}")
    print(body)

    # === Uncomment to enable actual sending
    # msg = EmailMessage()
    # msg["Subject"] = subject
    # msg["From"] = "your@email.com"
    # msg["To"] = to_email
    # msg.set_content(body)
    #
    # with smtplib.SMTP("smtp.yourmail.com", 587) as smtp:
    #     smtp.starttls()
    #     smtp.login("your@email.com", "yourpassword")
    #     smtp.send_message(msg)

print("\n✅ Alert email preparation complete.")
