from fastapi import APIRouter
import joblib
import numpy as np
import psycopg2
import datetime

router=APIRouter()

# Load trained model
model=joblib.load(r"D:/Projects/CHAITRA/data/Outputs/final_model_production/final_model_production.pkl")

FEATURE_ORDER=[
    "store",
    "department",
    "fuel_price",
    "cpi",
    "sales_lag_1",
    "sales_lag_2",
    "isholiday",
    "store_avg_sales",
    "store_sales_ratio",
    "dept_sales_ratio",
    "dept_avg_sales",
    "dept_median_sales",
    "store_median_sales", 
]

def get_confidence(features):
    score=0

    if features

def get_recent_trend(store,dept):
    conn=psycopg2.connect(
        dbname="chaitra_db",
        user="postgres", 
        password="root64",
        host="localhost",
        port="5432"
    )

    cursor=conn.cursor()

    cursor.execute("""
        SELECT weekly_sales
        FROM walmart_sales_refined
        WHERE "STORE"=%s
        ORDER BY date DESC
        LIMIT 4
        """, (store,)
    )

    rows=cursor.fetchall()
    conn.close()

    if len(rows)<2:
        return 0
    
    latest=rows[0][0]
    prev=rows[1][0]

    trend=latest-prev

    print("TREND:",trend)

    return trend

def time_factor():
    today=datetime.datetime.today()

    # Weekend boost 
    if today.weekday()>=4:
        return 1.05

    return 0.1

@router.post("/predict")
def predict(data:dict):

    try:
        features=data.get("features",[])
    
        if not features:
            return{
                "error":"No input features provided",
                "status":"failed"
            }
        
        # Convert to numpy
        features_array=np.array([features])
        print("MAPPED FEATURES:",features)

        X=[[features.get(col,0) for col in FEATURE_ORDER]]

        print("FINAL FEATURES SENT TO MODEL:",X)
        print("TOTAL FEATURES COUNT:",len(X[0]))

        # Predict
        prediction=model.predict(X)[0]

        trend=get_recent_trend(features["store"],features["department"])
        prediction=prediction+(0.3*trend)

        prediction=prediction*time_factor()

        print("FINAL PREDICTION",prediction)

        return round(prediction,2)

        #return {
         #   "input":features,
          #  "prediction":float(prediction),
           # "model":"final_model_production",
            #"status":"success"
        #}

    except Exception as e:
        return {
            "error":str(e),
            "status":"failed"
        }