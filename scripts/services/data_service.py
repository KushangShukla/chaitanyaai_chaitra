import psycopg2
from scripts.ml.model_manager import ModelManager

model_manager=ModelManager()

def get_db_connection():
    return psycopg2.connect(
        dbname="chitra_db",
        user="postgres",
        password="root64",
        host="localhost",
        port="5432"
    )

def get_core_data():
    conn=get_db_connection()
    cursor=conn.cursor()

    cursor.execute("""
    SELECT 
        AVG(weekly_sales),
        MAX(weekly_sales),
        MIN(weekly_sales),
        COUNT(*),
        AVG(sales_lag_1),
        AVG(sales_lag_2), 
        AVG(store_sales_ratio),
        AVG(dept_sales_ratio),
        AVG(store_avg_sales),
        AVG(dept_avg_sales)
    FROM walmart_sales_refined   
    """)

    row=cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None
    
    return {
        "avg_sales":row[0],
        "max_sales":row[1],
        "min_sales":row[2],
        "total_records":row[3],
        "lag1":row[4],
        "lag2":row[5],
        "store_ratio":row[6],
        "dept_ratio":row[7],
        "store_avg":row[8],
        "dept_avg":row[9],
    }

# Shared Insight Engine

def generate_insights(data):
    insights=[]

    trend=(data["lag1"] or 0) - (data["lag2"] or 0)

    if trend > 0:
        insights.append("Sales momentum increasing")
    else:
        insights.append("Sales momentum declining")

    if data ["store_ratio"] > data["dept_ratio"]:
        insights.append("Store dominates performance")
    else:
        insights.append("Department variation is high")
    
    if data["avg_sales"] > 20000:
        insights.append("Strong revenue performance")
    else:
        insights.append("Revenue below optimal")

    return insights

# Shared Prediction Engine
def generate_prediction(data):
    features={
        "store":1,
        "department":1,
        "sales_lag_1":data["lag1"],
        "sales_lag_2":data["lag2"],
        "store_avg_sales":data["store_avg"],
        "dept_avg_sales":data["dept_avg"],
    }

    pred=model_manager.predict(features)

    return pred or data ["avg_sales"]
