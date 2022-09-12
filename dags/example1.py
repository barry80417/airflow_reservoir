from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator

from tasks.step2 import foo

with DAG(
    'example1',
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='A simple tutorial DAG: example1',
    schedule_interval= '*/3 * * * *', #timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example1'],
) as dag:

    t1 = BashOperator(
        task_id='t1',
        bash_command='python /Users/chunweichang/airflow/tasks/step1.py',
    )

    t2 = PythonOperator(
        task_id='t2',
        python_callable=foo,
    )

    [t1, t2]
