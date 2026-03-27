import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split,RandomizedSearchCV
from xgboost import XGBRegressor

engine= create_engine(
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

param_dist={
    "n_estimators": [200,300,400],
    "max_depth": [4,6,8],
    "learning_rate": [0.05, 0.1, 0.2],
    "subsample": [0.7,0.8,0.9],
    "colsample_bytree":[0.7,0.8,0.9]
}

xgb=XGBRegressor(
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1
)

random_search= RandomizedSearchCV(
    estimator=xgb,
    param_distributions=param_dist,
    n_iter=10,
    scoring="neg_root_mean_squared_error",
    cv=3,
    verbose=2,
    random_state=42,
    n_jobs=-1
)

random_search.fit(X_train,y_train)

print("Best Parameters Found:")
print(random_search.best_params_)

best_model=random_search.best_estimator_

y_pred=best_model.predict(X_test)

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae=mean_absolute_error(y_test,y_pred)
rmse=np.sqrt(mean_squared_error(y_test,y_pred))
r2=r2_score(y_test,y_pred)

print("\nTuned Model Performance:")
print(f"MAE : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R2 : {r2:.4f}")

hyperparameter_tuning_results=pd.DataFrame([{
    "Model":"Hyperparameter Tuning",
    "MAE":mae,
    "RMSE":rmse,
    "R2_Score":r2
}])

hyperparameter_tuning_results.to_csv("../data/Outputs/hyperparameter_tuning/metrics_hyperparameter_tuning.csv", index=False)

import joblib

joblib.dump(best_model, "../data/Outputs/hyperparameter_tuning/final_model_week5_tuned.pkl")
print("Tuned Model saved.")