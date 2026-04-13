import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

engine=create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df=pd.read_sql("SELECT * FROM walmart_sales_ml_ready_final", engine)

print ("Dataset loaded:", df.shape)

X=df.drop(columns=["weekly_sales"])
y=df["weekly_sales"]

X_train,X_test,y_train,y_test= train_test_split(
    X,y,
    test_size=0.2,
    random_state=42
)

model=LinearRegression()
model.fit(X_train,y_train)

y_pred=model.predict(X_test)

mae=mean_absolute_error(y_test,y_pred)

import numpy as np
mse=mean_squared_error(y_test,y_pred)
rmse=np.sqrt(mse)

r2=r2_score(y_test,y_pred)

print("Baseline Model Performance:")
print(f"MAE : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R2 : {r2:.4f}")

lr_results=pd.DataFrame([{
    "Model":"LinearRegression",
    "MAE":mae,
    "RMSE":rmse,
    "R2_Score":r2
}])

lr_results.to_csv("../data/Outputs/baseline_model/metrics_linear_regression.csv", index=False)