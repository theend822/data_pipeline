from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import pandas as pd
from sqlalchemy import create_engine
from opt.airflow.config import config
from opt.airflow.data_operator import download_data
from opt.airflow.data_operator import process_data
from opt.airflow.data_operator import ingest_data


default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 3, 21),
}

with DAG (
    "e2e_data_pipeline",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,

) as dag: 

    def ingest_data():
        """Ingest data into PostgreSQL"""
        DATABASE_URI = "postgresql://airflow:airflow@postgres:5432/airflow"
        DATA_PATH = "/opt/airflow/data/raw_data.csv"
        
        engine = create_engine(DATABASE_URI)
        df = pd.read_csv(DATA_PATH)
        df.to_sql("raw_table", engine, if_exists="replace", index=False)
        print("Data ingested successfully.")

        create_table = SQLExecuteQueryOperator(
            task_id='create_table',
            conn_id='my_postgres_connection', # set up in airflow UI
            sql='sql/table_schema.sql',
        )

    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_csv_to_postgres,
        op_kwargs={
            'file_path':config['file_path'], 
            'user':config['user'], 
            'password':config['password'], 
            'host':config['host'], 
            'port':config['port'], 
            'database':config['database'], 
            'table_name':config['table'],
        }, # op stands for operator
    )

    verify_data = SQLExecuteQueryOperator(
        task_id='verify_data',
        conn_id='my_postgres_connection',
        sql='SELECT * FROM airflow_yellow_taxi LIMIT 1',
        do_xcom_push=True, # without this, query is run and never saved anywhere
        # with this, query results can be found in verify_data task -> Task Instance Details > XCom.
    )


    download_data_task = PythonOperator(
        task_id="download_data",
        python_callable=download_data,
        op_kwargs={
            "url":config["data_url"], 
            "file_path":config["file_path"],
        },
        dag=dag
    )

    process_data_task = PythonOperator(
        task_id="process_data",
        python_callable=process_data,
        op_kwargs={

        },
        dag=dag
    )

    ingest_data_task = PythonOperator(
        task_id="ingest_data",
        python_callable=ingest_data,
        op_kwargs={
            "user":config['user'], 
            "password":config['password'], 
            "host":config['host'], 
            "port":config['port'], 
            "database":config['database'], 
            "file_path":config['file_path'], 
            "table_name":config['table_name'],
        },
        dag=dag
    )

    dbt_task = PythonOperator(
        task_id="run_dbt",
        python_callable=lambda: os.system("dbt run --profiles-dir /usr/app/dbt"),
        dag=dag
    )

    visualize_task = PythonOperator(
        task_id="generate_visualization",
        python_callable=lambda: os.system("python /app/visualize.py"),
        dag=dag
    )

    fetch_task >> ingest_task >> dbt_task >> visualize_task
