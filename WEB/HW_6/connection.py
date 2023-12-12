import psycopg2
from contextlib import contextmanager
from psycopg2 import Error


@contextmanager
def create_connection():
    """ create a database connection to a Postgres database """

    try:
        conn = psycopg2.connect(host='localhost', database='webhw6', user='postgres', password='qwerty1', port='5432')
        yield conn
        conn.close()
    except psycopg2.OperationalError as err:
        raise RuntimeError(f"Failed to create database connection {err}")