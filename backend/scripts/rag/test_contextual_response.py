from backend.scripts.rag.retrieval import retrieve_context
from backend.scripts.llm.llm_engine import LLMEngine

llm=LLMEngine()

def test_query(question):

    print("\n=========================")
    print("QUESTION:",question)

    context=retrieve_context(question)

    print("\nRetrieved Context:\n")
    print(context[:500]) # Show partition context

    response=llm.generate_rag_response(context,question)

    print("\nAI RESPONSE:\n")
    print(response)

if __name__=="__main__":
    queries=[
        "Why did sales increase in Store 3?",
        "What factors affect weekly sales?",
        "Explain sales performance for department 5?",
        "Why are some stores underperforming?"
    ]

    for q in queries:
        test_query(q)
        