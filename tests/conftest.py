import pytest
import psycopg
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from collections.abc import Generator

from app.main import app

CREATE_TABLE = """
CREATE TABLE address_book (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE
);
"""


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine", driver=None) as postgres:
        yield postgres


@pytest.fixture(scope="session")
def database_url(postgres_container: PostgresContainer) -> str:
    return postgres_container.get_connection_url()


@pytest.fixture(scope="session", autouse=True)
def create_tables(database_url: str):
    with psycopg.connect(database_url) as conn:
        conn.execute(CREATE_TABLE)
        conn.commit()


@pytest.fixture(autouse=True)
def cleanup_data(database_url: str):
    yield
    with psycopg.connect(database_url) as conn:
        conn.execute("DELETE FROM address_book")
        conn.commit()


@pytest.fixture
def client(database_url: str) -> Generator[TestClient]:
    import app.database as db_module
    original_url = db_module.DATABASE_URL
    db_module.DATABASE_URL = database_url

    with TestClient(app) as c:
        yield c

    db_module.DATABASE_URL = original_url