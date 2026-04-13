import pandas as pd

# Load each model's metrics
baseline = pd.read_csv("../data/Outputs/baseline_model/metrics_linear_regression.csv")
rf = pd.read_csv("../data/Outputs/random_forest_model/metrics_random_forest.csv")
xgb_initial = pd.read_csv("../data/Outputs/xgboost_model/metrics_xgboost.csv")
xgb_tuned = pd.read_csv("../data/Outputs/hyperparameter_tuning/metrics_hyperparameter_tuning.csv")
xgb_refined = pd.read_csv("../data/Outputs/refined_model_training/metrics_refined_model_training.csv")

#Add model names
baseline["Model Stage"]="Baseline (Linear Regression)"
rf["Model Stage"]="Random Forest"
xgb_initial["Model Stage"]="XGBoost (Initial)"
xgb_tuned["Model Stage"]="XGBoost (Tuned - Day 29)"
xgb_refined["Model Stage"]="XGBoost (Refined - Day 33)"

#Combine
benchmark_df=pd.concat(
    [baseline,rf,xgb_initial,xgb_tuned,xgb_refined],
    ignore_index=True
)

#Reorder columns
benchmark_df=benchmark_df[
    ["Model Stage", "MAE", "RMSE", "R2_Score"]
]

print("\nConsolidated Benchmark:")
print(benchmark_df)

benchmark_df.to_csv(
    "../data/Outputs/performance_benchmarking/performance_benchmarking_consolidated.csv",
    index=False
)

print("\nConsolidated benchmark report saved.")

import matplotlib.pyplot as plt

#MAE
plt.figure(figsize=(10,6))

plt.bar(
    benchmark_df["Model Stage"],
    benchmark_df["MAE"]
)

plt.xticks(rotation=45)
plt.title("MAE Comparison Across Models")
plt.ylabel("MAE")

plt.tight_layout()

plt.savefig(
    "../data/Outputs/performance_benchmarking/mae_comparison.png",
    dpi=300
)

plt.show()

#RMSE
plt.figure(figsize=(10,6))

plt.bar(
    benchmark_df["Model Stage"],
    benchmark_df["RMSE"]
)

plt.xticks(rotation=45)
plt.title("RMSE Comparison Across Models")
plt.ylabel("RMSE")

plt.tight_layout()

plt.savefig(
    "../data/Outputs/performance_benchmarking/rmse_comparison.png",
    dpi=300
)

plt.show()

#R2_Score
plt.figure(figsize=(10,6))

plt.bar(
    benchmark_df["Model Stage"],
    benchmark_df["R2_Score"]
)

plt.xticks(rotation=45)
plt.title("R2 Score Comparison Across Models")
plt.ylabel("R2_Score")

plt.tight_layout()

plt.savefig(
    "../data/Outputs/performance_benchmarking/r2_score_comparison.png",
    dpi=300
)

plt.show()
