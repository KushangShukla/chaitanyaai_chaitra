from llm_engine import LLMEngine

context="""
Q4 revenue incresed by 15% compared to Q3.
Holiday sales and promotional campaigns contributed significantly.
"""

question="Why did revenue increase in Q4?"

llm=LLMEngine()

response=llm.generate_rag_response(context,question)

print("\nGenerated Response:\n")
print (response)