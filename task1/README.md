
# Airflow with Provectus
All the tasks in this repository were done as part of Provectus internship part 2. 

## Table of contents
- [Task 1](#task1)
    - [Task description](#task1-description)
    - [Solution logic](#task1-solution-logic)
    - [Running the solution](#task1-run-solution)

<a name="task1"></a>
## Task 1

<a name="task1-description"></a>
### Task description
We were asked to implement MapReducer using Apache airflow to find the word counts in a csv file.

<a name="task1-solution-logic"></a>
### Solution logic
First the data from the csv file is filtered. This is done by taking rid of the comas, spaces, and end-lines. In the end
a list of strings is generated from the csv file. The list is distributed evenly among the mappers. A mapper converts a list
of string to a dictionary (key: word, value: count), and forwards the output to the reducer. The reducer merges the outputs 
of all mappers to a single dictionary. Finally, it writes the resultant dictionary into a csv file.

<a name="task1-run-solution"></a>
### Run the solution
To run the solution you need to run the following steps taken from [the link](https://airflow.apache.org/docs/apache-airflow/stable/start/local.html):

```shell
# Airflow needs a home. `~/airflow` is the default, but you can put it
# somewhere else if you prefer (optional)
export AIRFLOW_HOME=~/airflow

# Install Airflow using the constraints file
AIRFLOW_VERSION=2.2.2
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.6
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.2.2/constraints-3.6.txt
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

To make sure apache airflow works run the following command:
```shell
airflow version
```

After that open the folder `~/airflow`, and create a new directory `dags` in it. Then in `dage` copy-paste the files 
[main.py, mapper.py , reducer.py, utils.py, tweets.csv]. Change `<username>` in the file main.py to the corresponding username.

Next, you need to run airflow webserver using the command:
```shell
airflow webserver
```

The next step is to run airflow scheduler using the command:
```shell
airflow scheduler
```

Finally, open the terminal in the `dags` we added earlier, and run the following command:
```shell
airflow dags backfill WordCounting --start-date 2015-06-01
```

You can check the logs of the MapReducer in `localhost:8080`. The output file should be in the same `dags` directory.
