FROM ghcr.io/dbt-labs/dbt-postgres:latest

WORKDIR /opt/dbt

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Chain dbt test and dbt run 
CMD ["sh", "-c", "dbt test --fail-fast && dbt run"]