from sqlalchemy import create_engine
import os

def create_pg_table(schema_file, **kwargs):
    """Creates a table using SQLAlchemy's create_engine with Airflow env var."""
    try:
        conn_string = os.getenv("AIRFLOW__DATABASE__SQL_ALCHEMY_CONN")
        if not conn_string:
            raise ValueError("AIRFLOW__DATABASE__SQL_ALCHEMY_CONN environment variable not set")

        # Create SQLAlchemy engine
        engine = create_engine(conn_string)
        
        # Open connection and execute SQL
        with engine.connect() as conn:
            with open(schema_file, 'r') as sql_file:
                sql = sql_file.read()
            conn.execute(sql)

        print("Table created successfully!")

    except Exception as e:
        print(f"Error creating table: {e}")
        raise
