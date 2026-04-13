from fastapi import APIRouter,UploadFile,File
import pandas as pd
from sqlalchemy import create_engine
import os
from backend.scripts.ml.automl_trainer import AutoMLTrainer
from backend.scripts.ml.model_manager import ModelManager

trainer=AutoMLTrainer()
model_manager=ModelManager()

router=APIRouter()

engine=create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

UPLOAD_DIR="uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)

@router.post("/upload-csv")
async def upload_csv(file: UploadFile=File(...)):

    try:
        # Save file locally
        file_path=os.path.join(UPLOAD_DIR,file.filename)

        with open (file_path,"wb") as f:
            f.write(await file.read())

        # Load CSV 
        df=pd.read_csv(file_path)

        # Clean columns names
        df.columns=[c.lower().replace(" ","_") for c in df.columns]

        # Create table name dynamically
        table_name=file.filename.replace(".csv",""  ).lower()

        # Save to PostgreSQL
        df.to_sql(table_name,engine,if_exists="replace",index=False)
        #with self.engine.connect() as conn:
         #   df=pd.read_sql(query,conn)

        # Train AutoML
        model,features=trainer.train(table_name)

        # Set Model
        model_manager.set_automl_model(model,features)

        return{
            "status":"success",
            "table_name":table_name,
            "columns":list(df.columns),
            "rows":len(df),
            "automl":"trained"
        }
    
    except Exception as e:
        return {"error":str(e)}