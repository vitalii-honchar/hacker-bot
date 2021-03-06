import asyncio, hackernews, logging, messages
from storage.subscriber.subscriber import get_subscribers_for_notifications, save_subscribers
from aiogram import Bot

async def _send_news(bot: Bot):
    subscribers = await get_subscribers_for_notifications()
    if len(subscribers) > 0:
        subsribers_for_save = []
        articles = await hackernews.get_top_arcticles()
        for subscriber in subscribers:
            msg = messages.create_message(articles)
            try:
                logging.info('Send articles to subscriber: subscriber = {}, message = {}'.format(subscriber, msg))
                await bot.send_message(
                    chat_id=subscriber.chat_id, 
                    text=msg,
                    parse_mode=messages.PARSE_MODE_MARKDOWN
                )
                subsribers_for_save.append(subscriber.update_notification_time())
            except Exception as e:
                logging.error('Error during send article: subscriber = {}, message = {}'.format(subscriber, msg), e)
        await save_subscribers(subsribers_for_save)

async def _start_send_news(period: int, bot: Bot):
    while True:
        try:
            await _send_news(bot)
            await asyncio.sleep(period)
        except Exception as e:
            logging.error('Unexpected error', e)

def start_send_news(period: int, bot: Bot):
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.create_task(_start_send_news(period, bot))
 