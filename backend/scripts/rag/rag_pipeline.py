def row_to_text(row):
    
    return f"""
Store {row['store']} - Department {row['dept']}

Date: {row['date']}

Weekly Sales: {row['weekly_sales']}

Business Conditions:
Holiday: {row['isholiday']}
Temperature: {row['temperature']}
Fuel Price: {row['fuel_price']}
CPI: {row['cpi']}
Unemployment Rate: {row['unemployment']}

Historical Sales:
Last Week Sales: {row['sales_lag_1']}
4 Week Average Sales: {row['rolling_mean_4']}

Store Statistics:
Store Average Sales: {row['store_avg_sales']}
Department Average Sales: {row['dept_avg_sales']}
"""
    
    return text.strip()

import pandas as pd
from sqlalchemy import create_engine
import psycopg2

engine=create_engine("postgresql://postgres:root64@localhost:5432/chaitra_db")

def load_data():
    conn=psycopg2.connect(
        dbname="chaitra_db",
        user="postgres",
        password="root64",
        host="localhost",
        port="5432"
    )

    query="SELECT * FROM walmart_sales_encoded LIMIT 1000"
    df=pd.read_sql(query,conn)

    conn.close()
    return df

def build_documents(df):
    documents=[]

    for _,row in df.iterrows():
        text=row_to_text(row)
        documents.append(text)

    return documents

if __name__=="__main__":
    df=load_data()
    docs=build_documents(df)

    print("\nSample Document:\n")
    print(docs[0])