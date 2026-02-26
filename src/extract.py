import pandas as pd
 
"""
Extract Phase:
 - Load CSV file
 - Validate data types
 """
def extract(file_path):
    # Load CSV
    df = pd.read_csv(file_path, sep=";")

    # Remove extra spaces in column names
    df.columns = df.columns.str.strip()
   
    # Validate data types
    df["Application Date"] = pd.to_datetime(df["Application Date"])
    df["YOE"] = df["YOE"].astype(int)
    df["Code Challenge Score"] = df["Code Challenge Score"].astype(float)
    df["Technical Interview Score"] = df["Technical Interview Score"].astype(float)

    print("Data types after validation:\n")
    print(df.dtypes)

    return df