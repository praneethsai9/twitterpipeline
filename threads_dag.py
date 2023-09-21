from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from threads_etl import *

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 8),
    'email': ['tpraneethsai@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'threads_dag',
    default_args=default_args,
    description='Our first DAG with ETL process!',
    schedule_interval=timedelta(days=1),  # Set the schedule_interval for daily execution
)

run_etl = PythonOperator(
    task_id='complete_threads_etl',
    python_callable=run_threads_etl,
    dag=dag,
)

run_etl