import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df = pd.read_sql("SELECT * FROM walmart_sales_kpi_enriched", engine)

print("Data loaded:", df.shape)

categorical_cols=["type"]
binary_cols=["isholiday"]

df["isholiday"]=df["isholiday"].astype(int)

df=pd.get_dummies(
    df,
    columns=categorical_cols,
    drop_first=True
)

print("Columns after encoding:")
print(df.columns)

print("Sample rows:")
print(df.head())

df.to_sql(
    "walmart_sales_encoded",
    engine,
    if_exists="replace",
    index=False
)