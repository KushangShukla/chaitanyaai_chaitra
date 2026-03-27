import time
import json
from llm_engine import LLMEngine

class LLMEvaluator:

    def __init__(self):
        self.engine=LLMEngine()

    def evaluate_question(self,item):
        start_time=time.time()

        if item["category"]=="rag_test":
            response=self.engine.generate(item["context"], item["question"])
        else:
            response=self.engine.generate_business_response(item["question"])

        end_time=time.time()

        latency=end_time-start_time

        return {
            "question": item.get("question"),
            "response_length": len(response.split()),
            "latency_seconds": round(latency,2),
            "response": response
        }

    def run_benchmark(self,filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            questions=json.load(f)

        results=[]

        for item in questions:
            result=self.evaluate_question(item)
            results.append(result)
        
        return results 
    
    def score_response(self,response):
        score=0

        if len(response.split())>20:
            score +=1
        
        if "because" in response.lower() or "due to" in response.lower():
            score +=1

        if len(response)>50:
            score +=1
        
        return score