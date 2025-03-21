from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
from opt.airflow.config import pipeline_config
from opt.airflow.data_operator import download_data
from opt.airflow.data_operator import process_data
from opt.airflow.data_operator import ingest_data
from opt.airflow.database.create_pg_table import create_pg_table

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

    download_data_task = PythonOperator(
        task_id="download_data",
        python_callable=download_data,
        op_kwargs={
            "url":pipeline_config["data_url"], 
            "output_raw":pipeline_config["raw_data_path"],
        },
    )

    process_data_task = PythonOperator(
        task_id="process_data",
        python_callable=process_data,
        op_kwargs={
            "input_raw": pipeline_config["raw_data_path"], 
            "output_csv": pipeline_config["processed_data_path"],
        },
    )

    create_table = SQLExecuteQueryOperator(
        task_id='create_table',
        python_callable=create_pg_table,
        op_kwargs = {
            "schema_file":"table_schema.sql",
        },
    )

    ingest_data_task = PythonOperator(
        task_id="ingest_data",
        python_callable=ingest_data,
        op_kwargs={
            "file_path":pipeline_config['processed_data_path'], 
            "table_name":pipeline_config['table_name'],
        },
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

    download_data_task >> process_data_task >> create_table >> ingest_data_task >> dbt_task >> visualize_task
