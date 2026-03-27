from scripts.llm.llm_engine import LLMEngine

class ExplanationEngine:
    def __init__(self):
        self.llm=LLMEngine()

    def generate_sales_explanation(self,data):

        context=f"""
Store: {data['store']}
Department: {data['dept']}
Weekly Sales: {data['weekly_sales']}

Business Factors:
Temperature: {data['temperature']}
Fuel Price: {data['fuel_price']}
CPI: {data['cpi']}
Unemployment: {data['unemployment']}

Historical Trend:
Last Week Sales: {data['sales_lag_1']}
Rolling Mean Sales: {data['rolling_mean_4']}
"""
        
        question="Explain why weekly sales behaved this way."

        return self.llm.generate_rag_response(context,question)