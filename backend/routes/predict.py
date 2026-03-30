from fastapi import APIRouter
import joblib
import numpy as np

router=APIRouter()

# Load trained model
model=joblib.load(r"D:/Projects/CHAITRA/data/Outputs/final_model_production/final_model_production.pkl")

@router.post("/predict")
def predict(data:dict):

    try:
        features=data.get("features",[])
    
        if not features:
            return{
                "error":"No input features provided",
                "status":"failed"
            }
        
        # Convert to numpy
        features_array=np.array([features])

        # Predict
        prediction=model.predict(features_array)[0]

        return {
            "input":features,
            "prediction":float(prediction),
            "model":"final_model_production",
            "status":"success"
        }

    except Exception as e:
        return {
            "error":str(e),
            "status":"failed"
        }