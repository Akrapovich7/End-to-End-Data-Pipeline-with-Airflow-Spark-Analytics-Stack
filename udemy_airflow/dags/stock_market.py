from airflow.decorators import dag,task
from airflow.hooks.base import BaseHook
from airflow.sensors.base import PokeReturnValue
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.providers.docker.operators.docker import DockerOperator
from include.stock_market.tasks import _get_stock_prices, _store_prices,_get_formatted_csv
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table,Metadata
from airflow.providers.slack.notifications.slack_notifier import SlackNotifier


SYMBOL="NVDA"
BUCKET_NAME="stock-market"

@dag(
    start_date=datetime(2025,12,18),
    schedule="@daily",
    catchup=False,
    tags=['stock market'],
    on_success_callback=SlackNotifier(
        slack_conn_id='slack',
        text="The DAG stock_market has succeded",
        channel="#general"
    ),
    on_failure_callback=SlackNotifier(
        slack_conn_id='slack',
        text="The DAG stock_market has failed",
        channel="#general"
    )
)

def stock_market():

    @task.sensor(poke_interval=30,timeout=300,mode="poke")

    def is_api_available() -> PokeReturnValue:
        import requests
        api=BaseHook.get_connection("stock_api")

        url=f"{api.host}{api.extra_dejson['endpoint']}"
        response=requests.get(url,headers=api.extra_dejson["headers"])

        condition=response.json()["finance"]["result"] is None

        return PokeReturnValue(is_done=condition,xcom_value=url)
    #--------------------------------------------------------------------
    get_stock_prices=PythonOperator(
        task_id="get_stock_prices",
        python_callable=_get_stock_prices,
        op_kwargs={"url": "{{ti.xcom_pull(task_ids='is_api_available')}}","symbol":SYMBOL}

    )

    #--------------------------------------------------------------------

    store_prices=PythonOperator(
        task_id="store_prices",
        python_callable=_store_prices,
        op_kwargs={"stock": "{{ti.xcom_pull(task_ids='get_stock_prices')}}"}
    )

    #--------------------------------------------------------------------

    format_prices = DockerOperator(
    task_id="format_prices",
    image="airflow/stock-app",
    api_version="auto",
    auto_remove="success",

    docker_url="tcp://host.docker.internal:2375",
    network_mode="bridge",
    mount_tmp_dir=False,

    tty=True,
    environment={
        "SPARK_MASTER_URL": "spark://spark-master:7077",
        "SPARK_APPLICATION_ARGS": "{{ ti.xcom_pull(task_ids='store_prices') }}"
    },
)


    #--------------------------------------------------------------------

    get_formatted_csv=PythonOperator(
        task_id="get_formatted_csv",
        python_callable=_get_formatted_csv,
        op_kwargs={'path':"{{ti.xcom_pull(task_ids='store_prices')}}"}

    )

    #--------------------------------------------------------------------

    load_to_dw = aql.load_file(
    task_id="load_to_dw",
    input_file=File(
        path="s3://stock-market/{{ ti.xcom_pull(task_ids='get_formatted_csv') }}",
        conn_id="minio"
    ),
    output_table=Table(
        name="stock_market",
        conn_id="postgres",
        metadata=Metadata(schema="public")
    ),
    load_options={
        "aws_access_key_id": "minio",
        "aws_secret_access_key": "minio123",
        "endpoint_url": "http://minio:9000"
    }
)


    is_api_available()>>get_stock_prices>>store_prices>>format_prices>>get_formatted_csv>>load_to_dw


stock_market()