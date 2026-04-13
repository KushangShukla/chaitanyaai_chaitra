from backend.scripts.llm.explanation_engine import ExplanationEngine

engine=ExplanationEngine()

sample_data={
    "store":3,
    "dept":5,
    "weekly_sales":21000,
    "temperature":22,
    "fuel_price":3.1,
    "cpi":210,
    "unemployment":7.1,
    "sales_lag_1":19500,
    "rolling_mean_4":20000
}

response=engine.generate_sales_explanation(sample_data)

print("\nExplanation:\n")
print(response)