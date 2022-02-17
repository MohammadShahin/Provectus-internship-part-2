
from utils import *
from airflow.models.baseoperator import T, BaseOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import json

bucket_name = 'bucket'
file_key = 'somekey.csv'


class MinioOperator(BaseOperator):
    def __init__(self, name: str, file_path, num_partitions, **kwargs) -> None:
        super().__init__(**kwargs) 
        self.name = name
        self.num_partitions = num_partitions
        self.s3_hook = S3Hook('minio')
        if not self.s3_hook.check_for_bucket(bucket_name):
            self.s3_hook.create_bucket(bucket_name)
        self.s3_hook.load_file(file_path, file_key, bucket_name, replace=True)


    def execute(self, context):
        file_content = self.s3_hook.read_key(file_key, bucket_name)
        all_data = filter_content(file_content)
        partitions = split_list(all_data, self.num_partitions)
        task_instance = context['task_instance']
        for i in range(self.num_partitions):
            task_instance.xcom_push(key=f"mapper_{i + 1}_data", value=json.dumps(partitions[i]))
        
