import joblib

class ModelManager:

    def __init__(self):

        # Load Multiple Models
        self.models={
            "sales":joblib.load(
                r"D:/Projects/CHAITRA/data/Outputs/final_model_production/final_model_production.pkl"
            ),

            # Future Models 
            # "demand":joblib.load
            # "customer":joblib.load
        }

    def select_model(self,query):
        query=query.lower()

        if "sales" in query:
            return self.models["sales"]
            
        if "revenue" in query:
            return self.models["sales"]
            
        if "forecast" in query:
            return self.models["Sales"]
            
        # fallback
        return self.models["sales"]

    def predict (self,query,features):
        model=self.select_model(query)

        # Temporary features
        #features=[1,2,3,4,5,6,7,8,9]

        prediction=model.predict([features])[0]

        return prediction
