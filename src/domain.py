from dataclasses import dataclass, replace
from datetime import datetime, timedelta

@dataclass(frozen=True)
class Subscriber:
    NOTIFICATION_TIMEOUT = timedelta(days=3)

    id: str
    chat_id: str
    first_name: str
    last_name: str
    notification_time: datetime = datetime.utcnow() + NOTIFICATION_TIMEOUT

    def is_need_notify(self):
        return (datetime.utcnow() - self.notification_time) >= Subscriber.NOTIFICATION_TIMEOUT

    def update_notification_time(self):
        return replace(self, notification_time=self.notification_time + Subscriber.NOTIFICATION_TIMEOUT)

class Article:
    def __init__(self, title: str, link: str, rank: int, score: int):
        self.title = title
        self.link = link
        self.rank = rank
        self.score = score

    def __repr__(self) -> str:
        return f"Article(title={self.title}, link={self.link}, rank={self.rank}, score={self.score})"