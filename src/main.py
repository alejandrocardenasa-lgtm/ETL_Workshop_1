from extract import extract
from transform import transform
from logs import log_progress
from load import load
from sqlalchemy import create_engine

def main():

    log_progress("ETL process started")

    # --- Extract ---
    log_progress("Extract phase started")
    file_path = "data/raw/candidates.csv"  # Path to raw CSV
    df = extract(file_path)
    log_progress("Extract phase completed")

    # --- Transform ---
    log_progress("Transform phase started")
    dim_candidate, dim_date, dim_seniority, dim_technology, fact_applications = transform(df)
    log_progress("Transform phase completed")

    # --- Load ---
    
    log_progress("Load phase started")
    engine = create_engine("mysql+pymysql://root:root@localhost/dw_candidates")
    load(engine, dim_candidate, dim_date, dim_seniority, dim_technology, fact_applications) 
    log_progress("Load phase completed")

    log_progress("ETL process finished")

if __name__ == "__main__":
    main()