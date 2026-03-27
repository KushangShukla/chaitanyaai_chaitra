import shap
import joblib
import pandas as pd
from sqlalchemy import create_engine

engine= create_engine(
     "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df=pd.read_sql("SELECT * FROM walmart_sales_refined", engine)

X=df.drop(columns=["weekly_sales"])

model=joblib.load(
    "../data/Outputs/final_model_production/final_model_production.pkl"
)

print("Model Loaded successfully.")

explainer= shap.TreeExplainer(model)
print("SHAP explainer initialized.")

sample_X=X.sample(1000, random_state=42)

shap_values= explainer.shap_values(sample_X)

print("SHAP values computed.")

import numpy as np

np.save(
    "../data/Outputs/shap_setup/shap_values_sample.npy",
    shap_values
)

print("SHAP values saved.")