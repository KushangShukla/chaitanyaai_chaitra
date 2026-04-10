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

    if features.get("sales_lag_1",0) > 0:
        score +=30

    if features.get("sales_lag_2",0) > 0:
        score +=20

    if features.get("dept_avg_sales",0) > 0:
        score +=20
    
    if features.get("store_avg_sales",0) > 0:
        score +=20

    if features.get("isholiday") is not None:
        score +=10

    return min(score,100)

def explain_prediction(features):
    explanation=[]

    if features.get("sales_lag_1",0) > 0:
        explanation.append("Recent sales trend is influencing prediction")
    
    if features.get("isholiday") == 1:
        explanation.append("Holiday impact considered")

    if features.get("fuel_price",0) > 2:
        explanation.aooend("High fuel price may reduce demand")

    if features.get("dept_avg_sales",0) > 0:
        explanation.append("Department performance considered")
    
    return explanation


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

        confidence=get_confidence(features)
        
        explanation=explain_prediction(features)

        return{
            "prediction":round(prediction,2),
            "confidence":confidence,
            "explanation":explanation
        }
    
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