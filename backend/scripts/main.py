from backend.scripts.orchestrator.query_router import QueryRouter

router=QueryRouter()

user_id=input("Enter user ID: ")
role=input("Enter role (admin/user): ")

while True:
    query=input("\nAsk your business question: ")

    if query.lower() == "exit":
        break

    response=router.route(query,user_id,role)

    print("\nAI Response:\n")
    print(response)