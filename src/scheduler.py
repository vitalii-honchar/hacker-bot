import threading, config, asyncio, logging
from typing import Callable

# def _execute_f(period, f):
#     asyncio.set_event_loop(config.event_loop)
#     asyncio.get_event_loop().run_forever()
    # event = threading.Event()
    # while not event.is_set():
    #     asyncio.set_event_loop(config.event_loop)
    #     logging.info('loop = {}'.format(config.event_loop))
    #     logging.info('asyncio loop = {}'.format(asyncio.get_event_loop()))
    #     f()
    #     event.wait(period)

def schedule(period, f):
    def init_event_loop():
        asyncio.set_event_loop(config.event_loop)
        asyncio.get_event_loop().create_task(_execute_f())
        asyncio.get_event_loop().run_forever()
    
    async def _execute_f():
        # while True:
            # f()
        await f()
        await asyncio.sleep(period)

    threading.Thread(target=init_event_loop).start()

    # threading.Thread(target=_execute_f, daemon=True, args=(period, f)).start()


