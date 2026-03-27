import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler

engine= create_engine(
        "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df=pd.read_sql("SELECT * FROM walmart_sales_validated",engine)

print ("Data loaded:", df.shape)

scale_cols=[
    "temperature",
    "fuel_price",
    "cpi",
    "unemployment",
]   

scaler=StandardScaler()

df[scale_cols]=scaler.fit_transform(df[scale_cols])

print("Normalization completed")

print(df[scale_cols].describe())

df.to_sql(
    "walmart_sales_normalized",
    engine,
    if_exists="replace",
    index=False
)

df.to_csv("D:/Projects/CHAITRA/data/Outputs/normalization/walmart_sales_normalized.csv", index=False)