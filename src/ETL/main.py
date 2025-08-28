import pandas as pd
from transform import transform_data
from load import load_to_mysql   

# Function to extract raw data from a CSV file
def extract(file_path):
    df = pd.read_csv(file_path, sep=';', engine='python')
    return df

def main():
    # Step 1: Extract
    # Load candidate data from the CSV file
    file_path = "data/candidates.csv"
    df = extract(file_path)
    print("==== RAW DATA ====")
    print(df.head())   # Show first rows to verify the raw data

    # Step 2: Transform
    # Clean and structure the data into dimension and fact tables
    tables = transform_data(df)

    # Step 3: Load
    # Insert transformed tables into the MySQL data warehouse
    load_to_mysql(
        tables=tables,
        host="localhost",   
        user="root",        
        password="root",   
        database="selection_dw"  
    )

# Entry point of the script
if __name__ == "__main__":   
    main()