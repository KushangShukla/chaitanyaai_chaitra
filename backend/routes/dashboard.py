from fastapi import APIRouter 
import psycopg2
import joblib
import os 

from scripts.services.data_service import *

router=APIRouter()

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
    conn=get_connection()
    cursor=conn.cursor()

    # KPI Queries

    cursor.execute("""
    SELECT 
        AVG(weekly_sales),
        MAX(weekly_sales),
        MIN(weekly_sales),
        COUNT(*)
        FROM walmart_sales_refined
    """)

    row=cursor.fetchone()

    print("KPI Query Result:",row)
    
    if row:
        avg_sales=float(row[0]) if row and row[0] else 0
        max_sales=float(row[1]) if row and row[0] else 0
        min_sales=float(row[2]) if row and row[0] else 0
        total_records=float(row[3]) if row and row[0] else 0
    

    else:
        avg_sales=max_sales=min_sales=total_records=0

    # Trend (last 2 entries)

    cursor.execute("""
    SELECT
        AVG(sales_lag_1),
        AVG(sales_lag_2)
        FROM walmart_sales_refined
    """)

    lag1,lag2=cursor.fetchone()
    trend=lag1-lag2 if lag1 and lag2 else 0

    # Store Performance

    cursor.execute("""
    SELECT 
        AVG(store_sales_ratio),
        AVG(dept_sales_ratio)
        FROM walmart_sales_refined
    """)

    store_ratio,dept_ratio=cursor.fetchone()

    # AUTO INSIGHTS ENGINE

    insights=[]

    if trend > 0:
        insights.append("Sales trend is improving based on recent history")
    
    else:
        insights.append("Sales are declining - intervention needed")

    if store_ratio > dept_ratio:
        insights.append("Store-level performance is stronger than department-level")
    else:
        insights.append("Department-level variation is higher-optimize categoires")
    
    if avg_sales > 20000:
        insights.append("Overall sales performance is strong")
    else:
        insights.append("Sales performance can be improved")
    
    # Explanation

    explanation=f"""
    The system analyzed historical lag features to determine the trend.

    Recent sales (lag-1) vs previous sales (lag-2) indicate a 
    {'positive' if trend > 0 else 'negative'} movement.

    Store ratio:{round(store_ratio,3)}
    Department ratio:{round(dept_ratio,3)}

    This helps identify whether performance variation is store-driven or department-driven.
    """

    # Real Trend Series (last 10 rows)
    cursor.execute("""
    SELECT sales_lag_1
    FROM walmart_sales_refined
    LIMIT 10               
    """)

    trend_rows=cursor.fetchall()

    trend_series=[float(r[0]) for r in trend_rows]

    # Feature Importance (AutoML)
    feature_importance={}

    if os.path.exists("scripts/ml/feature_importance.pkl"):

        feature_importance=joblib.load("scripts/ml/feature_importance.pkl")

    # Convert to top features
    top_features=sorted(
        feature_importance.items(),
        key=lambda x:x[1],
        reverse=True
    )[:5]

    conn.close()

    data=get_core_data()

    if not data:
        return {"error":"No data"}
    
    insights=generate_insights(data)
    prediction=generate_prediction(data)

    trend=(data["lag1"] or 0) - (data["lag2"] or 0)

    return {
        "kpis":{
            "avg_sales":data["avg_sales"],
            "max_sales":data["max_sales"],
            "min_sales":data["min_sales"],
            "total_records":data["total_records"]
        },
        "trend":trend,
        "insights":insights,
        "prediction":prediction,
        "explanation":explanation.strip(),
        "trend_series":trend_series,
        "feature_importance":top_features
    }