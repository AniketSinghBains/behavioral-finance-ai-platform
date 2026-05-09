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

users = pd.read_csv("data/raw/users.csv")
transactions = pd.read_csv("data/raw/transactions.csv")
user_segments = pd.read_csv("data/processed/user_segments.csv")

user_segments.rename(columns={"cluster": "cluster_id"}, inplace=True)

users.to_sql("users", engine, if_exists="append", index=False)
transactions.to_sql("transactions", engine, if_exists="append", index=False)
user_segments.to_sql("user_segments", engine, if_exists="append", index=False)


print("Data loaded successfully into SQL Server!")