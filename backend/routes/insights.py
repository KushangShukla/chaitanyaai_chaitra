from fastapi import APIRouter
import psycopg2
from backend.scripts.services.insight_engine import build_insights
from backend.db.connection import get_connection

router = APIRouter()

@router.get("/insights")
def get_insights():

    conn = get_connection()

    cursor = conn.cursor()

    try:
        # ================= DB FETCH =================
        cursor.execute("""
            SELECT 
                AVG(sales_lag_1),
                AVG(sales_lag_2),
                AVG(store_sales_ratio),
                AVG(dept_sales_ratio),
                AVG(weekly_sales)
            FROM walmart_sales_refined
        """)

        row = cursor.fetchone()

        if not row:
            return {"cards": [], "insights": [], "llm_explanation": ""}

        lag1, lag2, store_ratio, dept_ratio, avg_sales = row

        trend = (lag1 or 0) - (lag2 or 0)

        # ================= CORE DATA =================
        core_data = {
            "trend": trend,
            "avg_sales": avg_sales or 0
        }

        # ================= ML + LLM ENGINE =================
        try:
            result = build_insights(core_data)

            cards = result.get("cards", [])
            insights = result.get("insights", [])
            llm_explanation = result.get("llm_explanation", "")

        except Exception as e:
            print("Insight Engine Failed:", e)

            # ================= FALLBACK =================
            cards = [
                {"title": "Avg Sales", "value": round(avg_sales or 0, 2)},
                {"title": "Trend", "value": "Increasing" if trend > 0 else "Decreasing"},
                {"title": "Store Strength", "value": round(store_ratio or 0, 2)},
                {"title": "Dept Impact", "value": round(dept_ratio or 0, 2)}
            ]

            insights = []

            if trend > 0:
                insights.append("Sales momentum is increasing")
            else:
                insights.append("Sales momentum is decreasing")

            if store_ratio > dept_ratio:
                insights.append("Stores outperform departments")
            else:
                insights.append("Departments influence variability")

            if avg_sales > 20000:
                insights.append("Sales performance is strong")
            else:
                insights.append("Sales performance needs improvement")

            llm_explanation = "Fallback explanation used due to LLM/ML failure."

        # ================= FINAL RETURN =================
        return {
            "cards": cards,
            "insights": insights,
            "llm_explanation": llm_explanation
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()