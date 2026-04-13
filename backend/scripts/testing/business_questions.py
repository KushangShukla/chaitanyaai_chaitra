from backend.scripts.orchestrator.query_router import QueryRouter

test_questions = [

"Why did sales increase in store 3?",

"What factors affect weekly sales?",

"Explain department 5 performance",

"Which store has highest sales trend?",

"Why are some stores underperforming?",

"What is the predicted sales next week?",

"Which economic factors influence revenue?"

]
router=QueryRouter()

for q in test_questions:
    print("\n====================")
    print("QUESTION:",q)

    response=router.route(q)

    print("\nRESPONSE:")
    print(response)

