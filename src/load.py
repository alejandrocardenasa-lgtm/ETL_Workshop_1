def load(engine, dim_candidate, dim_date, dim_seniority, dim_technology, fact_applications):

    # Save processed data as CSV files (backup / validation)
    dim_candidate.to_csv("data/processed/dim_candidate.csv", index=False)
    dim_date.to_csv("data/processed/dim_date.csv", index=False)
    dim_seniority.to_csv("data/processed/dim_seniority.csv", index=False)
    dim_technology.to_csv("data/processed/dim_technology.csv", index=False)
    fact_applications.to_csv("data/processed/fact_applications.csv", index=False)

    print("Processed CSVs saved to data/processed/")

    # Load dimension tables into the Data Warehouse
    dim_candidate.to_sql("dim_candidate", engine, if_exists="append", index=False)
    dim_date.to_sql("dim_date", engine, if_exists="append", index=False)
    dim_seniority.to_sql("dim_seniority", engine, if_exists="append", index=False)
    dim_technology.to_sql("dim_technology", engine, if_exists="append", index=False)

    # Load fact table (after dimensions)
    fact_applications.to_sql("fact_applications", engine, if_exists="append", index=False)


    print("Load done: dimensions + fact inserted into DW.")