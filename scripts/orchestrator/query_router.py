from scripts.llm.llm_engine import LLMEngine
from scripts.rag.retrieval import retrieve_context
from scripts.memory.vector_memory import VectorMemory
from scripts.memory.memory_manager import MemoryManager
from scripts.memory.context_builder import build_memory_context
from scripts.utils.error_handler import safe_exectue
from scripts.utils.logger import log
import joblib
from scripts.ml.model_manager import ModelManager
from scripts.ml.feature_extractor import FeatureExtractor
from scripts.ml.feature_store import FeatureStore
from scripts.ml.schema_mapper import SchemaMapper
from scripts.ml.data_collector import DataCollector
from scripts.ml.automl_trainer import AutoMLTrainer
from scripts.ml.feature_formatter import FeatureFormatter

class QueryRouter:

    def __init__(self):
        self.llm=LLMEngine()
        self.memory=MemoryManager()
        self.vector_memory=VectorMemory()

        self.model_manager=ModelManager()
        self.schema_mapper=SchemaMapper()
        self.data_collector=DataCollector()
        self.trainer=AutoMLTrainer()
        self.retrain_threshold=20 
        self.feature_extractor=FeatureExtractor()
        self.feature_store=FeatureStore()
        self.feature_formatter=FeatureFormatter()
        #self.ml_model=joblib.load(r"D:/Projects/CHAITRA/data/Outputs/final_model_production/final_model_production.pkl")

    def run_ml(self,query,user_id="default_user"):
        try:

            # Extract Features
            raw_features=self.feature_extractor.extract(query)
            print("RAW FEATURES:",raw_features)

            # Map shcema -> standard format
            mapped_features=self.schema_mapper.map_features(raw_features)
            print("MAPPED FEATURES:",mapped_features)

            # Safety Check
            if raw_features is None:
                return "ERROR: raw_features is None"
            
            if mapped_features is None:
                return "Error: mapped_features is None"

            if not isinstance (mapped_features,dict):
                return f"ERROR: mapped_features not dict: {mapped_features}"
            
            if len(mapped_features)==0:
                return "ERROR: mapped_features empty"

            # Save features (DB)
            #self.feature_store.save(user_id,query,mapped_features)

            # Convert dict-> list (model input)
            #if not mapped_features:
                #raise ValueError("No Features Extracted")
            
            features=self.feature_formatter.format(mapped_features)

            prediction=self.model_manager.predict(query,features)

            # Save for retraining (simulate target)
            self.data_collector.save(mapped_features,prediction)

            # Check threshold
            #count=self.data_collector.get_count()
            #print("Training data count:",count)

            #if count>= self.retrain_threshold and count % self.retrain_threshold ==0:
                #print("Triggering Auto Retraining...")
                #self.trainer.train()

            return f"Predicted value is {round(prediction,2)} using {mapped_features}"
            
        except Exception as e:
            print("FULL ERROR:",e)
            return f"ML Error:{str(e)}"

    def route(self,query,user_id="default_user",role="user"):
        log (f"Query: {query}")
        print("Query Received:",query)
        
        # Detect Intent
        intent=self.detect_intnet(query)

        # Get Memory
        history=self.memory.get_recent_history(user_id)
        memory_context=build_memory_context(history[:2])
        vector_context=self.vector_memory.search_memory(query)
        
        if intent=="ml_prediction":
            response=self.run_ml(query)

        elif intent=="rag_explanation":
            rag_context=retrieve_context(query)

            clean_context=rag_context[:1000]

            rag_prompt=f"""
            You are CHAITRA, an AI business analyst.

            Use the following business context to answer the question.
            Do NOT include code.
            Do NOT repeat the context.
            Answer in 3–5 lines with clear business insight.

            Context:
            {clean_context}

            Question:
            {query} 
            """

            response=self.llm.generate(rag_prompt)

        else:
            prompt=f"""
            You are CHAITRA , an AI business assistant.

            Answer the question clearly in 3-5 lines.
            Do NOT include code.
            Do NOT repeat instructions.
            
            Question:
            {query}
            """
            response=self.llm.generate(prompt)

        if "import" in response or "model=" in response:
            response="The system detected irrelevant context. Please refine your query."

        log(f"Response: {response}")
        print("Final Response:",response)

        # Save Chat
        self.memory.save_chat(user_id,role,query,response)
        self.vector_memory.add_memory(query,response)

        return response
    
    def detect_intnet(self,query,):
        query=query.lower()
        if "predict" in query or "forecast" in query:
            return "ml_prediction"
        
        if "why" in query or "explain" in query:
            return "rag_explanation"
        
        return "general_llm"