from scripts.llm.llm_engine import LLMEngine
from scripts.rag.retrieval import retrieve_context
from scripts.memory.vector_memory import VectorMemory
from scripts.memory.memory_manager import MemoryManager
from scripts.memory.context_builder import build_memory_context
from scripts.utils.logger import log

from scripts.ml.model_manager import ModelManager
from scripts.ml.feature_extractor import FeatureExtractor
from scripts.ml.schema_mapper import SchemaMapper
from scripts.ml.data_collector import DataCollector
from scripts.ml.feature_formatter import FeatureFormatter
from scripts.ml.automl_trainer import AutoMLTrainer

from scripts.utils.querry_logger import QueryLogger

import time
import re


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
    def run_ml(self, query, user_id="default_user", input_type="text"):
        start_time = time.time()

        try:
            # 1. Extract Features
            raw_features = self.feature_extractor.extract(query)
            print("RAW FEATURES:", raw_features)

            mapped_features = self.schema_mapper.map_features(raw_features)
            print("MAPPED FEATURES:", mapped_features)

            # Safety
            if not mapped_features or not isinstance(mapped_features, dict):
                return "Could not extract valid features from query."

            # 2. Format for model
            features = self.feature_formatter.format(mapped_features)

            # 3. Prediction
            prediction = self.model_manager.predict(query, features)

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
            memory_context = build_memory_context(history[:2])

            # ================= ML =================
            if intent == "ml_prediction":
                response = self.run_ml(query, user_id)

            # ================= RAG =================
            elif intent == "rag_explanation" or len(query.split()) > 8:

                rag_context = retrieve_context(query)[:800]

                prompt = f"""
You are CHAITRA, a practical business analyst assistant.
Use the context and answer the question in plain text.
Keep the answer concise, factual, and avoid bullet emojis.

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
Answer clearly in plain text using 2-4 short sentences.
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

        response = self._sanitize_response(response)

        # Clean unwanted outputs
        if any(x in response for x in ["import", "def", "class"]):
            response = "Invalid model output detected. Please retry."

        log(f"Response: {response}")
        print("Final Response:", response)

        # Save memory
        self.memory.save_chat(user_id, role, query, response)
        self.vector_memory.add_memory(query, response)

        return response

    def _sanitize_response(self, text):
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

        # Hard cap overly long noisy generations
        if len(cleaned) > 900:
            cleaned = cleaned[:900].rstrip() + "..."

        # If output is mostly template noise, force clean fallback
        noise_tokens = ["💡", "📖", "📝", "🔍", "Best Practice", "Case Study", "Next Steps"]
        if sum(1 for t in noise_tokens if t in cleaned) >= 3:
            return "I can answer this, but the model output was noisy. Please ask again in one short sentence."

        return cleaned

    # =========================
    #  INTENT DETECTION
    # =========================
    def detect_intent(self, query):
        query = query.lower()

        if "predict" in query or "forecast" in query:
            return "ml_prediction"

        if "why" in query or "explain" in query:
            return "rag_explanation"

        return "general_llm"