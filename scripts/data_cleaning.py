import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df = pd.read_sql("SELECT * FROM walmart_sales", engine)

print("Data loaded")
print(df.shape)

missing = df.isnull().sum()
missing_percent = (missing / len(df)) * 100

missing_df = pd.DataFrame({
    "missing_count": missing,
    "missing_percent": missing_percent
}).sort_values(by="missing_percent", ascending=False)

print(missing_df)

# Fill markdown columns with 0
markdown_cols = [
    "markdown1", "markdown2", "markdown3",
    "markdown4", "markdown5"
]

for col in markdown_cols:
    if col in df.columns:
        df[col] = df[col].fillna(0)

# Fill isholiday safely
df["isholiday"] = df["isholiday"].fillna(False)

print("Missing values after cleaning:")
print(df.isnull().sum())
df.to_sql(
    "walmart_sales_cleaned",
    engine,
    if_exists="replace",
    index=False
)
