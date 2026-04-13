import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df = pd.read_sql("SELECT * FROM walmart_sales_normalized", engine)

print("Data loaded:", df.shape)

corr_features = [
    "weekly_sales",
    "temperature",
    "fuel_price",
    "cpi",
    "unemployment"
]

corr_matrix = df[corr_features].corr()

print(corr_matrix)

plt.figure(figsize=(8, 6))
sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)
plt.title("Feature Correlation Heatmap")

plt.savefig("../data/Outputs/feature_relevance/feature_correlation_heatmap.png",
            dpi=300,
            bbox_inches="tight")
plt.show()

target_corr = corr_matrix["weekly_sales"].sort_values(ascending=False)
print(target_corr)
