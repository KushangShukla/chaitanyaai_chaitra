import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df=pd.read_sql("SELECT * FROM walmart_sales_temporal", engine)

print("Data loaded:", df.shape)

store_kpis=(
    df.groupby("store")["weekly_sales"]
    .agg(["mean","median"])
    .reset_index()
    .rename(columns={
        "mean":"store_avg_sales",
        "median": "store_median_sales"
    })
)

dept_kpis=(
     df.groupby("dept")["weekly_sales"]
    .agg(["mean","median"])
    .reset_index()
    .rename(columns={
        "mean":"dept_avg_sales",
        "median": "dept_median_sales"
    })
)

df=df.merge(store_kpis, on="store", how="left")
df=df.merge(dept_kpis, on="dept", how="left")

print("After KPI aggregation:", df.shape)

df["store_sales_ratio"]=df["weekly_sales"]/df["store_avg_sales"]
df["dept_sales_ratio"]=df["weekly_sales"]/df["dept_avg_sales"]

df.to_sql(
    "walmart_sales_kpi_enriched",
    engine,
    if_exists="replace",
    index=False
)