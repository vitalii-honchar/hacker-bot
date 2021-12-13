import logging, messages
from storage.subscriber.subscriber import save_subscriber
from domain import Subscriber
from hackernews import get_top_arcticles
from aiogram.types import Message


async def start(message: Message):
    logging.info(message)
    subscriber = Subscriber(message.from_user.id, message.chat.id, message.from_user.first_name, message.from_user.last_name)
    logging.info('Bot started: user = {}'.format(subscriber))
    save_subscriber(subscriber)
    await message.answer(text="I'm a tech news bot, I will send you news every day!")
    articles = await get_top_arcticles()
    await message.answer(
        text=messages.create_message(articles),
        parse_mode=messages.PARSE_MODE_MARKDOWN
    )

commands = {
    'start': start
}
