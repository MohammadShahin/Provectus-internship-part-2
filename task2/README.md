
# Airflow with Provectus
All the tasks in this repository were done as part of Provectus internship part 2. 

## Table of contents
- [Task 1](#task2)
    - [Task description](#task2-description)
    - [Solution logic](#task2-solution-logic)
    - [Running the solution](#task2-run-solution)

<a name="task2"></a>
## Task 2

<a name="task2-description"></a>
### Task description
We were asked to implement MapReducer using Apache airflow to count the word counts in a csv file. The file to be read is stored in MinIO. The output of the process should be written into Postgres database.

<a name="task2-solution-logic"></a>
### Solution logic
There are four main operators: MinIO operator, mapper, reducer, Postgres operator. 
Firstly, the file is loaded to MinIO. Then the file is read from MinIO. After that the data on the csv file is filtered. This is done by taking rid of the commas, spaces, and end-lines. Then anything but the latin letters are removed.
A list of strings is generated from the csv file. The list is distributed evenly among the mappers. A mapper converts a list
of string to a dictionary (key: word, value: count), and forwards the output to the reducer. The reducer merges the outputs 
of all mappers to a single dictionary. Finally, Postgres operator writes the combined dictionary to the database. 

<a name="task2-run-solution"></a>
Below is the steps for running the application for ubuntu 20.04.

You need to have docker and docker-compose installed. Here is a guide how to install them taken from the [official documentation](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html). 

- Install Docker [Community Edition (CE)](https://docs.docker.com/engine/installation/) on your workstation. Depending on the OS, you may need to configure your Docker instance to use 4.00 GB of memory for all containers to run properly.

- Install [Docker Compose](https://docs.docker.com/compose/install/) v1.29.1 and newer on your workstation.

*Note*: Older versions of docker-compose might not support all the features required by docker-compose.yml file, so double check that your version meets the minimum version requirements.

Open the terminal inside the project directory, run the following command:
```shell
mkdir logs ; mkdir minio ; sudo chmod -R 777 minio ; mkdir pgadmin ; sudo chmod -R 777 pgadmin
```

Now you should run docker-compose in the project's directory using the command:
```shell
docker-compose up --build
```
The appplication should run. The name of the DAG is WordCounting. You can check Airflow on `localhost:8080`. 

You can also check the postgres database in Pgadmin `localhost:5050`. To do that, you need to create a server on Pgadmin. Below are the specifications of the server:
- server name: airflow
- host: postgres
- username: airflow
- password: airflow

The table will be stored in the server `airflow` in a table called `words_counting`. 