def build_memory_context(history):
    context="Previous conversation:\n"

    for q,r in history:
        context += f"\nUser: {q}\nAI: {r}\n"

    return context