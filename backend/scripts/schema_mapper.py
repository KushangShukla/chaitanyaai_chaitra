def detect_schema(df):

    mapping={}

    for col in df.columns:
        col_lower=col.lower()
        if "sales" in col_lower:
            mapping["target"]=col
        elif "date" in col_lower:
            mapping["date"]=col
        elif "store" in col_lower:
            mapping["store"]=col
        elif "dept" in col_lower or "category" in col_lower:
            mapping["dept"]=col
        
        print("Detected Schema:",mapping)
        return mapping
    
def standardize(df,mapping):

    df_std=df.copy()

    rename_map={}

    if "target" in mapping:
        rename_map[mapping["target"]]="weekly_sales"
    
    if "date" in mapping:
        rename_map[mapping["date"]]="date"
    
    if "store" in mapping:
        rename_map[mapping["store"]]="store"

    if "dept" in mapping:
        rename_map[mapping["dept"]]="dept"

    df_std.rename(columns=rename_map,inplace=True)

    return df_std

# For ML Query Pipeline
class SchemaMapper:
    def map(self,raw_features):
        mapped={}

        # Default-safe mapping

        mapped["store"]=int(raw_features.get("Store",1))
        mapped["department"]=int(raw_features.get("department",1))

        # External Factors
        mapped["fuel_price"]=float(raw_features.get("fuel_price",2.5))
        mapped["cpi"]=float(raw_features.get("cpi",200))

        return mapped