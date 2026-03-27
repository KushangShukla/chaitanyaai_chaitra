import pandas as pd
from sqlalchemy import create_engine

# Connect to PostgreSQL
engine = create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

# Load data from DB
df = pd.read_sql("SELECT * FROM walmart_sales", engine)

print(" Data loaded from PostgreSQL")
print("Shape:", df.shape)
print(df.head())

print("\n--- DATA INFO ---")
print(df.info())

print("\n--- DESCRIPTIVE STATISTICS ---")
print(df.describe())

print("\n--- HOLIDAY VS NON-HOLIDAY SALES ---")
print(df.groupby("isholiday")["weekly_sales"].mean())

print("\n--- SALES BY STORE TYPE ---")
print(df.groupby("type")["weekly_sales"].mean())
