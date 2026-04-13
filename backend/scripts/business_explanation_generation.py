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

print("SHAP values computed for explanation layer.")

index_to_explain=0

prediction=model.predict(Sample_X.iloc[[index_to_explain]])[0]

contributions=pd.Series(
    shap_values[index_to_explain],
    index=Sample_X.columns
).sort_values(ascending=False)

top_positive=contributions.head(3)
top_negative=contributions.tail(3)

print("Top Positive Contributors: ")
print(top_positive)

print("\n Top Negative Contributors:")
print(top_negative)

explanation_text=f"""
Sales Forcast: {prediction:.2f}

Key positive drivers:
- {top_positive.index[0]} significantly increased project sales.
- {top_positive.index[1]} contributed positively. 
- {top_positive.index[2]} added upward momentum. 

Key negative drivers:
- {top_negative.index[0]} slightly reduced projectd sales.
- {top_negative.index[1]} had a downward influence.
- {top_negative.index[2]} marginally decreased forecast.
"""

print("\nGenerated Business Explanation")
print(explanation_text)

with open("../data/Outputs/business_explanation_generation/sample_business_explanation.txt","w") as f:
    f.write(explanation_text)

print("Explanation saved.")