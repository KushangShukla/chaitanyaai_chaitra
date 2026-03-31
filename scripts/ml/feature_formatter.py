class FeatureFormatter:

    def format(self,mapped_features):

        feature_vector={
            "store":1,
            "dept":1,
            "temperature":25,
            "fuel_price":2.5,
            "cpi":200,
            "unemployment":7,
            "holiday_flag":0,
            "prev_week_sales":10000,
            "prev_month_sales":12000
        }

        # Override with extracted features
        for key in mapped_features:
            if key in feature_vector:
                feature_vector[key]=mapped_features[key]
        
        return list(feature_vector.values())