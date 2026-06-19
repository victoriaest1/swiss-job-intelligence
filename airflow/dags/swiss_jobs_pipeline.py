from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = "/Users/eldorado/Documents/swiss-job-intelligence"
DBT_DIR = f"{PROJECT_DIR}/dbt_project/swiss_jobs_dbt"
PYTHON = f"{PROJECT_DIR}/venv/bin/python"
DBT = f"{PROJECT_DIR}/venv/bin/dbt"

default_args = {
    'owner': 'victoria',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='swiss_jobs_pipeline',
    default_args=default_args,
    description='Daily Swiss job market intelligence pipeline',
    schedule_interval='0 6 * * *',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['swiss_jobs', 'data_engineering'],
) as dag:

    ingest_task = BashOperator(
        task_id='ingest_data',
        bash_command=f'{PYTHON} {PROJECT_DIR}/ingestion/data_generator.py',
    )

    dbt_run_task = BashOperator(
        task_id='dbt_run',
        bash_command=f'cd {DBT_DIR} && {DBT} run',
    )

    dbt_test_task = BashOperator(
        task_id='dbt_test',
        bash_command=f'cd {DBT_DIR} && {DBT} test',
    )

    dbt_docs_task = BashOperator(
        task_id='dbt_docs',
        bash_command=f'cd {DBT_DIR} && {DBT} docs generate',
    )

    export_dashboard = BashOperator(
        task_id='export_dashboard_json',
        bash_command=f'{PYTHON} {PROJECT_DIR}/export_dashboard_json.py',
    )

    ingest_task >> dbt_run_task >> dbt_test_task >> dbt_docs_task >> export_dashboard
