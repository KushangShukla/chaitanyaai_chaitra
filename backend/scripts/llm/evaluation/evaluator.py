import time
import json
from ..llm_engine import LLMEngine

class LLMEvaluator:

    def __init__(self):
        print("Initializing LLM Evaluator...")
        self.engine=LLMEngine()

    # ==========================
    # Evaluate Single Question
    # ==========================
    def evaluate_question(self,item):

        start_time=time.time()

        # Handle different categories
        if item["category"] == "rag_test":
            response = self.engine.generate_rag_response(
            item["context"],
            item["question"]
        )
        else:
            response = self.engine.generate_business_response(
            item["question"]
        )

        end_time=time.time()
        latency=end_time-start_time

        #Compute Score
        score_details=self.score_response(
            response,
            item.get("expected_keywords",[])
        )

        return {
            "question": item.get("question"),
            "response": response,
            "latency_seconds": round(latency,2),
            "response_length": len(response.split()),
            "score": score_details
        }

    def run_benchmark(self,filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            benchmark_data=json.load(f)
    
        if isinstance(benchmark_data,dict):
            questions=benchmark_data("questions",[])
        else:
            questions=benchmark_data

        results=[]

        for idx,item in enumerate(questions):
            print(f"Evaluating {idx+1}/{len(questions)}...")
            result=self.evaluate_question(item)
            results.append(result)
        
        return results 
    
    # Scoring Logic

    def score_response(self,response,expected_keywords):
        
        score=0
        matched_keywords=[]

        response_lower=response.lower()

        for keyword in expected_keywords:
            if keyword.lower() in response_lower:
                score +=1
                matched_keywords.append(keyword)
        
        if len (response.split())>20:
            score +=1

        if "because" in response_lower or "due to" in response_lower:
            score +=1
        
        return {
            "total_score":score,
            "matched_keywords":matched_keywords,
            "total_keywords_expected":len(expected_keywords)
        }