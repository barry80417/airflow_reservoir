from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator

from tasks.f import extract, transform, load

with DAG(
    'example2',
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='A simple tutorial DAG: example2',
    schedule_interval= '@once' , #'*/3 * * * *', #timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example2'],
) as dag:

    t1 = PythonOperator(
        task_id='t1',
        python_callable=extract,
    )

    t2 = PythonOperator(
        task_id='t2',
        python_callable=transform,
    )

    t3 = PythonOperator(
        task_id='t3',
        python_callable=load,
    )

    t1 >> t2 >> t3
