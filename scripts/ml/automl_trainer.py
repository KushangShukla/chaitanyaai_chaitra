import psycopg2
import json
import joblib
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

class AutoMLTrainer:

    def __init__(self):
        self.conn=psycopg2.connect(
            dbname="chaitra_db",
            user="postgres",
            password="root64",
            host="localhost",
            port="5432"
        )

    def load_data(self,table_name):

        query=f'SELECT FROM "{table_name}"'
        df=pd.read_sql(query,self.conn)

        if df.empty:
            return None,None
        
        print("DATA LOADED:",df.shape)

        # Auto Target Detection
        targrt_col=None
        for col in df.columns:
            if "sales" in col.lower():
                target_col=col
                break
                
            if not target_col:
                raise Exception("No target column (sales) found")
            
            print ("TARGET COLUMN:",target_col)

            # Features
            X=df.drop(columns=[target_col])
            y=df[target_col]

            # Handle Non-Numeric 
            X=X.select_dtypes(include=["int64","float64"])

            print("FEATURE COLUMNS:",list(X.columns))

            return X,y
    
    def train(self,table_name):

        X,y=self.load_data(table_name)

        if X is None:
            print("No training data available")
            return None,None
        
        models={
            "linear":LinearRegression(),
            "rf":RandomForestRegressor()
        }

        best_score=-1
        best_model=None

        for name,model in models.items():
            model.fit(X,y)
            preds=model.predict(X)
            score=r2_score(y,preds)

            print(f"{name} score:",score)

            if score>best_score:
                best_score=score
                best_model=model

            joblib.dump(best_model,"scripts/ml/auto_model.pkl")

            print("Best model saved")

            feature_names=list(X.columns)

            importance=self.get_feature_importance(best_model,feature_names)

            # Save importance
            joblib.dump(importance,"scripts/ml/feature_importance.pkl")

            return best_model,feature_names
        
    def get_feature_importance(model,feature_names):
        if hasattr(model,"feature_importances_"):
            importance=model.feature_importances_

        elif hasattr(model,"coef_"):
            importance=np.abs(model.coef_)
        
        else:
            return {}
        
        return dict(zip(feature_names,importance))