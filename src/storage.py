import config, psycopg2
from contextlib import contextmanager
from typing import List, Any
from domain import Subscriber

SQL_CREATE_SCHEMA = '''
    CREATE TABLE IF NOT EXISTS subscriber (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        chat_id TEXT NOT NULL UNIQUE
    );
'''

SQL_INSERT_SUBSCRIBER = '''
    INSERT INTO subscriber 
        (id, first_name, last_name, chat_id)
    VALUES 
        (%(id)s, %(first_name)s, %(last_name)s, %(chat_id)s)
'''

SQL_READ_SUBSCRIBER = 'SELECT * FROM subscriber WHERE id = %(id)s'

SQL_READ_SUBSCRIBERS = 'SELECT * FROM subscriber'


def get_subscribers() -> list[Subscriber]:
    with _read_cursor() as cursor:
        cursor.execute(SQL_READ_SUBSCRIBERS)
        rows = cursor.fetchall()
        subscribers = []
        for row in rows:
            subscribers.append(_map_row_to_subscriber(row))
        return subscribers

def save_subscriber(subscriber: Subscriber):
    with _update_cusor() as cursor:
        if not _is_subscriber_exists(subscriber, cursor):
            cursor.execute(
                SQL_INSERT_SUBSCRIBER,
                _map_subscriber_to_dict(subscriber)
            )

def init():
    with _update_cusor() as cursor:
        cursor.execute(SQL_CREATE_SCHEMA)

def _is_subscriber_exists(subscriber, cursor):
    cursor.execute(SQL_READ_SUBSCRIBER, {'id': subscriber.id})
    return len(cursor.fetchall()) > 0

def _map_row_to_subscriber(row) -> Subscriber:
    return Subscriber(id=row[0], first_name=row[1], last_name=row[2], chat_id=row[3])

def _map_subscriber_to_dict(subscriber: Subscriber) -> dict[str, object]:
    return {
        'id': subscriber.id, 
        'chat_id': subscriber.chat_id,
        'first_name': subscriber.first_name,
        'last_name': subscriber.last_name
    }

@contextmanager
def _read_cursor():
    with _connection() as conn:
        yield conn.cursor()

@contextmanager
def _update_cusor():
    with _connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            conn.commit() 
            cursor.close()

@contextmanager
def _connection():
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