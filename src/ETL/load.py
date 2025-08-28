import mysql.connector
from mysql.connector import Error

def load_to_mysql(tables, host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if conn.is_connected():
            print("Successful connection to MySQL")

        cursor = conn.cursor()

        # Table definitions with AUTO_INCREMENT IDs
        table_schemas = {
            "dim_candidate": """
                CREATE TABLE IF NOT EXISTS dim_candidate (
                    candidate_id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(100),
                    last_name VARCHAR(100),
                    email VARCHAR(150),
                    yoe INT
                )
            """,
            "dim_date": """
                CREATE TABLE IF NOT EXISTS dim_date (
                    date_id INT AUTO_INCREMENT PRIMARY KEY,
                    year INT,
                    month INT,
                    day INT,
                    full_date DATE
                )
            """,
            "dim_country": """
                CREATE TABLE IF NOT EXISTS dim_country (
                    country_id INT AUTO_INCREMENT PRIMARY KEY,
                    country_name VARCHAR(100)
                )
            """,
            "dim_technology": """
                CREATE TABLE IF NOT EXISTS dim_technology (
                    technology_id INT AUTO_INCREMENT PRIMARY KEY,
                    technology_name VARCHAR(100)
                )
            """,
            "dim_seniority": """
                CREATE TABLE IF NOT EXISTS dim_seniority (
                    seniority_id INT AUTO_INCREMENT PRIMARY KEY,
                    seniority_name VARCHAR(100)
                )
            """,
            "fact_selection": """
                CREATE TABLE IF NOT EXISTS fact_selection (
                    selection_id INT AUTO_INCREMENT PRIMARY KEY,
                    candidate_id INT,
                    date_id INT,
                    country_id INT,
                    technology_id INT,
                    seniority_id INT,
                    code_challenge_score INT,
                    technical_interview_score INT,
                    hired TINYINT,
                    FOREIGN KEY(candidate_id) REFERENCES dim_candidate(candidate_id),
                    FOREIGN KEY(date_id) REFERENCES dim_date(date_id),
                    FOREIGN KEY(country_id) REFERENCES dim_country(country_id),
                    FOREIGN KEY(technology_id) REFERENCES dim_technology(technology_id),
                    FOREIGN KEY(seniority_id) REFERENCES dim_seniority(seniority_id)
                )
            """
        }

        # Create tables
        for table, schema in table_schemas.items():
            cursor.execute(schema)
            print(f" Table {table} verified/created")

        # Insert data
        for table_name, df in tables.items():
            print(f"Inserting data into {table_name}...")

            df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

            cols = ", ".join([f"`{col}`" for col in df.columns])  
            placeholders = ", ".join(["%s"] * len(df.columns))
            sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

            try:
                cursor.executemany(sql, df.values.tolist())
                conn.commit()
                print(f" {len(df)} rows inserted into {table_name}")
            except Error as e:
                print(f"Error inserting into {table_name}: {e}")

        cursor.close()
        conn.close()
        print("Connection closed")

    except Error as e:
        print("Connection error:", e)