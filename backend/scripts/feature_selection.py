import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_selection import VarianceThreshold
from sklearn.ensemble import RandomForestRegressor

engine=create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df=pd.read_sql("SELECT * FROM walmart_sales_encoded", engine)

print("Data loaded:", df.shape)

x=df.drop(columns=["weekly_sales"])
y=df["weekly_sales"] 

#Technique 1: Correlation-Based Fitering

features_to_drop=[
    "rolling_mean_4"
]

X=x.drop(columns=features_to_drop,errors="ignore")

print("After correlation-based filtering:", X.shape)

#Technique 2: Variance Threshold (Low- Variability Removal)

# Drop non-numeric columns (important!)
non_numeric_cols = X.select_dtypes(exclude=["number"]).columns
print("Dropping non-numeric columns:", list(non_numeric_cols))

X_numeric = X.drop(columns=non_numeric_cols)

selector=VarianceThreshold(threshold=0.01)
X_var=selector.fit_transform(X_numeric)

selected_features=X_numeric.columns[selector.get_support()]
X=pd.DataFrame(X_var,columns=selected_features)

print("After Variance thresholding:",X.shape)

#Technique 3: Model-Based Feature Importance

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

TOP_N=15

final_features=importances.head(TOP_N).index.tolist()

X_final=X[final_features]

print("Final selected features:" ,len(final_features))

final_df=X_final.copy()
final_df["weekly_sales"]=y.values

final_df.to_sql(
    "walmart_sales_feature_selected",
    engine,
    if_exists="replace",
    index=False
)
