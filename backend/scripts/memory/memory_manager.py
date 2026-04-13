import psycopg2

class MemoryManager:
    
    def __init__(self):
        self.conn=psycopg2.connect(
            dbname="chaitra_db",
            user="postgres",
            password="root64",
            host="localhost",
            port="5432"
        )
        self.cursor=self.conn.cursor()

    def save_chat(self,user_id,role,query,response):
        self.cursor.execute(
            """
            INSERT INTO chat_history (user_id,role,query,response)
            VALUES (%s,%s,%s,%s)
            """,
            (user_id,role,query,response)
        )
        self.conn.commit()

    def get_recent_history(self,user_id,limit=5):
        self.cursor.execute(
            """
            SELECT query,response FROM chat_history
            WHERE user_id=%s
            ORDER BY timestamp DESC
            LIMIT %s
            """,
            (user_id,limit)
        )
        return self.cursor.fetchall()