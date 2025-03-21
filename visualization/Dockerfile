FROM metabase/metabase:latest

WORKDIR /opt/visulazation

# Copy requirements
# COPY requirements.txt requirements.txt

# # Install dependencies
# RUN pip install -r requirements.txt

# Copy the application code
COPY . . 

EXPOSE 3000
CMD ["java", "-jar", "/app/metabase.jar"]