import pandas as pd
from sqlalchemy import create_engine

# SQLite DB create
engine = create_engine("sqlite:///behavioral_finance.db")

# Load CSV files
users = pd.read_csv("data/raw/users.csv")
transactions = pd.read_csv("data/raw/transactions.csv")
segments = pd.read_csv("data/processed/user_segments.csv")
anomalies = pd.read_csv("data/processed/transactions_with_anomalies.csv")

# Push to SQLite
users.to_sql("users", engine, if_exists="replace", index=False)
transactions.to_sql("transactions", engine, if_exists="replace", index=False)
segments.to_sql("user_segments", engine, if_exists="replace", index=False)
anomalies.to_sql("transaction_anomalies", engine, if_exists="replace", index=False)

print("SQLite DB Created Successfully!")