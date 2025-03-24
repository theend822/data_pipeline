FROM ghcr.io/dbt-labs/dbt-postgres:1.9.latest@sha256:a705312b55af0ebdd149977914c28502a382d74dca8fe51fff368371a61cc8a7

WORKDIR /opt/dbt

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apk add --no-cache coreutils
# you're essentially telling the container to watch for new content in a file that never changes and never has any content
# if no task to run, container will shut down immediately. however, we will manually trigger transformation task in airflow and the timing is not fixed. therefore, need the container to be up and runnig
CMD ["tail", "-f", "/dev/null"]