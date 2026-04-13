import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

engine=create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df=pd.read_sql("SELECT * FROM walmart_sales_refined",engine)

print("Refined Dataset loaded:", df.shape)

X=df.drop(columns=["weekly_sales"])
y=df["weekly_sales"]

X_train,X_test,y_train,y_test=train_test_split(
    X,y,
    test_size=0.2,
    random_state=42
)

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

model.fit(X_train,y_train)

y_pred=model.predict(X_test)

mae=mean_absolute_error(y_test,y_pred)
rmse=np.sqrt(mean_squared_error(y_test,y_pred))
r2=r2_score(y_test,y_pred)

print("\nRefined Model Performancee:")
print(f"MAE : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R2 : {r2:.4f}")

refined_model_training_results=pd.DataFrame([{
    "Model":"Refined_Model_Training",
    "MAE":mae,
    "RMSE":rmse,
    "R2_Score":r2
}])

refined_model_training_results.to_csv("../data/Outputs/refined_model_training/metrics_refined_model_training.csv", index=False)

import joblib

joblib.dump(
    model,
    "../data/Outputs/refined_model_training/final_model_week5_optimized.pkl"
)
print("Final optimized model saved.")