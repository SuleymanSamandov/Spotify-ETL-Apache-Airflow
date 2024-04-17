import pandas as pd
import requests
from datetime import datetime,timedelta
import time
import datetime
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import datetime
from connection import connection
from get_data import processes


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.datetime(2024,4,16),
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=1)
}

with DAG(
    'etl_for_spotify',
    default_args=default_args,
    description='ETL for Spotify',
    schedule_interval=datetime.timedelta(minutes=2),
) as dag:
    
    task=PythonOperator(
        task_id="connection_task",
        python_callable=connection,
        dag=dag
 
    )

    task2=PythonOperator(
        task_id="processes",
        python_callable=processes,
        dag=dag
 
    )



task>>task2