import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df = pd.read_sql("SELECT * FROM walmart_sales_feature_selected", engine)

print("Final dataset shape:", df.shape)
print("Null values:\n", df.isnull().sum())
print("Sample rows:\n", df.head())

df.to_sql(
    "walmart_sales_ml_ready_final",
    engine,
    if_exists="replace",
    index=False
)
