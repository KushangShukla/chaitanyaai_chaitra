import re

class FeatureExtractor:

    def extract(self,query):

        query=query.lower()
        features={}

        # Store/outlet/branch
        match=re.search(r"(store|outlest|branch)\s*(\d+)",query)
        if match:
            features[match.group(1)]=int(match.group(2))

        # Fuel Price/petrol
        match=re.search(r"(fuel price|petrol|energy cost)\s*(\d+\.?\d*)",query)
        if match:
            features[match.group(1)]=float(match.group(2))

        # CPI/inflation
        match=re.search(r"(cpi|inflation|price index)\s*(\d+\.?\d*)",query)
        if match:
            features[match.group(1)]=float(match.group(2))

        # Default fallback
        if not features:
            features={
                "store":1,
                "fuel_price":2.5,
                "cpi":200
            }

        return features
