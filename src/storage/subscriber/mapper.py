from domain import Subscriber

def row_to_subscriber(row) -> Subscriber:
    return Subscriber(
        id=row[0], 
        first_name=row[1], 
        last_name=row[2], 
        chat_id=row[3], 
        notification_time=row[4]
    )

def subscriber_to_dict(subscriber: Subscriber) -> dict[str, object]:
    return {
        'id': subscriber.id, 
        'chat_id': subscriber.chat_id,
        'first_name': subscriber.first_name,
        'last_name': subscriber.last_name,
        'notification_time': subscriber.notification_time
    }