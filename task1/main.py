
from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG
from airflow.operators.bash import BashOperator
from mapper import MapperOperator
from reducer import ReducerOperator
from utils import *


NUM_MAPPERS = 3
OUTPUT_FILE = '/home/<username>/airflow/dags/output.csv'
TWEETS_FILE = '/home/<username>/airflow/dags/tweets.csv'


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
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:
    file_name = '/home/mohammad/airflow/dags/tweets.csv'
    with open(file_name) as tweets_file:
        content = tweets_file.readlines()
    content = filter_content(content)
    lists = split_list(content, NUM_MAPPERS)
    mapper_operators = []
    for i in range(NUM_MAPPERS):
        mapper_operators.append(MapperOperator(name=f"mapper_{i + 1}", data=lists[i], task_id=f"mapper_{i + 1}"))

    reducer_operator = ReducerOperator(name="reducer", num_mappers=NUM_MAPPERS, output_file=OUTPUT_FILE, task_id='reducer')

    [*mapper_operators] >> reducer_operator
