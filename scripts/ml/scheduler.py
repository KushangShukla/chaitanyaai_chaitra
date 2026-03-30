import time
from scripts.ml.automl_trainer import AutoMLTrainer

trainer=AutoMLTrainer()

while True:
    print("Running scheduled retraining...")
    trainer.train()

    # run every 24 hours
    time.sleep(86400)