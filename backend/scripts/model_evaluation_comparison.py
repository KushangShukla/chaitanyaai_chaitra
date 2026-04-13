import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

engine=create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df=pd.read_sql("SELECT * FROM walmart_sales_ml_ready_final",engine)

print("Dataset loaded:", df.shape)

X=df.drop(columns=["weekly_sales"])
y=df["weekly_sales"]

X_train,X_test,y_train,y_test=train_test_split(
    X,y,
    test_size=0.2,
    random_state=42,
)

lr=LinearRegression()
lr.fit(X_train,y_train)
y_pred_lr=lr.predict(X_test)

rf=RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train,y_train)
y_pred_rf=rf.predict(X_test)

def evaluate_model(y_true,y_pred):
    mae=mean_absolute_error(y_true,y_pred)
    mse=mean_squared_error(y_true,y_pred)
    rmse=np.sqrt(mse)
    r2=r2_score(y_true,y_pred)
    return mae,rmse,r2

lr_mae,lr_rmse,lr_r2=evaluate_model(y_test,y_pred_lr)
rf_mae,rf_rmse,rf_r2=evaluate_model(y_test,y_pred_rf)

comparison_df=pd.DataFrame({
    "Model": ["Linear Regression","Random Forest"],
    "MAE": [lr_mae,rf_mae],
    "RMSE": [lr_rmse,rf_rmse],
    "R2-Score": [lr_r2,rf_r2]
})

print("\nModel Comparison:")
print(comparison_df)

comparison_df.to_csv(
    "../data/Outputs/model_evaluation_comparison/model_comparison_day24.csv",
    index=False
)
