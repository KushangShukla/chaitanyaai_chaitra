import joblib
import numpy as np

class ModelManager:
    
    def __init__(self):

        self.models = {
            "refined": {
                "model": joblib.load("D:/Projects/CHAITRA/data/Outputs/final_model_production/final_model_production.pkl"),
                "features": [
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
            },

            "ml_ready": {
                "model": joblib.load("D:/Projects/CHAITRA/data/Outputs/hyperparameter_tuning/final_model_week5_tuned.pkl"),
                "features": [
                    "store",
                    "dept",
                    "week",
                    "cpi",
                    "temperature",
                    "unemployment",
                    "isholiday",
                    "size"
                ]
            }
        }

        # AutoML Model (Dynamic)
        self.automl_model=None

    def set_automl_model(self,model,features):
        self.automl_model={
            "model":model,
            "features":features
        }

    def select_model(self,query):
        q=query.lower()

        # Prioriry -> AutoML if exists
        if self.automl_model:
            return self.automl_model 

        # Advanced queries -> refined model
        if "lag" in q or "trend" in q:
            return self.models["refined"]
            
        # Default -> ml_ready model
        return self.models["ml_ready"]

    def format(self, mapped_features, feature_list):
    
        final = {}
        
        for f in feature_list:
            try:
                final[f] = float(mapped_features.get(f, 0))
            except:
                final[f] = 0

        feature_vector = [final[f] for f in feature_list]

        print("DYNAMIC FEATURES:", final)
        print("FEATURE VECTOR:", feature_vector)

        return feature_vector