import pandas as pd
import numpy as np

def transform_data(df):
    
    # Convert dates to datetime
    
    df["application_date"] = pd.to_datetime(df["Application Date"], errors="coerce")

    
    # Hired rule
    
    df["hired"] = (
        (df["Code Challenge Score"] >= 7) &
        (df["Technical Interview Score"] >= 7)
    ).astype(int)

    
    # Create dimension tables
    

    # DimCandidate
    dim_candidate = (
        df[["First Name", "Last Name", "Email", "YOE"]]
        .drop_duplicates(subset=["Email"])
        .reset_index(drop=True)
    )
    dim_candidate["candidate_id"] = dim_candidate.index + 1 

    # DimDate
    dim_date = (
        df[["application_date"]]
        .dropna()
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_date["date_id"] = dim_date.index + 1
    dim_date["day"]   = dim_date["application_date"].dt.day
    dim_date["month"] = dim_date["application_date"].dt.month
    dim_date["year"]  = dim_date["application_date"].dt.year

    # DimCountry
    dim_country = df[["Country"]].drop_duplicates().reset_index(drop=True)
    dim_country["country_id"] = dim_country.index + 1

    # DimTechnology
    dim_tech = df[["Technology"]].drop_duplicates().reset_index(drop=True)
    dim_tech["technology_id"] = dim_tech.index + 1

    # DimSeniority
    dim_seniority = df[["Seniority"]].drop_duplicates().reset_index(drop=True)
    dim_seniority["seniority_id"] = dim_seniority.index + 1

    
    # Create fact table
    
    fact_selection = (
        df
        .merge(dim_candidate, on="Email")
        .merge(dim_date, on="application_date")
        .merge(dim_country, on="Country")
        .merge(dim_tech, on="Technology")
        .merge(dim_seniority, on="Seniority")
    )

    fact_selection = fact_selection[[
        "candidate_id", "date_id", "country_id", "technology_id", "seniority_id",
        "Code Challenge Score", "Technical Interview Score", "hired"
    ]].reset_index(drop=True)

    fact_selection["selection_id"] = fact_selection.index + 1  # PK

   
    # Convert numpy types → native int/float
    
    tables = {
        "dim_candidate": dim_candidate,
        "dim_date": dim_date,
        "dim_country": dim_country,
        "dim_technology": dim_tech,
        "dim_seniority": dim_seniority,
        "fact_selection": fact_selection
    }

    for name, df_table in tables.items():
        for col in df_table.select_dtypes(include=["int64", "float64"]).columns:
            df_table[col] = df_table[col].apply(
                lambda x: int(x) if isinstance(x, (np.integer,)) else float(x) if isinstance(x, (np.floating,)) else x
            )
        tables[name] = df_table

    # Control logs
    print("DimCandidate:", dim_candidate.shape)
    print("DimDate:", dim_date.shape)
    print("DimCountry:", dim_country.shape)
    print("DimTechnology:", dim_tech.shape)
    print("DimSeniority:", dim_seniority.shape)
    print("FactSelection:", fact_selection.shape)
    print(f"Raw rows: {len(df)} | Fact rows: {len(fact_selection)}")

    return tables