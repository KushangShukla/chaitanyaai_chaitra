from scripts.orchestrator.query_router import QueryRouter

router=QueryRouter()

queries = [

"Why did sales increase in store 4?",
"Explain department performance",
"Predict next week sales",
"What factors affect demand?",
"Explain CPI impact on sales"

]

for q in queries:

    print("\n=====================")
    print("Query:", q)

    response = router.route(q)

    print("Response:", response)