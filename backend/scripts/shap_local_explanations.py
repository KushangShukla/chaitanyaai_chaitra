import shap
import joblib
import pandas as pd
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

print("SHAP local analysis ready.")

index_to_explain=0

print("Explaining row index:", index_to_explain)

prediction=model.predict(Sample_X.iloc[[index_to_explain]])[0]

print("Prediction value:", prediction)

plt.figure()

shap.plots._waterfall.waterfall_legacy(
    explainer.expected_value,
    shap_values[index_to_explain],
    Sample_X.iloc[index_to_explain]
)

plt.savefig(
    "../data/Outputs/shap_local_explanations/shap_waterfall_plot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
print("Waterfall plot saved.")

shap.initjs()

force_plot=shap.force_plot(
    explainer.expected_value,
    shap_values[index_to_explain],
    Sample_X.iloc[index_to_explain]
)

shap.save_html(
    "../data/Outputs/shap_local_explanations/shap_force_plot.html",
    force_plot
)

print("Force plot saved as HTML.")

import numpy as np

contributions=pd.Series(
    shap_values[index_to_explain],
    index=Sample_X.columns
).sort_values(ascending=False)

print("\nTop Positive Contributors:")
print(contributions.head(5))

print("\nTOp Negative Contributors:")
print(contributions.tail(5))
