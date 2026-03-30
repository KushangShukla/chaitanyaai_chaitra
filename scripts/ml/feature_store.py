import psycopg2
import json

class FeatureStore:

    def __init__(self):
        self.conn=psycopg2.connect(
            dbname="chaitra_db",
            user="postgres",
            password="root64",
            host="localhost",
            port="5432"
        )
        self.cursor=self.conn.cursor()

    def save(self,user_id,query,features):

        self.cursor.execute(
            """
            INSERT INTO extracted_features (user_id,query,features)
            VALUES (%s,%s,%s)           
            """,
            (user_id,query,json.dumps(features))
        )

        self.conn.commit()