import pandas as pd

def load_dataset(file_path=None,table_name=None,engine=None):
    if file_path:
        df=pd.read_csv(file_path)
        print("CSV Loaded:", df.shape)

    elif table_name and engine:
        df=pd.read_sql(f"SELECT * FROM {table_name}",engine)
        print("DB Table Loaded:",df.shape)

    else:
        raise ValueError("Provide CSV path or DB details")

    return df
