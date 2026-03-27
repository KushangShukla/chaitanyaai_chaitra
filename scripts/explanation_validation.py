import shap
import joblib
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

engine=create_engine(
     "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df=pd.read_sql("SELECT * FROM walmart_sales_refined", engine)

X=df.drop(columns=["weekly_sales"])

model=joblib.load(
    "../data/Outputs/final_model_production/final_model_production.pkl"
)

explainer=shap.TreeExplainer(model)

#Sample Dataset
Sample_X=X.sample(1000, random_state=42)
shap_values=explainer.shap_values(Sample_X)

print("Validation dataset ready.")

top_features_list=[]

for i in range(50):
    contributions=pd.Series(
        shap_values[i],
        index=Sample_X.columns
    ).abs().sort_values(ascending=False)

    top_features_list.append(contributions.index[0])

feature_frequency=pd.Series(top_features_list).value_counts()

print("\nTop Feature Frequency (Across 50 Samples):")
print(feature_frequency)

shap_variance=pd.DataFrame(shap_values).var()

variance_series=pd.Series(
    shap_variance.values,
    index=Sample_X.columns
).sort_values(ascending=False)

print("\n SHAP Variance Ranking:")
print(variance_series.head(10))

correlation=np.corrcoef(
    Sample_X["sales_lag_1"],
    shap_values[:, Sample_X.columns.get_loc("sales_lag_1")]
)[0,1]

print("\n Correlation between sales_lag_1 and its SHAP value:")
print(correlation)