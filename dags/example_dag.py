from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from tasks import clean_data, train_model 

with DAG(
    dag_id="smart_logitrack_pipeline",
    start_date=datetime(2026, 1, 15),
    schedule_interval=False,
    catchup=False
) as dag:

    # task1 (nettoyage)
    task_clean = PythonOperator(
        task_id="clean_bronze_to_silver",
        python_callable=clean_data
    )

    # task2 (entrainement)
    task_train = PythonOperator(
        task_id="train_random_forest",
        python_callable=train_model
    )

    task_clean >> task_train