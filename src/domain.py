from dataclasses import dataclass, replace
from datetime import datetime, timedelta

def _next_notification_time():
    return (datetime.utcnow() + timedelta(days=1)).replace(hour=6, minute=0, second=0, microsecond=0)

@dataclass(frozen=True)
class Subscriber:
    id: str
    chat_id: str
    first_name: str
    last_name: str
    notification_time: datetime = _next_notification_time()

    def update_notification_time(self):
        return replace(self, notification_time=_next_notification_time())

@dataclass(frozen=True)
class Article:
    title: str
    link: str
    score: int
