from fastapi import APIRouter
import psycopg2

router = APIRouter()

@router.get("/insights")
def get_insights():

    conn = psycopg2.connect(
        dbname="chaitra_db",
        user="postgres",
        password="root64",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()

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

    cursor.close()
    conn.close()

    if not row:
        return {"cards": [], "insights": []}

    lag1, lag2, store_ratio, dept_ratio, avg_sales = row

    trend = (lag1 or 0) - (lag2 or 0)

    #  KPI CARDS
    cards = [
        {"title": "Avg Sales", "value": round(avg_sales or 0, 2)},
        {"title": "Trend", "value": "Increasing" if trend > 0 else "Decreasing"},
        {"title": "Store Strength", "value": round(store_ratio or 0, 2)},
        {"title": "Dept Impact", "value": round(dept_ratio or 0, 2)}
    ]

    #  INSIGHTS
    insights = []

    if trend > 0:
        insights.append("Sales momentum is increasing ")
    else:
        insights.append("Sales momentum is decreasing ")

    if store_ratio > dept_ratio:
        insights.append("Stores are outperforming departments")
    else:
        insights.append("Departments are driving variability")

    if avg_sales > 20000:
        insights.append("Sales performance is strong")
    else:
        insights.append("Sales performance needs improvement")

    return {
        "cards": cards,
        "insights": insights
    }
