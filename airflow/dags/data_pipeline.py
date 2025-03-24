from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from config import pipeline_config
from data_operator.download_data import download_data
from data_operator.process_data import process_data
from data_operator.ingest_data import ingest_data
from database.create_pg_table import create_pg_table

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

    create_table = PythonOperator(
        task_id='create_table',
        python_callable=create_pg_table,
        op_kwargs = {
            "schema_file":"/opt/airflow/database/table_schema.sql",
        },
    )

    ingest_data_task = PythonOperator(
        task_id="ingest_data",
        python_callable=ingest_data,
        op_kwargs={
            "file_path":pipeline_config['processed_data_path'], 
            "table_name":pipeline_config['table'],
        },
    )

    dbt_transformation_task = BashOperator(
        task_id="dbt_execute",
        bash_command="docker exec pl_dbt dbt test --fail-fast && docker exec pl_dbt dbt run"
    )

    download_data_task >> process_data_task >> create_table >> ingest_data_task >> dbt_transformation_task 
