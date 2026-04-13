import joblib
import numpy as np
import os
from sqlalchemy import create_engine
import pandas as pd

class AutoMLTrainer:
    def __int__(self):
         self.engine=create_engine(
             "postgresql://postgres:root64@localhost:5432/chaitra_db"
         )
    def load_data(self,table_name):
        query=f'SELECT * FROM "{table_name}"'
        df=pd.read_sql(query,self.engine)
        return df

class ModelManager:
    _instance=None

    # Made Model Manager Singleton so that Model Manager inside upload != Model Manager inside Query Router
    def __new__(cls):
        if cls._instance is None:
            cls._instance=super().__new__(cls)
            cls._instance.models={}
            cls._instance.automl_model=None
        return cls._instance
    
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
        self.feature_importance=None
        self.features=None
    
        # Load AutoML
        self.load_automl()

    def load_automl(self):
        if os.path.exists("scripts/ml/auto_model.pkl"):

            model=joblib.load("scripts/ml/auto_model.pkl")

            if os.path.exists("scripts/ml/feature_importance.pkl"):

                self.feature_importance=joblib.load("scripts/ml/feature_importance.pkl")

                self_features=list(self.feature_importance.keys())

                self.automl_model={
                    "model":model,
                    "features":self_features
                }

    def predict(self,features_dict):
        if not self.automl_model:
            return None
    
        FEATURE_ORDER=self.automl_model["features"]

        X=[[features_dict.get(col,0) for col in FEATURE_ORDER]]

        prediction=self.automl_model["model"].predict(X)[0]

        return prediction

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