# data_pipeline

Overview of the Pipeline
Download Data: A Python script will fetch data from a URL.
Ingest into PostgreSQL: Store the downloaded data in a PostgreSQL database.
DBT for Transformation: Use DBT (Data Build Tool) to transform the data.
Visualization: Use a simple tool like Matplotlib or Streamlit to visualize the data with metadata.
Airflow Monitoring: Orchestrate and monitor the pipeline with Apache Airflow.



postgres_data:/var/lib/postgresql/data/
postgres_data is the "system file" created by postgres and it outlives the container so that if container stops, data is not lost. 
/var/lib/postgresql/data/ is a directory in container where directly points to  my local storage. it's not a folder that keeps a copy of postgres_data but a door / path to storage outside container. 


build: airflow/ 
docker will look for Dockerfile in the folder to build the container (instead of pulling from docker hub)

[FUCK THIS!!!!] airflow scheduler is for daily execution of data pipline. therefore, can be skipped in adhoc pipeline hosted in localhost. 

AIRFLOW SCHEDULER IS A MUST. OTHERWISE YOU WON'T SEE YOUR DAG TASK IN WEB UI

<!-- docker-compose exec airflow airflow dags list-import-errors -->
<!-- docker-compose exec airflow airflow dags list -->