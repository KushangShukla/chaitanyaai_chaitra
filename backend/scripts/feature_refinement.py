import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

engine=create_engine(
     "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df=pd.read_sql("SELECT * FROM walmart_sales_ml_ready_final",engine)

X=df.drop(columns=["weekly_sales"])
y=df["weekly_sales"]

model=XGBRegressor(
    n_estimators=400,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.7,
    colsample_bytree=0.7,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1
)


model.fit(X,y)

importances=pd.Series(
    model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

print("\nFeature Importance Ranking:")
print(importances)

threshold=0.01

selected_features=importances[importances>threshold].index.tolist()

print("\nRefined Feature Count:", len(selected_features))

refined_df=df[selected_features+["weekly_sales"]]

refined_df.to_sql(
    "walmart_sales_refined",
    engine,
    if_exists="replace",
    index=False
)

print("Refined dataset saved.")