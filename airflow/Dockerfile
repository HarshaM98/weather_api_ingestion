FROM apache/airflow:2.7.1

# Copy requirements.txt as airflow user
USER airflow
COPY requirements.txt /requirements.txt

# Install Python dependencies as airflow user
RUN pip install --user --no-cache-dir -r /requirements.txt
