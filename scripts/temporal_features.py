import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df = pd.read_sql("SELECT * FROM walmart_sales_ml_ready", engine)

print("Data loaded:", df.shape)

df["date"]=pd.to_datetime(df["date"])

df["year"]=df["date"].dt.year
df["month"]=df["date"].dt.month
df["week"]=df["date"].dt.isocalendar().week.astype(int)
df["day_of_week"]=df["date"].dt.dayofweek

df=df.sort_values(["store","dept","date"])

df["sales_lag_1"]=df.groupby(["store","dept"])["weekly_sales"].shift(1)
df["sales_lag_2"]=df.groupby(["store","dept"])["weekly_sales"].shift(2)

df["rolling_mean_4"]=(
    df.groupby(["store","dept"])["weekly_sales"]
    .transform(lambda x: x.rolling (4).mean())
)

df=df.dropna()
print("After temporal feature extraction:" ,df.shape)

df.to_sql(
    "walmart_sales_temporal",
    engine,
    if_exists="replace",
    index=False,
)

