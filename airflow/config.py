import os
from dotenv import load_dotenv
from datetime import datetime

run_date = datetime.now().strftime('%Y%m%d') # e.g., 20250321

load_dotenv('/opt/airflow/.env')

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")

config = {
    "data_url":"https://github.com/openfootball/england/blob/master/2023-24/1-premierleague.txt",
    "output_path":f"/opt/airflow/raw_data/raw_{run_date}.txt",
    "file_path":f"/opt/airflow/clean_data/pl_2425_{run_date}.csv",
    "database": db_name,
    "table": "football_db_pl_2425",
    "user": db_user,
    "password": db_password,
    "host": "postgres", # if use docker compose, use the service name
    "port": "5432",
}
