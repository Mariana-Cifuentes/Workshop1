import mysql.connector
import pandas as pd

# Database Connection

def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="selection_dw"
        )
        if conn.is_connected():
            print("Connection established")
        return conn
    except mysql.connector.Error as e:
        print("Connection error:", e)
        return None


# KPI 1: Hiring Rate

def kpi_hire_rate(conn):
    query = """
        SELECT 
            (SUM(CASE WHEN f.hired = 1 THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS hire_rate
        FROM fact_selection f;
    """
    return pd.read_sql(query, conn)


# KPI 2: Average Scores (Challenge & Interview) by Seniority, only hired

def kpi_avg_scores_hired_by_seniority(conn):
    query = """
        SELECT
            s.seniority,
            AVG(f.code_challenge_score) AS avg_challenge_hired,
            AVG(f.technical_interview_score) AS avg_interview_hired
        FROM fact_selection f
        JOIN dim_seniority s ON f.seniority_id = s.seniority_id
        WHERE f.hired = 1
        GROUP BY s.seniority
        ORDER BY s.seniority;
    """
    return pd.read_sql(query, conn)


# KPI 3: Hires by Technology

def kpi_hires_by_technology(conn):
    query = """
        SELECT 
            t.technology,
            COUNT(*) AS total_hires
        FROM fact_selection f
        JOIN dim_technology t ON f.technology_id = t.technology_id
        WHERE f.hired = 1
        GROUP BY t.technology
        ORDER BY total_hires DESC;
    """
    return pd.read_sql(query, conn)


# KPI 4: Hires by Year

def kpi_hires_by_year(conn):
    query = """
        SELECT 
            d.year,
            COUNT(*) AS total_hires
        FROM fact_selection f
        JOIN dim_date d ON f.date_id = d.date_id
        WHERE f.hired = 1
        GROUP BY d.year
        ORDER BY d.year;
    """
    return pd.read_sql(query, conn)


# KPI 5: Hires by Seniority

def kpi_hires_by_seniority(conn):
    query = """
        SELECT 
            s.seniority,
            COUNT(*) AS total_hires
        FROM fact_selection f
        JOIN dim_seniority s ON f.seniority_id = s.seniority_id
        WHERE f.hired = 1
        GROUP BY s.seniority
        ORDER BY total_hires DESC;
    """
    return pd.read_sql(query, conn)


# KPI 6: Hires by Country

def kpi_hires_by_country(conn):
    query = """
        SELECT 
            c.country,
            d.year,
            COUNT(*) AS total_hires
        FROM fact_selection f
        JOIN dim_country c ON f.country_id = c.country_id
        JOIN dim_date d ON f.date_id = d.date_id
        WHERE f.hired = 1
          AND c.country IN ('USA', 'Brazil', 'Colombia', 'Ecuador')
        GROUP BY c.country, d.year
        ORDER BY d.year, total_hires DESC;
    """
    return pd.read_sql(query, conn)


# MAIN

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        print("\n--- KPI 1: Hiring Rate ---")
        print(kpi_hire_rate(conn))

        print("\n--- KPI 2: Average Scores (Challenge & Interview) by Seniority [only hired] ---")
        print(kpi_avg_scores_hired_by_seniority(conn))

        print("\n--- KPI 3: Hires by Technology ---")
        print(kpi_hires_by_technology(conn))

        print("\n--- KPI 4: Hires by Year ---")
        print(kpi_hires_by_year(conn))

        print("\n--- KPI 5: Hires by Seniority ---")
        print(kpi_hires_by_seniority(conn))

        print("\n--- KPI 6: Hires by Country ---")
        print(kpi_hires_by_country(conn))

        conn.close()