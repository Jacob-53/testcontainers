import psycopg

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/devdb"


def get_connection() -> psycopg.Connection:
    return psycopg.connect(DATABASE_URL)