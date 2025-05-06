from dotenv import load_dotenv
import os
import pytest
import psycopg2
from database.task_repository import TaskRepository
import jsonschema
import uuid
from models.config import Envs
from requests import Session
from common_api.camunda_api import CamundaAPI
from context import TestContext


@pytest.fixture(scope="function", autouse=True)
def test_context() -> TestContext:
    current_test_context = TestContext()
    return current_test_context


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(
        db_host=os.getenv("DB_HOST"),
        db_port=os.getenv("DB_PORT"),
        db_user=os.getenv("DB_USER"),
        db_pass=os.getenv("DB_PASS"),
        db_name=os.getenv("DB_NAME")
    )


@pytest.fixture(scope="session")
def db_connection(envs: Envs) -> psycopg2.connect:
    conn = psycopg2.connect(
        host=envs.db_host,
        user=envs.db_user,
        password=envs.db_pass,
        dbname=envs.db_name,
        port=envs.db_port
    )
    yield conn
    conn.close()


@pytest.fixture(scope="function")
def task_repository(db_connection) -> TaskRepository:
    return TaskRepository(db_connection)


@pytest.fixture(scope="function")
def db_cursor(db_connection):
    cursor = db_connection.cursor()
    yield cursor
    cursor.close()


@pytest.fixture(scope="function")
def session():
    session = Session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def cleanup_database(task_repository, test_context):
    yield
    task_repository.delete_task_by_task_id_from_all_tables(test_context.get_param("task_id"))


@pytest.fixture(scope="function")
def create_success_schema():
    return {
        "type": "object",
        "properties": {
            "success": {
                "type": "boolean"
            },
            "taskId": {
                "type": "string",
                "format": "uuid"
            }
        },
        "required": ["success", "taskId"]
    }


@pytest.fixture(scope="function")
def create_error_schema():
    return {
        "type": "object",
        "properties": {
            "success": {"type": "boolean"},
            "error": {
                "type": "object",
                "properties": {
                    "code": {"type": "number"},
                    "type": {"type": "string"},
                    "message": {"type": "string"}
                },
                "required": ["code", "type", "message"]
            }
        },
        "required": ["success", "error"]
    }
