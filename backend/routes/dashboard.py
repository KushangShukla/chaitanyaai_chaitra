from fastapi import APIRouter
import psycopg2
import joblib
from scripts.services.insight_engine import build_insights
from scripts.ml.model_manager import ModelManager

router = APIRouter()

model_manager = ModelManager()
model_manager.load_automl()


def get_connection():
    return psycopg2.connect(
        dbname="chaitra_db",
        user="postgres",
        password="root64",
        host="localhost",
        port="5432"
    )


@router.get("/dashboard")
def get_dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # ================= KPI =================
        cursor.execute("""
            SELECT AVG(weekly_sales), MAX(weekly_sales),
                   MIN(weekly_sales), COUNT(*)
            FROM walmart_sales_refined
        """)
        result = cursor.fetchone()

        if not result:
            return {"error": "No data found"}

        avg_sales, max_sales, min_sales, total_records = result

        # ================= TREND =================
        cursor.execute("""
            SELECT sales_lag_1, sales_lag_2
            FROM walmart_sales_refined
            LIMIT 100
        """)
        rows = cursor.fetchall()

        trend = 0
        if rows:
            diffs = [r[0] - r[1] for r in rows if r[0] and r[1]]
            if diffs:
                trend = sum(diffs) / len(diffs)

        # ================= TREND DATA =================
        cursor.execute("""
            SELECT weekly_sales
            FROM walmart_sales_refined
            ORDER BY weekly_sales DESC
            LIMIT 10
        """)
        trend_data = [r[0] for r in cursor.fetchall()]

        # ================= STORE =================
        cursor.execute("""
            SELECT store_avg_sales
            FROM walmart_sales_refined
            LIMIT 100
        """)
        store_vals = [r[0] for r in cursor.fetchall() if r[0]]

        best_store = max(store_vals) if store_vals else 0
        worst_store = min(store_vals) if store_vals else 0

        # ================= FEATURE IMPORTANCE =================
        try:
            importance = joblib.load("scripts/ml/feature_importance.pkl")
        except:
            importance = {}

        # ================= ML + LLM =================
        core_data = {
            "trend": trend,
            "avg_sales": avg_sales
        }

        try:
            insight_block = build_insights(core_data)

            insights = insight_block.get("insights", [])
            cards = insight_block.get("cards", [])
            llm_explanation = insight_block.get("llm_explanation", "")

        except Exception as e:
            print("Insight Engine Failed:", e)

            #  FALLBACK
            insights = []

            if trend > 0:
                insights.append("Sales are increasing recently.")
            else:
                insights.append("Sales are declining — attention needed.")

            if avg_sales > 20000:
                insights.append("Strong overall store performance.")
            else:
                insights.append("Sales below optimal range.")

            if best_store > 50000:
                insights.append("Some stores performing exceptionally well.")

            if worst_store < 5000:
                insights.append("Some stores underperforming significantly.")

            cards = [
                {"title": "Avg Sales", "value": round(avg_sales, 2)},
                {"title": "Trend", "value": "Increasing" if trend > 0 else "Decreasing"},
            ]

            llm_explanation = "Fallback explanation used."

        # ================= RETURN =================
        return {
            "kpis": {
                "avg_sales": round(avg_sales, 2),
                "max_sales": round(max_sales, 2),
                "min_sales": round(min_sales, 2),
                "total_records": total_records,
                "best_store": round(best_store, 2),
                "worst_store": round(worst_store, 2),
            },
            "trend": round(trend, 2),
            "trend_data": trend_data,
            "feature_importance": importance,

            "insights": insights,
            "cards": cards,
            "llm_explanation": llm_explanation
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()