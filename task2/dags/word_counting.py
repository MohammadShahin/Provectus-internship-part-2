from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG
from airflow.operators.bash import BashOperator

from utils import *

from mapper import MapperOperator
from reducer import ReducerOperator
from postgres_operator import PostgresOperator
from minio_operator import MinioOperator

NUM_MAPPERS = 3
OUTPUT_FILE = './output.csv'
file_path = '/opt/airflow/dags/tweets.csv'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
    'WordCounting',
    default_args=default_args,
    description="Finds words' Frequency",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    minio_operator = MinioOperator(name='minio', file_path=file_path, num_partitions=NUM_MAPPERS, task_id='minio')
    
    mapper_operators = [MapperOperator(name=f"mapper_{i + 1}", index=i+1, task_id=f"mapper_{i + 1}") for i in range(NUM_MAPPERS)]

    reducer_operator = ReducerOperator(name="reducer", num_mappers=NUM_MAPPERS, task_id='reducer')

    postgres_operator = PostgresOperator(name='postgres_operator', task_id='postgres_operator')

    minio_operator >> [*mapper_operators] >> reducer_operator >> postgres_operator

