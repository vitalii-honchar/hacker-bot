import config, sqlite3
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
        (:id, :first_name, :last_name, :chat_id)
'''

SQL_READ_SUBSCRIBER = 'SELECT * FROM subscriber WHERE id = :id'

SQL_READ_SUBSCRIBERS = 'SELECT * FROM subscriber'


def get_subscribers() -> list[Subscriber]:
    with _read_cursor() as cursor:
        rows = cursor.execute(SQL_READ_SUBSCRIBERS).fetchall()
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
    return len(cursor.execute(SQL_READ_SUBSCRIBER, {'id': subscriber.id}).fetchall()) > 0

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
        try:
            yield conn.cursor()
        finally:
            conn.commit() 

@contextmanager
def _connection():
    connection = sqlite3.connect(config.bot_config.storage)
    try:
        yield connection
    finally:
        connection.close()