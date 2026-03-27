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

Sample_X=X.sample(1000,random_state=42)

explainer=shap.TreeExplainer(model)
shap_values=explainer.shap_values(Sample_X)

print("SHAP values ready.")

plt.figure()
shap.summary_plot(
    shap_values,
    Sample_X,
    show=False
)

plt.savefig(
    "../data/Outputs/shap_visualizations/shap_summary_plot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
print("SHAP summary plot saved.")

plt.figure()
shap.summary_plot(
    shap_values,
    Sample_X,
    plot_type="bar",
    show=False
)

plt.savefig(
    "../data/Outputs/shap_visualizations/shap_bar_plot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
print("SHAP bar plot saved.")

plt.figure()
shap.dependence_plot(
    "sales_lag_1",
    shap_values,
    Sample_X,
    show=False
)

plt.savefig(
    "../data/Outputs/shap_visualizations/shap_dependency_sales_lag_1.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
print("SHAP dependence plot saved.")