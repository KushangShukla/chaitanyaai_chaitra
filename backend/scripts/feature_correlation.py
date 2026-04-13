import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df = pd.read_sql("SELECT * FROM walmart_sales_encoded", engine)

print("Data loaded:", df.shape)

corr_matrix=df.drop(columns=["weekly_sales"]).corr()

plt.figure(figsize=(14,10))
sns.heatmap(
    corr_matrix,
    cmap="coolwarm",
    center=0
)
plt.title("Feature Correlation Heatmap")

plt.savefig("../data/Outputs/feature_correlation/feature_correlation_all.png",
            dpi=300,
            bbox_inches="tight")
plt.show()

high_corr=(
    corr_matrix.abs()
    .unstack()
    .sort_values(ascending=False)
)

high_corr=high_corr[
    (high_corr>0.8) & (high_corr<1.0)
]

print(high_corr.head(20))
