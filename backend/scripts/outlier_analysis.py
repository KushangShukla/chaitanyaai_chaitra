#Load cleaned Data
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df = pd.read_sql("SELECT * FROM walmart_sales_cleaned", engine)

print("Data loaded:", df.shape)

#Focus on business-analytics Numeric columns
numeric_cols = [
    "weekly_sales",
    "temperature",
    "fuel_price",
    "cpi",
    "unemployment"
]

plt.figure()
sns.boxplot(y=df["weekly_sales"])
plt.title("Outlier Detection: Weekly Sales")

plt.savefig("../data/Outputs/outlier_analysis/outlier_weekly_sales.png",
            dpi=300,
            bbox_inches="tight")
plt.show()

for col in numeric_cols[1:]:
    plt.figure()
    sns.boxplot(y=df[col])
    plt.title(f"Outlier Detection: {col}")

    filename = f"outlier_{col}.png"
    plt.savefig(f"../data/Outputs/outlier_analysis/{filename}",
                dpi=300,
                bbox_inches="tight")
    plt.show()

Q1 = df["weekly_sales"].quantile(0.25)
Q3 = df["weekly_sales"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[
    (df["weekly_sales"] < lower_bound) |
    (df["weekly_sales"] > upper_bound)
]

print("Number of weekly sales outliers:", len(outliers))

print("Negative sales:",
      (df["weekly_sales"] < 0).sum())

df.to_sql(
    "walmart_sales_validated",
    engine,
    if_exists="replace",
    index=False
)
