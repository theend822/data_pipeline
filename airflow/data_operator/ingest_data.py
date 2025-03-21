import pandas as pd
from sqlalchemy import create_engine

def ingest_data(user, password, host, port, database, file_path, table_name):
    # Database connection
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    
    # Read CSV and load to PostgreSQL
    df = pd.read_csv(file_path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Data ingested into {table_name}")

if __name__ == "__main__":
    # for standalone testing only
    file_path = "..."
    table_name = "..."
    ingest_data(file_path, table_name)