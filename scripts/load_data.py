import pandas as pd
from sqlalchemy import create_engine

# Load CSV
df = pd.read_csv("D:\Projects\CHAITRA\data\walmart_sales.csv")

# Select required columns
required_columns = [
    "Store",
    "Dept",
    "Date",
    "Weekly_Sales",
    "IsHoliday",
    "Temperature",
    "Fuel_Price",
    "CPI",
    "Unemployment",
    "Type",
    "Size",
    "week",
    "month",
    "year"
]

df = df[required_columns]

# 🔴 THIS IS THE CRITICAL LINE
df.columns = [col.lower() for col in df.columns]

# Convert date
df["date"] = pd.to_datetime(df["date"])

# PostgreSQL connection
engine = create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

# Insert into PostgreSQL
df.to_sql(
    name="walmart_sales",
    con=engine,
    schema="public",
    if_exists="append",
    index=False,
    method="multi"
)


print("Data successfully inserted into PostgreSQL")
