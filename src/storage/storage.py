import config, psycopg2
from contextlib import contextmanager

SQL_CREATE_SCHEMA = '''
    CREATE TABLE IF NOT EXISTS subscriber (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        chat_id TEXT NOT NULL UNIQUE,
        notification_time timestamp NOT NULL
    );
'''

def init():
    with update_cursor() as cursor:
        cursor.execute(SQL_CREATE_SCHEMA)

@contextmanager
def read_cursor():
    with connection() as conn:
        yield conn.cursor()

@contextmanager
def update_cursor():
    with connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            conn.commit() 
            cursor.close()

@contextmanager
def connection():
    connection = psycopg2.connect(
        host=config.db_config.host,
        database=config.db_config.name,
        user=config.db_config.user,
        password=config.db_config.password,
        port=config.db_config.port
    )
    try:
        yield connection
    finally:
        connection.close()
