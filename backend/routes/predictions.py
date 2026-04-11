from fastapi import APIRouter
import psycopg2
from scripts.ml.model_manager import ModelManager

router=APIRouter()
model_manager=ModelManager()

@router.get("/predictions")
def get_predictions():

    conn=psycopg2.connect(
        dbname="chaitra_db",
        user="postgres",
        password="root64",
        host="localhost",
        port="5432"
    )
    cursor=conn.cursor()

    # Get last 5 rows
    cursor.execute("""
    SELECT
        "Store",
        "Dept",
        sales_lag_1,
        sales_lag_2,
        store_avg_sales,
        dept_avg_sales
    FROM walmart_sales_refined
    LIMIT 5
    """)

    rows=cursor.fetchall()

    cursor.close()
    conn.close()

    predictions=[]

    for i,r in enumerate(rows):
        features={
            "store":r[0],
            "department":r[1],
            "sales_lag_1":r[2],
            "sales_lag_2":r[3],
            "store_avg_sales":r[4],
            "dept_avg_sales":r[5],
        }

        pred=model_manager.predict(features)

        predictions.append({
            "id":i,
            "prediction":float(pred or 0),
            "query":f"Store {r[0]} Dept {r[1]}"
        })
        return {"predictions":predictions}