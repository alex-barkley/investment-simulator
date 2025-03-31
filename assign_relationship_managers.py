import pandas as pd
import random
from faker import Faker

# Load customers
customers = pd.read_csv("dummy_customers.csv")

# Create dummy RMs
fake = Faker()
num_rms = 5
rms = []

for i in range(1, num_rms + 1):
    rms.append({
        "RM ID": f"RM{i:03d}",
        "First Name": fake.first_name(),
        "Last Name": fake.last_name()
    })

rms_df = pd.DataFrame(rms)
rms_df.to_csv("relationship_managers.csv", index=False)

# Assign RMs to 20% of customers
num_customers_to_assign = int(0.2 * len(customers))
selected_customer_ids = random.sample(customers["Customer ID"].tolist(), num_customers_to_assign)

# Create assignment
assignments = []
for customer_id in selected_customer_ids:
    assigned_rm = random.choice(rms)
    assignments.append({
        "Customer ID": customer_id,
        "RM ID": assigned_rm["RM ID"]
    })

assignments_df = pd.DataFrame(assignments)

# Merge with customer data (optional — to create a joined file)
customers_with_rm = customers.merge(assignments_df, on="Customer ID", how="left")
customers_with_rm.to_csv("customers_with_rm.csv", index=False)

print("✅ RMs assigned to 20% of customers")
print(customers_with_rm.head())
