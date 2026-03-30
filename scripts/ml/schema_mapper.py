class SchemaMapper:

    def __init__(self):
        
        # Global Mapping (can be expanded later)
        self.mapping={
            "store":["store","outlet","branch"],
            "fuel_price":["fuel price","petrol","energy cost"],
            "cpi":["cpi","inflation","price index"]
        }

    def map_features(self,raw_features):

        mapped={}

        for standard_key,variations in self.mapping.items():
            for var in variations:
                for key in raw_features:
                    if var in key.lower():
                        mapped[standard_key]=raw_features[key]
                
        return mapped