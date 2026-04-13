import shap
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

print("SHAP ready for interpretation.")

mean_abs_shap=np.abs(shap_values).mean(axis=0)

feature_importance=pd.Series(
    mean_abs_shap,
    index=Sample_X.columns
).sort_values(ascending=False)

print("\n Business_Level Feature Impact Ranking:")
print(feature_importance)

plt.figure(figsize=(10,6))

feature_importance.head(10).plot(kind="bar")

plt.title("Top Business Drivers of Sales Prediction")
plt.ylabel("Avergae Impact Magnitude")

plt.tight_layout()

plt.savefig(
    "../data/Outputs/business_interpretation/business_driver_analysis.png",
    dpi=300
)

plt.close()
print("Business friver chart saved.")

mean_shap=shap_values.mean(axis=0)

directional_impact=pd.Series(
    mean_shap,
    index=Sample_X.columns
).sort_values(ascending=False)

print("\nFeatures Increasing Predictions:")
print(directional_impact.head(5))

print("\nFeatures Decreasing Predictions:")
print(directional_impact.tail(5))
