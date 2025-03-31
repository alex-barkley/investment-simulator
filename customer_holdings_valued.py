import pandas as pd
import yfinance as yf

# Load holdings
holdings = pd.read_csv("customer_holdings.csv")

# Get unique tickers
tickers = holdings["Stock Ticker"].unique().tolist()

# Fetch current prices using yfinance
price_data = {}
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]
        price_data[ticker] = price
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        price_data[ticker] = None

# Add current price and value
holdings["Current Price"] = holdings["Stock Ticker"].map(price_data)
holdings["Current Value"] = holdings["Number of Shares"] * holdings["Current Price"]

# Save updated holdings
holdings.to_csv("customer_holdings_valued.csv", index=False)

# Optional: aggregate total portfolio value per customer
portfolio_summary = holdings.groupby("Customer ID")["Current Value"].sum().reset_index()
portfolio_summary.columns = ["Customer ID", "Total Portfolio Value"]
portfolio_summary.to_csv("customer_portfolio_summary.csv", index=False)

print("✅ Valuation complete!")
print(portfolio_summary.head())
