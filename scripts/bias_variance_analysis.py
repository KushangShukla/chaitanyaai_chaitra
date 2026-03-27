import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor

engine=create_engine(
     "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df=pd.read_sql("SELECT * FROM walmart_sales_ml_ready_final",engine)

X=df.drop(columns=["weekly_sales"])
y=df["weekly_sales"]

X_train,X_test,y_train,y_test = train_test_split(
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

y_train_pred=model.predict(X_train)
y_test_pred=model.predict(X_test)

train_rmse= np.sqrt(mean_squared_error(y_train,y_train_pred))
test_rmse= np.sqrt(mean_squared_error(y_test,y_test_pred))

print("\nTraining RMSE:", train_rmse)
print("Test RMSE:", test_rmse)

import matplotlib.pyplot as plt

plt.bar(["Train RMSE", "Test RMSE"], [train_rmse,test_rmse])
plt.title("Bias-Variance Analysis")

plt.savefig("../data/Outputs/bias_variance/bias_variance_analysis.png",
            dpi=300,
            bbox_inches="tight")
plt.show()
