import psycopg2 
import json

class DataCollector:

    def __init__(self):
        self.conn=psycopg2.connect(
            dbname="chaitra_db",
            user="postgres",
            password="root64",
            host="localhost",
            port="5432"
        )
        self.cursor=self.conn,self.cursor()

    def save(self,features,target):
        self.cursor.executea(
            """
            INSERT INTO training_data (features,target)
            VALUES (%s,%s)            
            """,
            (json.dumps(features),target)
        )
        self.conn.commit()
