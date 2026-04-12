from fastapi import APIRouter
import psycopg2
import joblib

router = APIRouter()

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
            SELECT 
                AVG(weekly_sales),
                MAX(weekly_sales),
                MIN(weekly_sales),
                COUNT(*)
            FROM walmart_sales_refined
        """)

        result = cursor.fetchone()

        if not result:
            return {"error": "No data found"}

        avg_sales, max_sales, min_sales, total_records = result

        print("KPI Query Result:", result)

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

        # ================= REAL TREND (LAST 10) =================
        cursor.execute("""
            SELECT weekly_sales
            FROM walmart_sales_refined
            ORDER BY weekly_sales DESC
            LIMIT 10
        """)

        trend_data = [row[0] for row in cursor.fetchall()]

        # ================= STORE PERFORMANCE =================
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

        # ================= INSIGHTS ENGINE =================
        insights = []

        if trend > 0:
            insights.append(" Sales are increasing recently.")
        else:
            insights.append(" Sales are declining — attention needed.")

        if avg_sales > 20000:
            insights.append(" Strong overall store performance.")
        else:
            insights.append(" Sales below optimal range.")

        if best_store > 50000:
            insights.append(" Some stores performing exceptionally well.")

        if worst_store < 5000:
            insights.append(" Some stores underperforming significantly.")

        # ================= BUSINESS EXPLANATION =================
        explanation = (
            "The system analyzes historical sales patterns, lag features, and "
            "store-level performance metrics to generate predictions and insights. "
            "Trend signals are derived from recent weekly differences."
        )

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
            "explanation": explanation
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()