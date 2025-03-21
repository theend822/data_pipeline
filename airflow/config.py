from datetime import datetime

run_date = datetime.now().strftime('%Y%m%d') # e.g., 20250321

pipeline_config = {
    "data_url":"https://github.com/openfootball/england/blob/master/2023-24/1-premierleague.txt",
    "raw_data_path":f"/opt/airflow/raw_data/raw_{run_date}.txt",
    "processed_data_path":f"/opt/airflow/clean_data/pl_2425_{run_date}.csv",
    "table": "premier_league_2425_raw",
}


# import os
# from dotenv import load_dotenv

# load_dotenv('/opt/airflow/.env')

# db_user = os.getenv("POSTGRES_USER")
# db_password = os.getenv("POSTGRES_PASSWORD")
# db_name = os.getenv("POSTGRES_DB")
# db_port = os.getenv("POSTGRES_PORT")
# db_host = os.getenv("POSTGRES_HOST")

# pg_db_config = {
#     "database": db_name,
#     "user": db_user,
#     "password": db_password,
#     "host": db_host, # if use docker compose, use the service name
#     "port": db_port,
# }