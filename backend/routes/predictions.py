from fastapi import APIRouter
import psycopg2
import numpy as np
from scripts.ml.model_manager import ModelManager
from scripts.services.llm_service import llm_service

router = APIRouter()

model_manager = ModelManager()

#  Load LLM once
try:
    llm_service.load()
except:
    pass


# ================= RULE-BASED EXPLANATION =================
def enrich_prediction(features):
    explanation = []

    if features.get("sales_lag_1", 0) > features.get("sales_lag_2", 0):
        explanation.append("Recent upward trend detected")

    else:
        explanation.append("Recent downward trend detected")

    if features.get("store_avg_sales", 0) > features.get("dept_avg_sales", 0):
        explanation.append("Store-level performance is strong")
    else:
        explanation.append("Department-level variation is impacting sales")

    return explanation


@router.get("/predictions")
def get_predictions():

    conn = psycopg2.connect(
        dbname="chaitra_db",
        user="postgres",
        password="root64",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    try:
        # ================= DB =================
        cursor.execute("""
            SELECT 
                "Store",
                "Dept",
                sales_lag_1,
                sales_lag_2,
                store_avg_sales,
                dept_avg_sales
            FROM walmart_sales_refined
            LIMIT 5
        """)

        rows = cursor.fetchall()

        predictions = []

        for i, r in enumerate(rows):

            features = {
                "store": r[0],
                "department": r[1],
                "sales_lag_1": r[2],
                "sales_lag_2": r[3],
                "store_avg_sales": r[4],
                "dept_avg_sales": r[5],
            }

            # ================= ML PREDICTION =================
            try:
                pred = model_manager.predict(features)

                if pred is None:
                    raise Exception("AutoML not available")

            except:
                try:
                    pred = 10000 + (features["sales_lag_1"] or 0)
                except:
                    pred = 10000

            # ================= CONFIDENCE =================
            confidence = min(100, int(
                (features["sales_lag_1"] > 0) * 30 +
                (features["sales_lag_2"] > 0) * 20 +
                (features["store_avg_sales"] > 0) * 25 +
                (features["dept_avg_sales"] > 0) * 25
            ))

            # ================= RULE EXPLANATION =================
            explanation = enrich_prediction(features)

            # ================= LLM (phi-2) =================
            try:
                prompt = f"""
                Prediction: {pred}
                Confidence: {confidence}
                Features: {features}

                Explain this prediction in business-friendly terms:
                """

                llm_text = llm_service.generate(prompt)

            except Exception as e:
                print("LLM failed:", e)
                llm_text = " ".join(explanation)  # fallback

            predictions.append({
                "id": i,
                "prediction": float(pred),
                "confidence": confidence,
                "explanation": explanation,
                "llm_explanation": llm_text,
                "query": f"Store {r[0]} Dept {r[1]}"
            })

        # ================= KPI =================
        values = [p["prediction"] for p in predictions]

        return {
            "kpis": {
                "avg_prediction": round(np.mean(values), 2) if values else 0,
                "total_predictions": len(predictions)
            },
            "predictions": predictions
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()