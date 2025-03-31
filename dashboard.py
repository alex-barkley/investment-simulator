import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --------------------------
# Load Data
# --------------------------
customers = pd.read_csv("customers_with_rm.csv")
holdings = pd.read_csv("customer_holdings_valued.csv")
rms = pd.read_csv("relationship_managers.csv")
history = pd.read_csv("portfolio_history.csv")
history["Date"] = pd.to_datetime(history["Date"])

# --------------------------
# Prepare Holdings Data
# --------------------------
holdings = holdings.merge(customers[["Customer ID", "First Name", "Last Name", "RM ID"]], on="Customer ID", how="left")

# --------------------------
# Sidebar Filters
# --------------------------
st.sidebar.title("Filters")
view_option = st.sidebar.radio("Select View:", ["Overall Portfolio", "By Relationship Manager"])

if view_option == "By Relationship Manager":
    rm_ids = rms["RM ID"].tolist()
    selected_rm = st.sidebar.selectbox("Select RM", rm_ids)
    filtered_holdings = holdings[holdings["RM ID"] == selected_rm]
    filtered_customers = customers[customers["RM ID"] == selected_rm]
    st.title(f"Portfolio Overview for {selected_rm}")
else:
    filtered_holdings = holdings
    filtered_customers = customers
    st.title("Overall Portfolio Overview")

# --------------------------
# Summary Stats
# --------------------------
total_value = filtered_holdings["Current Value"].sum()
average_value = (
    filtered_holdings.groupby("Customer ID")["Current Value"].sum().mean()
    if not filtered_holdings.empty else 0
)
num_customers = filtered_customers["Customer ID"].nunique()

st.metric("Total Portfolio Value", f"${total_value:,.2f}")
st.metric("Average Portfolio Size", f"${average_value:,.2f}")
st.metric("Number of Customers", num_customers)

# --------------------------
# 7-Day Change Calculation
# --------------------------
today = history["Date"].max()
one_week_ago = today - timedelta(days=7)

today_values = history[history["Date"] == today]
week_ago_values = history[history["Date"] == one_week_ago]

change_df = today_values.merge(
    week_ago_values,
    on="Customer ID",
    suffixes=("_Today", "_LastWeek")
)
change_df["Change"] = change_df["Current Value_Today"] - change_df["Current Value_LastWeek"]

# --------------------------
# Client Summary View
# --------------------------
customer_values = (
    filtered_holdings.groupby("Customer ID")["Current Value"]
    .sum()
    .reset_index()
    .rename(columns={"Current Value": "Total Portfolio Value"})
)

# Add name + RM
customer_summary = customer_values.merge(
    customers[["Customer ID", "First Name", "Last Name", "RM ID"]],
    on="Customer ID",
    how="left"
)

# Add change
customer_summary = customer_summary.merge(
    change_df[["Customer ID", "Change"]],
    on="Customer ID",
    how="left"
)

# Format table
customer_summary = customer_summary[[
    "Customer ID", "First Name", "Last Name", "RM ID", 
    "Total Portfolio Value", "Change"
]].sort_values(by="Total Portfolio Value", ascending=False)

st.subheader("Client Summary View")
st.dataframe(customer_summary, use_container_width=True)

# --------------------------
# RM-specific Client Table
# --------------------------
if view_option == "By Relationship Manager":
    st.subheader(f"Client List for {selected_rm}")
    rm_clients = customer_summary[customer_summary["RM ID"] == selected_rm]
    st.dataframe(rm_clients, use_container_width=True)
