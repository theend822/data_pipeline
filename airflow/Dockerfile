FROM apache/airflow:2.10.5-python3.12
# temporary switch to root user to install applications
USER root 

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/airflow
COPY airflow /opt/airflow

USER airflow
RUN pip install --no-cache-dir -r requirements.txt