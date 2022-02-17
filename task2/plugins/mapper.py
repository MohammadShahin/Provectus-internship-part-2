import json

from airflow.models.baseoperator import BaseOperator


class MapperOperator(BaseOperator):
    def __init__(self, name, index, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.index = index

    def execute(self, context):
        task_instance = context['task_instance']
        data = json.loads(task_instance.xcom_pull(task_ids=f'minio', key=f'mapper_{self.index}_data'))
        word_count = {}
        for word in data:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        task_instance.xcom_push(key=f"mapper_{self.index}_processed_data", value=json.dumps(word_count))