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

    def format(self, mapped_features,feature_required):
    
        formatted={}

        for f in feature_required:
            value=mapped_features.get(f,0)

        #formatted.append(float(value))

        # 3. Debug logs
        print("FINAL FEATURES SENT TO MODEL:", formatted)
        print("TOTAL FEATURES COUNT:", len(formatted))

        return formatted