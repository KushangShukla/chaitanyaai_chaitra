import psycopg2
import json
import joblib
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

class AutoMLTrainer:

    def __init__(self):
        self.conn=psycopg2.connect(
            dbname="chaitra_db",
            user="postgres",
            password="root64",
            host="localhost",
            port="5432"
        )

    def load_data(self):

        query="SELECT features, target FROM training_data"
        df=pd.read_sql(query,self.conn)

        if df.empty:
            return None,None
        
        X=df["features"].apply(json.loads).apply(lambda x: list(x.values()))
        X=pd.DataFrame(X.tolist())

        y=df["target"]

        return X,y
    
    def train(self):

        X,y=self.load_data()

        if X is None:
            print("No training data available")
            return
        
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

            return best_model,list(X.columns)