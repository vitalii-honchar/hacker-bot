import logging, storage, config
from domain import Subscriber
from messages import create_message
from hackernews import get_top_arcticles
from aiogram.types import Message

PARSE_MODE_MARKDOWN = 'MarkdownV2'

async def start(message: Message):
    logging.info(message)
    subscriber = Subscriber(message.from_user.id, message.chat.id, message.from_user.first_name, message.from_user.last_name)
    logging.info('Bot started: user = {}'.format(subscriber))
    storage.save_subscriber(subscriber)
    await message.answer(text="I'm a tech news bot, I will send you news every day!")
    articles = await get_top_arcticles()
    await message.answer(
        text=create_message(articles),
        parse_mode=PARSE_MODE_MARKDOWN
    )

commands = {
    'start': start
}