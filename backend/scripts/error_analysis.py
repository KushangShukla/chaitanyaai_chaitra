import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

engine=create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df=pd.read_sql("SELECT * FROM walmart_sales_ml_ready_final", engine)

print("Dataset loaded:", df.shape)

X=df.drop(columns=["weekly_sales"])
y=df["weekly_sales"]

X_train,X_test,y_train,y_test=train_test_split(
    X,y,
    test_size=0.2,
    random_state=42
)

model=XGBRegressor(
    n_estimators=300,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train,y_train)

y_pred=model.predict(X_test)

errors=y_test-y_pred

error_df=X_test.copy()
error_df["actual_sales"]=y_test
error_df["predicted_sales"]=y_pred
error_df["error"]=errors
error_df["abs_error"]=np.abs(errors)

#Error Distribution

plt.figure(figsize=(8,5))
sns.histplot(error_df["error"],bins=50,kde=True)
plt.title("Prediction Error Distributon")
plt.savefig("../data/Outputs/error_analysis/error_distribution.png",
            dpi=300,
            bbox_inches="tight")
plt.show()

#Error vs Actual Sales

plt.figure(figsize=(8,5))
sns.scatterplot(
    x=error_df["actual_sales"],
    y=error_df["error"],
    alpha=0.3
)
plt.axhline(0,color="red",linestyle="--")
plt.title("Error vs Actual Sales")

plt.savefig("../data/Outputs/error_analysis/error_vs_actual.png",
            dpi=300,
            bbox_inches="tight")
plt.show()

#Segment-wise Error (holiday vs non-holiday)

if "isholiday" in error_df.columns:
    holiday_error=error_df.groupby("isholiday")["abs_error"].mean()
    print("\nMean Absolute Error by Holiday Falg:")
    print(holiday_error)

#Top error cases (outliers)

print("\nTop 10 highest error cases:")
print(error_df.sort_values("abs_error",ascending=False).head(10))
