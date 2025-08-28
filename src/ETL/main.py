import pandas as pd
from transform import transform_data
from load import load_to_mysql   

def extract(file_path):
    df = pd.read_csv(file_path, sep=';', engine='python')
    return df

def main():
    # Extract
    file_path = "data/candidates.csv"
    df = extract(file_path)
    print("==== RAW DATA ====")
    print(df.head())

    # Transform
    tables = transform_data(df)

    # Load 
    load_to_mysql(
        tables=tables,
        host="localhost",   
        user="root",        
        password="root",   
        database="selection_dw"  
    )

if __name__ == "__main__":   
    main()
