from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'http_random_data', default_args=default_args, schedule_interval=timedelta(minutes=10))

start = DummyOperator(task_id='run_this_first', dag=dag)

passing = KubernetesPodOperator(namespace='raj-airflow',
        image="tuskacad/fakerdata:latest",
                          labels={"foo": "bar"},
                          name="random_http_data",
                          task_id="pod_task",
                          get_logs=False,
                          dag=dag,
                          in_cluster=True
                          )


passing.set_upstream(start)
