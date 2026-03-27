import os
import json
from datetime import datetime
from .evaluator import LLMEvaluator

#CONFIG

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
QUESTIONS_PATH=os.path.join(BASE_DIR, "benchmark_questions.json")
OUTPUT_PATH= os.path.join(BASE_DIR, "evaluation_results.json")

print("Starting Evaluation...")

evaluator=LLMEvaluator()
results=evaluator.run_benchmark(QUESTIONS_PATH)

output_data={
    "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "results":results
}

# LOAD QUESTIONS

with open (OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(output_data,f,indent=4)

print("\nEvaluation Completed.")
print("Results saved to:")
print(OUTPUT_PATH)
