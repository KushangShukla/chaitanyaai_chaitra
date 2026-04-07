import joblib
import numpy as np


class ModelManager:

    def __init__(self):
        # Load models
        self.models = {
            "sales": joblib.load(
                r"D:/Projects/CHAITRA/data/Outputs/final_model_production/final_model_production.pkl"
            ),
        }

        # Expected feature size (IMPORTANT)
        self.expected_features = 9

    # =========================
    #  MODEL SELECTION
    # =========================
    def select_model(self, query):
        query = query.lower()

        if "sales" in query or "revenue" in query or "forecast" in query:
            return self.models["sales"]

        return self.models["sales"]

    # =========================
    #  FEATURE SAFETY FIX
    # =========================
    def validate_features(self, features):
        print("MODEL INPUT FEATURES:", features)

        if not isinstance(features, (list, tuple, np.ndarray)):
            raise ValueError("Features must be a list or array")

        # Fix feature size mismatch
        if len(features) < self.expected_features:
            # pad with zeros
            features = list(features) + [0] * (self.expected_features - len(features))

        elif len(features) > self.expected_features:
            # trim extra
            features = features[:self.expected_features]

        print("FINAL FEATURES USED:", features)

        return features

    # =========================
    #  PREDICTION
    # =========================
    def predict(self, query, features):
        try:
            model = self.select_model(query)

            features = self.validate_features(features)

            prediction = model.predict([features])[0]

            return float(prediction)

        except Exception as e:
            print("MODEL ERROR:", e)
            raise e