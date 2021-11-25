import threading
from typing import Callable

def _execute_f(period, f):
        event = threading.Event()
        while not event.is_set():
            f()
            event.wait(period)

def schedule(period, f):
    threading.Thread(target=_execute_f, daemon=True, args=(period, f)).start()

