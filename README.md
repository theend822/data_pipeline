# Data Pipeline Practices - Mar 2025

## Pipeline overview

A python data pipeline built on Docker, orchestrated by Airflow, to 
1. Download premier league 23-24 match data in txt format
2. Process txt file and ingest data in csv format into Postgres DB
3. Use DBT to transform the match data into PL standing table of each round
4. Use Metabase to build simple visualization

## Pipeline Results

![2324 Premier League Standing Table](https://drive.google.com/file/d/1ifmppqHphlt8NMX3xKwZsDo0KSK8aE3c/view?usp=sharing)
![Chelsea No Good](https://drive.google.com/file/d/14jxxV1HI-MRChDolpmaWeNQsYgKj1npP/view?usp=sharing)

## Learning points
- Airflow scheduler is a must to see the DAG pipeline in Airflow UI
- Airflow init is also highly recommanded
- As *docker-compose.yml* and *.env* are most likely to be saved in root folder, saving env variables in *.env* and use them in enviornment section of each service may come very handy
- Transformation task in dbt can be added into a Airflow DAG pipeline via `BashOperator` to execute bash command inside dbt container
	- in this way, dq check and transformation task can be chained together
- Volume mapping will overwrite the file system in docker container. If the code is working as expected, volume mapping may be skipped as long as files are copied into docker image via `COPY` command in Dockerfile 
 - But in developing stage, volume mapping allows live edit without rebuilding the image, making the development phase more efficient
- Once docker images are built and uploaded to repo, *docker-compose.yml* also need to be shared so that end user knows list / number of services in the pipeline
- Data volume is the "system file" created by postgres db that outlives the container. So that data is not lost once container is down. 
- Dockerfile only needed when building own image with customized commands / entrypoint etc.
	- build (path to folder with Dockerfile) vs image (link to image in docker hub)
	- when using build, image becomes the name of the image, not the link to docker hub anymore


## Tricks learnt

- `docker-compose exec <airflow container name> airflow dags list-import-errors` to debug import error in DAG file
- `AIRFLOW__CORE__LOAD_EXAMPLES:False` in Airflow Env will skip creating any user, even admin. Have to create manually via 
  > airflow users create \
      --username admin \
      --firstname Admin \
      --lastname User \
      --role Admin \
      --email admin@example.com \
  >   --password your_secure_password`
- The stupid **TypeError: can't compare offset-naive and offset-aware datetimes** when launching Airflow web UI is mostly due to mismatch between db timestamp (timezone aware in postgres db) and flash session timestamp (timezone native). Needs to change `session_backend` in airflow.cfg to `securecookie` 
- add *__init__.py* into a folder to make the folder a "package"; then the self-defined functions in the python files in this folder can be imported directly without specifying file path
	- if the file is in root folder where *_ _init_ _.py* is not available, better to add the root folder to PYTHONPATH env `ENV PYTHONPATH=/opt/airflow` to import seemlessly
	- In Dockerfile, setting up WORKDIR only sets up the working folder; doesn't add the folder into PYTHONPATH 



