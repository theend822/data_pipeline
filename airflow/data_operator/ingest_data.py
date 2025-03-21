import pandas as pd
from sqlalchemy import create_engine
import os

def ingest_data(file_path, table_name):
    conn_string = os.getenv("AIRFLOW__CORE__SQL_ALCHEMY_CONN")
    if not conn_string:
        raise ValueError("AIRFLOW__CORE__SQL_ALCHEMY_CONN environment variable not set")
    
    # Database connection
    engine = create_engine(conn_string)
    
    # Read CSV and load to PostgreSQL
    df = pd.read_csv(file_path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Data ingested into {table_name}")

if __name__ == "__main__":
    # for standalone testing only
    file_path = "..."
    table_name = "..."
    ingest_data(file_path, table_name)