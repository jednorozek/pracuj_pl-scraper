from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from upload_data import upload
from pracuj_scraper import scrape
import os

#dir_path = os.path.dirname(os.path.realpath(__file__))
#cwd = os.getcwd()
#os.chdir(dir_path)
#os.chdir('/home/DOCKER/D2/dags/')

default_args = {
    'owner': 'jednorozek',
    'retries': 3,
    'retry_delay': timedelta(minutes=1)

}



with DAG(
    default_args=default_args,
    dag_id='ingest_data_v01',
    description='Scraping data from the website and uploading to the Postgres DB',
    start_date=datetime(2022, 8, 20),
    schedule_interval='@daily',
    catchup=False
) as dag:
    task1 = PythonOperator(
        task_id='scrape',
        python_callable=scrape
    )

    task2 = PythonOperator(
        task_id='upload',
        python_callable=upload
    )

    task1 >> task2