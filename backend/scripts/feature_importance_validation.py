import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor

engine=create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df=pd.read_sql("SELECT * FROM walmart_sales_feature_selected", engine)

print("Data loaded:", df.shape)

X=df.drop(columns=["weekly_sales"])
y=df["weekly_sales"]

rf=RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

rf.fit(X,y)

importances=pd.Series(
    rf.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

print(importances.head(10))

plt.figure(figsize=(10,6))
sns.barplot(
    x=importances.head(10),
    y=importances.head(10).index
)
plt.title("Top 10 Feature Importances")

plt.savefig("../data/Outputs/feature_importance_validation/feature_importance_top10.png",
            dpi=300,
            bbox_inches="tight"
)
plt.show()

final_features=importances.index.tolist()

print("Final feature count:", len(final_features))
