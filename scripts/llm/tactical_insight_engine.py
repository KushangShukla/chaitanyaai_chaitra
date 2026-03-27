from scripts.llm.llm_engine import LLMEngine

class TacticalInsightEngine:
    def __init__ (self):
        self.llm=LLMEngine()

    def generate_insight(self,context):

        prompt=f"""
You are a retail business strategist.
Based on the following sales data,provide tactical recommendations for improving store performance.

Context:
{context}

Provide:
1. Key insight
2. Business risk
3. Recommend actions
"""
        
        return self.llm.generate(prompt)