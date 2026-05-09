import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

SERVER_NAME = r"LAPTOP-IJ4V7L7Q\SQLEXPRESS"
DATABASE_NAME = "BehavioralFinanceDB"

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    "Trusted_Connection=yes;"
)

connection_url = quote_plus(connection_string)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_url}")

anomalies = pd.read_csv("data/processed/transactions_with_anomalies.csv")

anomalies = anomalies[[
    "transaction_id",
    "user_id",
    "transaction_date",
    "transaction_hour",
    "category",
    "merchant",
    "amount",
    "payment_method",
    "mood_score",
    "financial_stress_level",
    "impulse_purchase",
    "is_anomaly"
]]

anomalies.to_sql(
    "transaction_anomalies",
    engine,
    if_exists="append",
    index=False
)

print("Anomaly data loaded successfully!")