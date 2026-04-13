import pandas as pd
import joblib
from sqlalchemy import create_engine
from xgboost import XGBRegressor

engine=create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df = pd.read_sql("SELECT * FROM walmart_sales_refined", engine)

print("Production dataset loaded:", df.shape)

X = df.drop(columns=["weekly_sales"])
y = df["weekly_sales"]

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

joblib.dump(
    model,
    "../data/Outputs/final_model_production/final_model_production.pkl"
)

print("Production model saved successfully.")