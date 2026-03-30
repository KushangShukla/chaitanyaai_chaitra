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

class QueryRouter:

    def __init__(self):
        self.llm=LLMEngine()
        self.memory=MemoryManager()
        self.vector_memory=VectorMemory()

        self.model_manager=ModelManager()
        self.model_manager=FeatureExtractor()
        self.model_manager=FeatureStore()
        #self.ml_model=joblib.load(r"D:/Projects/CHAITRA/data/Outputs/final_model_production/final_model_production.pkl")

    def run_ml(self,query,user_id="default_user"):
        try:

            # Extract Features
            features_dict=self.features_extractor.extract(query)

            # Save features (DB)
            self.feature_store.save(user_id,query,features_dict)

            # Convert dict-> list (model input)
            features=list(features_dict.values())

            prediction=self.model_manager.predict(query,features)
            return f"Predicted value is {round(prediction,2)} using features {features_dict}"
            
        except Exception as e:
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
