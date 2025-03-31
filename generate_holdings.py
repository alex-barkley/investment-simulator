import pandas as pd
import random
from faker import Faker

# Load customers
customers = pd.read_csv("dummy_customers.csv")

# Stocks universe
stocks = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'JPM', 'V', 'UNH']
fake = Faker()

# Generate holdings
holdings = []

for _, row in customers.iterrows():
    num_holdings = random.randint(1, 5)
    selected_stocks = random.sample(stocks, num_holdings)
    
    for stock in selected_stocks:
        holding = {
            "Customer ID": row["Customer ID"],
            "Stock Ticker": stock,
            "Number of Shares": random.randint(1, 100),
            "Purchase Price": round(random.uniform(50, 500), 2),
            "Purchase Date": fake.date_between(start_date='-5y', end_date='today')
        }
        holdings.append(holding)

# Create DataFrame
holdings_df = pd.DataFrame(holdings)

# Save to CSV
holdings_df.to_csv("customer_holdings.csv", index=False)

print(holdings_df.head())
