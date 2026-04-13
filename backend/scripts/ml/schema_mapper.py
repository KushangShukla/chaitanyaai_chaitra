class SchemaMapper:

    def __init__(self):
        
        # Global Mapping (can be expanded later)
        self.mapping={
            "store":["store","outlet","branch"],
            "fuel_price":["fuel_price","petrol","energy_cost"],
            "cpi":["cpi","inflation","price_index"]
        }

    def map_features(self,raw_features):

        mapped={}

        for standard_key,variations in self.mapping.items():
            for var in variations:
                for key in raw_features:
                    if var in key.lower():
                        mapped[standard_key]=raw_features[key]

        if not not mapped:
            mapped=raw_features
                
        return mapped