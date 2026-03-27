import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import cross_val_score,KFold
from xgboost import XGBRegressor

engine=create_engine(
     "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df=pd.read_sql("SELECT * FROM walmart_sales_ml_ready_final",engine)

X=df.drop(columns=["weekly_sales"])
y=df["weekly_sales"]

print("Dataset loaded.", df.shape)

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

kf=KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

cv_scores=cross_val_score(
    model,
    X,
    y,
    scoring="neg_root_mean_squared_error",
    cv=kf,
    n_jobs=-1
)

rmse_scores=- cv_scores

print("\nCross-Validation RMSE Scores:")
print(rmse_scores)

print("\nMean RMSE:", rmse_scores.mean())
print("Standard Deviation:", rmse_scores.std())

cv_results=pd.DataFrame({
    "Fold": range(1,6),
    "RMSE": rmse_scores
})

cv_results.to_csv(
    "../data/Outputs/cross_validation/cross_validation_results.csv",
    index=False
)
