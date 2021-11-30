from airflow.models.baseoperator import BaseOperator
import json


class ReducerOperator(BaseOperator):
    def __init__(self, name: str, num_mappers: int, output_file: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.num_mappers = num_mappers
        self.output_file = output_file

    def execute(self, context):
        word_count = {}
        task_instance = context['task_instance']
        for i in range(1, self.num_mappers + 1):
            dict_i = json.loads(task_instance.xcom_pull(task_ids=f'mapper_{i}', key=f'mapper_{i}_data'))
            for item in dict_i.items():
                if item[0] in word_count:
                    word_count[item[0]] += item[1]
                else:
                    word_count[item[0]] = item[1]

        with open(self.output_file, 'w') as out:
            out.write('word,count\n')
            for item in word_count.items():
                out.write(f"{item[0]},{item[1]}\n")
