from scripts.llm.llm_engine import LLMEngine
from scripts.rag.retrieval import retrieve_context
from scripts.memory.vector_memory import VectorMemory
from scripts.memory.memory_manager import MemoryManager
from scripts.memory.context_builder import build_memory_context
from scripts.utils.error_handler import safe_exectue

class QueryRouter:

    def __init__(self):
        self.llm=LLMEngine()
        self.memory=MemoryManager()
        self.vector_memory=VectorMemory()

    def route(self,query,user_id="default_user",role="user"):

        # Get Memory
        history=self.memory.get_recent_history(user_id)
        memory_context=build_memory_context(history)
        vector_context=self.vector_memory.search_memory(query)

        # Decide Pipeline
        if "why" in query.lower() or "explain" in query.lower():
            rag_context=retrieve_context(query)

            final_context=memory_context +"\n" + vector_context + "\n" + rag_context

            response=self.llm.generate_rag_response(final_context,query)
        
        else:
            prompt=memory_context+"\nQuestion: " +query
            response=self.llm.generate(prompt)

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
    
    def route(self,query):
        intent=self.detect_intnet(query)

        if intent=="rag":
            return safe_exectue(self.rag_engine,query)
        
        if intent=="ml":
            return safe_exectue(self.ml_engine,query)
        
        return safe_exectue(self.llm.engine.generate_business_reponse,query)