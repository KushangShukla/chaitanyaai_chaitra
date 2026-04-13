import pandas as pd

lr=pd.read_csv("../data/Outputs/baseline_model/metrics_linear_regression.csv")
rf=pd.read_csv("../data/Outputs/random_forest_model/metrics_random_forest.csv")
xgb=pd.read_csv("../data/Outputs/xgboost_model/metrics_xgboost.csv")

comparison_df=pd.concat([lr,rf,xgb],ignore_index=True)

comparison_df["Rank"]=comparison_df["RMSE"].rank()
comparison_df=comparison_df.sort_values("Rank")

print("\nFinal Model Comparison:")
print(comparison_df)

comparison_df.to_csv(
    "../data/Outputs/final_model_comparison/final_model_comparison.csv",
    index=False
)