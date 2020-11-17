import pandas as pd

bridge_data = "data/staging_data/bridge_df.csv"
taxi_data = "data/staging_data/taxi_df.csv"
zones_data = "data/staging_data/zones_df.csv"

def check(path):
    df = pd.read_csv(path)
    if len(df.columns) > 0  and len(df) > 0:
        print("Data quality in: ", path, " - Check PASSED.",  sep="")
        print("(rows, colums)")
        print(df.shape)
    else:
        print("Data quality checks FAILED.")
        print(path)

check(bridge_data)
check(taxi_data)
check(zones_data)