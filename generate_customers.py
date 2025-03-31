import pandas as pd
from faker import Faker
import random

# Setup
fake = Faker()
Faker.seed(0)
random.seed(0)

# Generate data
data = []
for i in range(1, 101):
    customer_id = f"CID{i:06d}"
    first_name = fake.first_name()
    last_name = fake.last_name()
    birth_date = fake.date_of_birth(minimum_age=25, maximum_age=85)
    
    data.append({
        "Customer ID": customer_id,
        "First Name": first_name,
        "Last Name": last_name,
        "Date of Birth": birth_date
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("dummy_customers.csv", index=False)

print(df.head())
