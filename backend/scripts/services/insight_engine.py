from backend.scripts.ml.model_manager import ModelManager
from backend.scripts.services.llm_service import llm_service

model_manager = ModelManager()
model_manager.load_automl()

def generate_ml_insights(core_data: dict):
    insights = []
    cards = []

    #  Get feature importance
    importance = getattr(model_manager, "feature_importance", {})

    if importance:
        top_features = sorted(
            importance.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        #  ML CARDS
        for f, v in top_features:
            cards.append({
                "title": f"Top Factor: {f}",
                "value": round(v, 3)
            })

        #  ML INSIGHTS
        for f, v in top_features:
            if v > 0.15:
                insights.append(f"{f} strongly influences predictions")

        # Special logic
        if "sales_lag_1" in importance:
            insights.append("Recent sales trend is a major driver")

    return cards, insights


#  FALLBACK RULE ENGINE (your existing logic preserved)
def fallback_insights(core_data: dict):
    insights = []

    trend = core_data.get("trend", 0)
    avg_sales = core_data.get("avg_sales", 0)

    if trend > 0:
        insights.append("Sales are increasing")
    else:
        insights.append("Sales are declining")

    if avg_sales > 20000:
        insights.append("Sales performance is strong")
    else:
        insights.append("Sales performance needs improvement")

    return insights


#  OPTIONAL LLM LAYER (safe)
def llm_explain(insights):
    try:
        # plug your LLM here (optional)
        # return enhanced explanation
        return insights  # keep safe for now
    except:
        return insights

# load once
try:
    llm_service.load()
except:
    pass


def build_insights(data):
    trend = data.get("trend", 0)
    avg_sales = data.get("avg_sales", 0)

    insights = []
    cards = []

    # ================= ML LOGIC =================
    if trend > 0:
        insights.append("Sales are increasing")
    else:
        insights.append("Sales are decreasing")

    if avg_sales > 20000:
        insights.append("Sales performance is strong")
    else:
        insights.append("Sales need improvement")

    cards = [
        {"title": "Trend", "value": "Increasing" if trend > 0 else "Decreasing"},
        {"title": "Avg Sales", "value": round(avg_sales, 2)}
    ]

    # ================= LLM =================
    prompt = f"""
    Analyze business data:
    Trend: {trend}
    Average Sales: {avg_sales}

    Explain insights in simple business language:
    """

    llm_output = llm_service.generate(prompt)

    return {
        "insights": insights,
        "cards": cards,
        "llm_explanation": llm_output
    }