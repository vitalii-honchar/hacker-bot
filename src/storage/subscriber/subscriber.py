from domain import Subscriber
from storage.storage import read_cursor, update_cursor
from storage.subscriber.mapper import row_to_subscriber, subscriber_to_dict

SQL_UPSERT_SUBSCRIBER = '''
    INSERT INTO subscriber 
        (id, first_name, last_name, chat_id, notification_time)
    VALUES 
        (%(id)s, %(first_name)s, %(last_name)s, %(chat_id)s, %(notification_time)s)
    ON CONFLICT (id)
    DO UPDATE SET
        first_name=%(first_name)s,
        last_name=%(last_name)s,
        notification_time=%(notification_time)s
'''

SQL_READ_SUBSCRIBERS_FOR_NOTIFICATIONS = 'SELECT * FROM subscriber WHERE notification_time <= NOW()'

def get_subscribers_for_notifications() -> list[Subscriber]:
    with read_cursor() as cursor:
        cursor.execute(SQL_READ_SUBSCRIBERS_FOR_NOTIFICATIONS)
        rows = cursor.fetchall()
        subscribers = []
        for row in rows:
            subscribers.append(row_to_subscriber(row))
        return subscribers

def save_subscribers(subscribers: list[Subscriber]):
    with update_cursor() as cursor:
        for subscriber in subscribers:
            cursor.execute(
                SQL_UPSERT_SUBSCRIBER,
                subscriber_to_dict(subscriber)
            )

def save_subscriber(subscriber: Subscriber):
    save_subscribers([subscriber])
