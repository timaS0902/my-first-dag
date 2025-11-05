from __future__ import annotations

from datetime import datetime
import json

from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import get_current_context
from airflow.utils.dates import days_ago
from airflow.providers.postgres.hooks.postgres import PostgresHook


# DAG: ручной запуск (schedule=None), без catchup
with DAG(
    dag_id="hello_world_etl",
    description="ETL demo: extract -> transform -> load into Postgres",
    schedule=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["demo"],
) as dag:

    @task
    def extract():
        """
        Имитация источника данных.
        Возвращаем небольшой JSON с run_id и сообщением.
        """
        ctx = get_current_context()
        return {
            "run_id": ctx["run_id"],
            "message": "hello world",
            "extracted_at": datetime.utcnow().isoformat(),
        }

    @task
    def transform(payload: dict):
        """
        Простая трансформация: uppercase + добавим длину строки.
        """
        msg = payload["message"]
        payload["message_upper"] = msg.upper()
        payload["msg_len"] = len(msg)
        payload["transformed_at"] = datetime.utcnow().isoformat()
        return payload

    @task
    def load(data: dict):
        """
        Записываем результат в Postgres (контейнер 'postgres').
        Соединение берём из AIRFLOW_CONN_PG_DEMO.
        """
        hook = PostgresHook(postgres_conn_id="pg_demo")

        # 1) Создаём схему/таблицу, если их ещё нет
        hook.run(
            """
            CREATE SCHEMA IF NOT EXISTS demo;

            CREATE TABLE IF NOT EXISTS demo.hello_events (
                id SERIAL PRIMARY KEY,
                run_id TEXT,
                message TEXT,
                message_upper TEXT,
                msg_len INT,
                raw JSONB,
                inserted_at TIMESTAMPTZ DEFAULT now()
            );
            """
        )

        # 2) Пишем строку
        hook.run(
            """
            INSERT INTO demo.hello_events
                (run_id, message, message_upper, msg_len, raw)
            VALUES (%s, %s, %s, %s, %s);
            """,
            parameters=(
                data.get("run_id"),
                data.get("message"),
                data.get("message_upper"),
                data.get("msg_len"),
                json.dumps(data),
            ),
        )

    # Граф: extract -> transform -> load
    load(transform(extract()))
