from fastapi import APIRouter
import psycopg2
import numpy as np
from scripts.ml.model_manager import ModelManager

router = APIRouter()
model_manager = ModelManager()

@router.get("/predictions")
def get_predictions():

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
            "Store",
            "Dept",
            sales_lag_1,
            sales_lag_2,
            store_avg_sales,
            dept_avg_sales
        FROM walmart_sales_refined
        ORDER BY date DESC
        LIMIT 5
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    predictions = []

    for i, r in enumerate(rows):
        features = {
            "store": r[0],
            "department": r[1],
            "sales_lag_1": r[2],
            "sales_lag_2": r[3],
            "store_avg_sales": r[4],
            "dept_avg_sales": r[5],
        }

        pred = model_manager.predict(features) or 0

        #  Confidence logic
        confidence = min(100, int(
            (features["sales_lag_1"] > 0) * 30 +
            (features["sales_lag_2"] > 0) * 20 +
            (features["store_avg_sales"] > 0) * 25 +
            (features["dept_avg_sales"] > 0) * 25
        ))

        explanation = []
        if features["sales_lag_1"] > features["sales_lag_2"]:
            explanation.append("Recent trend is increasing")
        else:
            explanation.append("Recent trend is decreasing")

        if features["store_avg_sales"] > features["dept_avg_sales"]:
            explanation.append("Store performance is strong")
        else:
            explanation.append("Department performance affects output")

        predictions.append({
            "id": i,
            "prediction": float(pred),
            "confidence": confidence,
            "explanation": explanation,
            "query": f"Store {r[0]} Dept {r[1]}"
        })

    #  KPI CALCULATION
    values = [p["prediction"] for p in predictions]

    kpis = {
        "avg_prediction": round(np.mean(values), 2) if values else 0,
        "total_predictions": len(predictions)
    }

    return {
        "kpis": kpis,
        "predictions": predictions
    }