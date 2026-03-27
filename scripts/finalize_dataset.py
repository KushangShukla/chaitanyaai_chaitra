import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df = pd.read_sql("SELECT * FROM walmart_sales_normalized", engine)

print("Final dataset loaded:", df.shape)

print("\n--- FINAL DATA INFO ---")
print(df.info())

print("\n--- CHECK FOR NULLS ---")
print(df.isnull().sum())

print("\n--- TARGET VARIABLE SUMMARY ---")
print(df["weekly_sales"].describe())

target = "weekly_sales"

features = [
    col for col in df.columns if col != target
]

print("Number of features:", len(features))

df.to_sql(
    "walmart_sales_ml_ready",
    engine,
    if_exists="replace",
    index=False
)

df.to_csv("../data/walmart_sales_ml_ready.csv", index=False)
