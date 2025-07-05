from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'harsha',
    'start_date': datetime(2025, 7, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('weather_ingest_dag',
         default_args=default_args,
         schedule_interval='@hourly',
         catchup=False) as dag:

    fetch_and_insert = BashOperator(
        task_id='fetch_and_insert',
        bash_command='python /opt/airflow/dags/fetch_weather.py',
    )
