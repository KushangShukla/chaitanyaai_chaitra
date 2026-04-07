class FeatureFormatter:
    
    def __init__(self):
        #  STRICT ORDER (MUST MATCH TRAINING DATA)
        self.feature_order = [
            "store",
            "dept",
            "temperature",
            "fuel_price",
            "cpi",
            "unemployment",
            "holiday_flag",
            "prev_week_sales",
            "prev_month_sales"
        ]

        #  DEFAULT VALUES (fallback)
        self.default_values = {
            "store": 1,
            "dept": 1,
            "temperature": 25.0,
            "fuel_price": 2.5,
            "cpi": 200.0,
            "unemployment": 7.0,
            "holiday_flag": 0,
            "prev_week_sales": 10000.0,
            "prev_month_sales": 12000.0
        }

    def format(self, mapped_features):

        # 1. Merge with defaults
        final_features = self.default_values.copy()

        for key, value in mapped_features.items():
            if key in final_features:
                try:
                    # Convert safely to float/int
                    final_features[key] = float(value)
                except:
                    final_features[key] = self.default_values[key]

        # 2. Create ordered vector
        feature_vector = [final_features[f] for f in self.feature_order]

        # 3. Debug logs
        print("FINAL FEATURE DICT:", final_features)
        print("FINAL FEATURE VECTOR:", feature_vector)

        return feature_vector