from typing import List
from domain import Subscriber

subscribers = []

def get_subscribers() -> List[Subscriber]:
    return subscribers

def save_subscriber(s: Subscriber):
    subscribers.append(s)