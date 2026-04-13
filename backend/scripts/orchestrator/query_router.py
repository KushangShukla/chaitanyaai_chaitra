from backend.routes import query
from backend.scripts.llm.llm_engine import LLMEngine
from backend.scripts.rag.retrieval import retrieve_context
from backend.scripts.memory.vector_memory import VectorMemory
from backend.scripts.memory.memory_manager import MemoryManager
from backend.scripts.memory.context_builder import build_memory_context
from backend.scripts.utils.logger import log

from backend.scripts.ml.model_manager import ModelManager
from backend.scripts.ml.feature_extractor import FeatureExtractor
from backend.scripts.schema_mapper import SchemaMapper
from backend.scripts.schema_mapper import detect_schema
from backend.scripts.ml.data_collector import DataCollector
from backend.scripts.ml.feature_formatter import FeatureFormatter
from backend.scripts.ml.automl_trainer import AutoMLTrainer

from backend.scripts.utils.querry_logger import QueryLogger

import time
import re
import psycopg2

class QueryRouter:

    def __init__(self):
        self.llm = LLMEngine()
        self.memory = MemoryManager()
        self.vector_memory = VectorMemory()

        self.model_manager = ModelManager()
        self.schema_mapper = SchemaMapper()
        self.data_collector = DataCollector()
        self.feature_extractor = FeatureExtractor()
        self.feature_formatter = FeatureFormatter()

        self.trainer = AutoMLTrainer()
        self.retrain_threshold = 20

        self.query_logger = QueryLogger()

    # =========================
    #  ML PIPELINE
    # =========================
        self.table_name="walmart_sales_refined"

        self.columns=[
        "sales_lag_1",
        "sales_lag_2",
        "isholiday",
        "store_sales_ratio",
        "dept_sales_ratio",
        "dept_avg_sales",
        "dept_median_sales",
        "store_median_sales",
        "store_avg_sales",
        "weekly_sales"
    ]

    def route_hybrid_safe(self,query):
        q=query.lower()

        # ML Prediction
        if "predict" in q or "forecast" in q:
            return "ml_prediction"
        
        # SQL Data Lookup
        if any(x in q for x in ["average","avg","max","min","median"]):
            return "data_lookup"
        
        # ML Feature Explanation (New)
        if "feature" in q or "model uses" in q:
            return "ml_explain"
        
        # RAG (DOCUMENTS/WHY)
        if "why" in q or "explain" in q or len(q.split())>8:
            return "rag_explanation"

        # Default
        return "general_llm"
    
    def run_ml(self, query, user_id="default_user", input_type="text"):
        start_time = time.time()

        try:
            # 1. Extract Features
            raw_features = self.feature_extractor.extract(query)
            print("RAW FEATURES:", raw_features)

            mapped_features=self.schema_mapper.map(raw_features)
            print("MAPPED FEATURES BEFORE ENRICH:", mapped_features)

            mapped_features=self.enrich_features_from_db(mapped_features) 
            print("MAPPED FEATURES:", mapped_features)

            # Safety
            if not mapped_features or not isinstance(mapped_features, dict):
                return "Could not extract valid features from query."

            # 2. Format for model
            model_info= self.model_manager.select_model(query)

            model=model_info["model"]
            features_required=model_info["features"]

            features=self.feature_formatter.format(mapped_features,features_required)

            # 3. Prediction
            prediction = model.predict([features])

            # 4. Save training data
            self.data_collector.save(mapped_features, float(prediction))

            # 5. Structured business response
            response = f"""
📊 Key Insight:
Predicted sales value is approximately {round(float(prediction), 2)}.

📈 Recommendation:
Focus on optimizing pricing and demand drivers like CPI and fuel trends.

⚠️ Risk:
External factors like economic shifts may impact prediction accuracy.
"""

            latency = round(time.time() - start_time, 3)

            # 6. Log
            self.query_logger.log({
                "user_id": user_id,
                "query": query,
                "input_type": input_type,
                "mode": "ml",
                "model": "sales_model_v1",
                "features": mapped_features,
                "prediction": float(prediction),
                "response": response,
                "latency": latency
            })

            return response.strip()

        except Exception as e:
            print("FULL ERROR:", e)
            return f"ML Error: {str(e)}"

    # =========================
    #  MAIN ROUTER
    # =========================
    def route(self, query, user_id="default_user", role="user", mode_override=None):

        log(f"Query: {query}")
        print("Query Received:", query)

        response = None

        try:
            intent = self.detect_intent(query)
            if mode_override == "rag":
                intent = "rag_explanation"
            elif mode_override == "llm":
                intent = "general_llm"
            elif mode_override == "ml":
                intent = "ml_prediction"

            # Memory (light)
            history = self.memory.get_recent_history(user_id)
            memory_context = build_memory_context(history[:100])

            intent=self.route_hybrid_safe(query)

            if intent == "data_lookup":
                response = self.run_data_lookup(query)

            if "sales" in query.lower() and "predict" not in query.lower():
                return self.run_data_lookup(query)
            
            if self.is_sql_query(query):
                return "⚠️ Direct SQL queries are not allowed. Please ask in natural language."

            if intent=="ml_explain":
                return """
                The ML model uses the following features:

                - sales_lag_1 (last week sales)
                - sales_lag_2 (2 weeks ago sales)
                - isholiday 
                - store_sales_ratio
                - dept_sa;es_ratio
                - dept_avg_sales
                - dept_median_sales
                - store_median_sales
                - store_avg_sales

                These features are engineered from historical and store-level data.
                """
            
            if "train model" in query.lower() or "automl" in query.lower():
                return self.run_automl("your_uploaded_table")

            # ================= ML =================
            if intent == "ml_prediction":
                response = self.run_ml(query, user_id)

            # ================= RAG =================
            #elif intent == "rag_explanation" or len(query.split()) > 8:

            rag_context = retrieve_context(query)[:800]
            print("RAG CONTEXT:",rag_context)
            if rag_context and "No RAG data" not in rag_context:
                prompt = f"""
You are CHAITRA, a practical business analyst assistant.
Answer only from uploaded document.
Answer ONLY using the provided context.
Do NOT guess or hallucinate.
Use the context and answer the question in plain text.
Give a complete and factual answer. Avoid emojis and template labels.

Context:
{rag_context}

Question:
{query}

Answer:
"""

                response = self.llm.generate(prompt)

            # ================= LLM =================
            else:
                prompt = f"""
You are CHAITRA, a helpful assistant.
Answer clearly in plain text with full details when needed.
Do not use templates, emojis, or repeated labels.

Question:
{query}

Answer:
"""

                response = self.llm.generate(prompt)

        except Exception as e:
            print("ROUTER ERROR:", e)
            response = f"System error: {str(e)}"

        # Fallback
        if not response or len(response.strip()) < 5:
            response = "I couldn't generate a proper answer. Try again."

        response = self.sanitize_response(response)

        # Clean unwanted outputs
        if any(x in response for x in ["import", "def", "class"]):
            response = "Invalid model output detected. Please retry."

        log(f"Response: {response}")
        print("Final Response:", response)

        # Save memory
        self.memory.save_chat(user_id, role, query, response)
        self.vector_memory.add_memory(query, response)

        return response

    def sanitize_response(self, text):
        cleaned = (text or "").strip()
        if not cleaned:
            return cleaned

        # Collapse excessive whitespace
        cleaned = re.sub(r"\s+", " ", cleaned)

        # Remove repeated template artifacts from model drift
        artifacts = [
            "🔍 Question:",
            "💡 Solution:",
            "📖 Example:",
            "📝 Answer:",
        ]
        for token in artifacts:
            if cleaned.count(token) > 1:
                first_idx = cleaned.find(token)
                if first_idx != -1:
                    # keep first section only for this repeated token pattern
                    second_idx = cleaned.find(token, first_idx + len(token))
                    if second_idx != -1:
                        cleaned = cleaned[:second_idx].strip()

        # Safety cap for extreme runaway generations
        if len(cleaned) > 3500:
            cleaned = cleaned[:3500].rstrip() + "..."

        # If output is mostly template noise, force clean fallback
        noise_tokens = ["💡", "📖", "📝", "🔍", "Best Practice", "Case Study", "Next Steps"]
        if sum(1 for t in noise_tokens if t in cleaned) >= 3:
            return "I can answer this, but the model output was noisy. Please ask again in one short sentence."

        return cleaned
    
    def enrich_features_from_db(self, mapped_features):

        try:
            conn=psycopg2.connect(
                dbname="chaitra_db",
                user="postgres", 
                password="root64",
                host="localhost",
                port="5432"
            )
            
            cursor=conn.cursor()

            store=int(mapped_features.get("store", 1))

            dept=int(mapped_features.get("department", 1))

            # Fetch REAL contextual features from DB based on store and department
            cursor.execute(
                """
                SELECT sales_lag_1,sales_lag_2,isholiday,store_sales_ratio, dept_sales_ratio, dept_avg_sales, dept_median_sales,
                store_median_sales, store_avg_sales
                FROM walmart_sales_refined
                LIMIT 1
                """,
                (store, dept)
            )
            row=cursor.fetchone()

            conn.close()

            if row:
                keys=[
                    "sales_lag_1",
                    "sales_lag_2",
                    "isholiday",
                    "store_sales_ratio",
                    "dept_sales_ratio",
                    "dept_avg_sales",
                    "dept_median_sales",
                    "store_median_sales",
                    "store_avg_sales"   
                ]
                for i, key in enumerate(keys):
                    mapped_features[key]=float(row[i] or 0)

                    print("ENRICHED FEATURES:",mapped_features)

        except Exception as e:
            print("DB ENRICHMENT ERROR:", e)    
        return mapped_features
             

    def get_table_schema(self, table_name="walmart_sales_refined"):

        conn=psycopg2.connect(
            dbname="chaitra_db",
            user="postgres",
            password="root64",
            host="localhost",
            port="5432"
        )

        cursor=conn.cursor()

        cursor.execute(
            """
            SELECT column_name FROM information_schema.columns
            WHERE table_name='(walmart_sales_refined)'
            """)
        
        columns=[row[0] for row in cursor.fetchall()]
        conn.close()

        return columns
    
    
    def map_column(self,query):

        query=query.lower()

        # Normalize variations
        query=query.replace("week's","week")
        query=query.replace("weeks","week")
        query=query.replace("holiday","isholiday")
        query=query.replace("_"," ")
        query=query.replace("-"," ")

        mapping={
            "sales last week":"sales_lag_1",
            "last week sales":"sales_lag_1",
            "previous_week_sales":"sales_lag_1",

            "sales 2 week":"sales_lag_2",
            "sales two week":"sales_lag_2",
            "sales 2 weeks ago":"sales_lag_2",

            "is holiday":"isholiday",
            "holiday":"isholiday",

            "store sales ratio":"store_sales_ratio",

            "department sales ratio":"dept_sales_ratio",

            "department average sales":"dept_avg_sales",
            "dept avg sales":"dept_avg_sales",

            "dept median sales":"dept_median_sales",
            "department median sales":"dept_median_sales",

            "store median sales":"store_median_sales",

            "store average sales":"store_avg_sales",

            "weekly sales":"weekly_sales"
        }

        for k,v in mapping.items():
            if k in query:
                return v
        return None
    
    def detect_operation(self,query):
        
        query=query.lower()

        if "average" in query or "avg" in query:
            return "avg"
        
        if "max" in query or "highest" in query:
            return "max"

        if "min" in query or "lowest" in query:
            return "min"

        if "median" in query:
            return "median"
        
        if "show" in query or "list" in query or "display" in query:
            return "select"
        
        return "select"
    
    def build_sql(self,query):
        
        column=self.map_column(query)
        operation=self.detect_operation(query)

        if not column:
            return None, "Could not identify a valid column in the query."
            
        table=self.table_name

        if operation == "avg":
            sql=f"SELECT AVG({column}) FROM {table};"

        elif operation == "max":
            sql=f"SELECT MAX({column}) FROM {table};"

        elif operation == "min":  
            sql=f"SELECT MIN({column}) FROM {table};"
        
        elif operation == "median":
            sql=f"""SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {column}) FROM {table};"""

        else:
            sql=f"SELECT {column} FROM {table} LIMIT 10;"
        return sql, None
    
    def is_sql_query(self, query):

        sql_keywords = [
        "select", "insert", "update", "delete",
        "drop", "alter", "truncate"
    ]
        q = query.lower()

        return any(word in q for word in sql_keywords)
    
    def execute_sql(self,sql):

        try:
            conn=psycopg2.connect(
                dbname="chaitra_db",
                user="postgres",
                password="root64",
                host="localhost",
                port="5432"
            )

            cursor=conn.cursor()
            cursor.execute(sql)

            if "avg" in sql.lower() or "max" in sql.lower() or "min" in sql.lower() or "percentile_cont" in sql.lower():    
                result=cursor.fetchone()
            else:
                result=cursor.fetchall()

            conn.close()

            return result,None
    
        except Exception as e:
            return None, f"SQL Error: {str(e)}"

    def run_data_lookup(self, query):
    
        table_name="walmart_sales_refined"

        sql, error = self.build_sql(query)

        if error:
            return error
        
        print("Final SQL:", sql)

        # Execute 
        result,err= self.execute_sql(sql)

        if err:
            return f"SQL Error: {err}"
        
        if not result:
            return "No data found."
        
        if isinstance(result, tuple):
            value=result[0]
        else:
            value=result[0][0]

        if value is None:
            return "No data available for this query."
        return f"""
        Key Insight:
        Result is {round(float(value), 2)}

        Recommendation:
        Use this metric for analysis.

        Risk:
        Single metric may not reflect full distribution.
        """

    def format_sql_response(self, columns,result):

        # Take first few rows (preview)
        preview=result[:10]

        response="\n Key Insights:\n"

        for row in preview:
            row_text=" , ".join(
                f"{columns[i]}: {row[i]}" for i in range(len(columns))
            )
            response+=f"- {row_text}\n"

            response+="\n Recommendation: \nUse filters for deeper insights."

            response+="\n\n Risk: \nLarge datasets may require aggregation."

            return response
        
    def run_automl(self,table_name):

        try:
            print("Running AutoMl on:", table_name)

            model, features = self.trainer.train(table_name)

            # Set Model
            self.model_manager.set_automl_model(model, features)

            return f"""
            AutoML Training Complete.

            Model trained on {table_name}
            Features used: {features}

            You can now ask predictions on this dataset.
            """

        except Exception as e:
            print(f"AutoML Error: {str(e)}")

    # =========================
    #  INTENT DETECTION
    # =========================
    def detect_intent(self, query):

        q = query.lower()

        # ML
        if "predict" in q or "forecast" in q:
            return "ml_prediction"

        # RAG
        if "why" in q or "reason" in q or "explain" in q:
            return "rag"

        
        return "llm"