import psycopg2
import json
import time

class QueryLogger:

    def __init__(self):
        self.conn=psycopg2.connect(
            dbname="chaitra_db",
            user="postgres",
            password="root64",
            host="localhost",
            port="5432"
        )
        self.cursor=self.conn.cursor()

    def log(self,data:dict):
        self.cursor.execute(
            """
            INSERT INTO query_logs
            (user_id,query,input_type,mode,model_used,features,prediction,response,latency)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                data["user_id"],
                data["query"],
                data["input_type"],
                data["mode"],
                data["model_used"],
                json.dumps(data["features"]),
                float(data["prediction"]),
                data["response"],
                float(data["latency"])
            )
        )
        self.conn.commit()