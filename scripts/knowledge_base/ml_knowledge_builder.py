import pandas as pd
from sqlalchemy import create_engine

DB_URI="postgresql://postgres:root64@localhost:5432/chaitra_db"

def load_ml_data():
    query="""
    SELECT * 
    FROM walmart_sales_encoded
    LIMIT 1000
    """

    df=pd.read_sql(query,DB_URI)
    print("Data loaded:", df.shape)
    return df

def row_to_knowledge(row):

    text=f"""
Store {row['store']} department {row['dept']} recorded sales of {row['weekly_sales']}.

Business conditions included temperature {row['temperature']},
fuel price {row['fuel_price']},
CPI {row['cpi']},
and unemployment rate {row['unemployment']}.

Historical indicators show previous week sales of {row['sales_lag_1']}
and rolling average sales of {row['rolling_mean_4']}.

Store average sales are {row['store_avg_sales']}
while department average sales are {row['dept_avg_sales']}.

These indicators help predict future business performance.
"""
    
    return text

def build_knowledge_documents(df):
    documents=[]

    for _,row in df.iterrows():
        doc=row_to_knowledge(row)
        documents.append(doc)

    return documents

import pickle

def save_documents(documents):
    with open("scripts/rag/ml_knowledge.pkl","wb") as f:
        pickle.dump(documents,f)

    print("Knowledge base saved.")

if __name__=="__main__":
    df=load_ml_data()
    documents=build_knowledge_documents(df)
    save_documents(documents)