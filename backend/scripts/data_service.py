import psycopg2
from backend.scripts.ml.model_manager import ModelManager

model_manager=ModelManager()

def get_db_connection():
    return psycopg2.connect(
        dbname="chaitra_db",
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