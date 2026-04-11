from fastapi import APIRouter 
import psycopg2

router=APIRouter()

@router.get("/insights")
def get_insights():

    conn=psycopg2.connect(
        dbname="chaitra_db",
        user="postgres",
        password="root64",
        host="localhost",
        port="5432"
    )

    cursor=conn.cursor()

    # Get latest stats
    cursor.execute("""
    SELECT 
        AVG(sales_lag_1),
        AVG(sales_lag_2),
        AVG(store_sales_ratio),
        AVG(dept_sales_ratio),
        AVG(weekly_sales)
    FROM walmart_sales_refined
    """)

    lag1,lag2,store_ratio,dept_ratio,avg_sales=cursor.fetchone()

    cursor.close()
    conn.close()

    insights=[]

    # Dynamic Insights
    trend=(lag1 or 0) - (lag2 or 0)

    if trend > 0:
        insights.append("Sales momentum is increasing")
    else:
        insights.append("Sales momentum is declining")
    
    if store_ratio > dept_ratio:
        insights.append("Store-level performance is stronger than departement-level")
    else:
        insights.append("Department variations are impacting overall sales")
    if avg_sales > 20000:
        insights.append("Sales are below-optimal-consider improvements")
    else:
        insights.append("Sales are below optimal-consider improvements")
    
    return {"insights":insights}