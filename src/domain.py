from dataclasses import dataclass, replace
from datetime import datetime, timedelta

@dataclass(frozen=True)
class Subscriber:
    NOTIFICATION_TIMEOUT = timedelta(days=1)

    id: str
    chat_id: str
    first_name: str
    last_name: str
    notification_time: datetime = (datetime.utcnow() + NOTIFICATION_TIMEOUT).replace(hour=6, minute=0, second=0, microsecond=0)

    def update_notification_time(self):
        return replace(self, notification_time=self.notification_time + Subscriber.NOTIFICATION_TIMEOUT)

@dataclass(frozen=True)
class Article:
    title: str
    link: str
    score: int
