import json

from airflow.models.baseoperator import BaseOperator


class MapperOperator(BaseOperator):
    def __init__(self, name: str, data: list, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.data = data

    def execute(self, context):
        word_count = {}
        for word in self.data:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        task_instance = context['task_instance']
        task_instance.xcom_push(key=f"{self.name}_data", value=json.dumps(word_count))
