
import json
from airflow.models.taskinstance import Context
import psycopg2
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.baseoperator import BaseOperator
from airflow.models.connection import Connection


class PostgresOperator(BaseOperator):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name

    def get_db_connection_cursor(self):
        connection_id = 'postgres'
        pg_hook = PostgresHook(postgres_conn_id=connection_id, schema='airflow')
        connection = pg_hook.get_conn()
        cursor = connection.cursor()
        return connection, cursor

    def create_table(self):
        request = '''CREATE TABLE IF NOT EXISTS words_counting(
            id SERIAL PRIMARY KEY NOT NULL,
            word varchar (300) NOT NULL,
            count int NOT NULL);'''
        connection, cursor = self.get_db_connection_cursor()
        cursor.execute(request)
        connection.commit()
        cursor.close()
        connection.close()

    def write_values(self, _dict):
        items = list(_dict.items())
        values = [f"('{word}',{count})" for word, count in items]
        values = ','.join(values)
        values += ';'
        request = '''INSERT INTO words_counting (word, count) VALUES ''' + values
        connection, cursor = self.get_db_connection_cursor()
        cursor.execute(request)
        connection.commit()
        cursor.close()
        connection.close()

    def execute(self, context):
        self.create_table()
        task_instance = context['task_instance']
        dict_i = json.loads(task_instance.xcom_pull(task_ids='reducer', key='all_data'))
        self.write_values(dict_i)
