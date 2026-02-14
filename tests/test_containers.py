import psycopg
from testcontainers.postgres import PostgresContainer

CREATE_TABLE = """
CREATE TABLE address_book (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE
);
"""

def test_creating_table_in_new_container_table_exists():
    # Given
    with PostgresContainer("postgres:16-alpine", driver=None) as postgres:
        url = postgres.get_connection_url()

        with psycopg.connect(url) as conn:
            # When
            conn.execute(CREATE_TABLE)
            conn.commit()

            # Then
            cur = conn.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_name = 'address_book'"
            )
            row = cur.fetchone()

    assert row is not None
    assert row[0] == "address_book"