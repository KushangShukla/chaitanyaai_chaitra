from scripts.orchestrator.query_router import QueryRouter

router=QueryRouter()

queries=[
    "Why did sales increase in store 3?",
    "Predict next week sales",
    "What affects retail sales?"
]

for q in queries:

    route=router.route(q)

    print("\nQuery:",q)
    print("Route:",route)