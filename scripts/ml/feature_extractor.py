import re

class FeatureExtractor:

    def extract(self,query):

        query=query.lower()
        features={}

        # Store
        store_match=re.search(r"store\s*(\d+)",query)
        if store_match:
            features["store"]=int(store_match.group(1))

        # Fuel Price
        fuel_match=re.search(r"fuel\s*price\s*(\d+\.?\d*)",query)
        if fuel_match:
            features["fuel_price"]=float(fuel_match.group(1))

        # CPI
        cpi_match=re.search(r"cpi\s*(\d+\.?\d*)",query)
        if cpi_match:
            features["cpi"]=float(cpi_match.group(1))

        # Default fallback
        if not features:
            features={
                "store":1,
                "fuel_price":2.5,
                "cpi":200
            }

            return features
