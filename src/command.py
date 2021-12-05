import logging, storage, config
from domain import Subscriber
from messages import create_message
from hackernews import get_top_arcticles
from telegram import Update, ParseMode
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    async def _start():
        subscriber = Subscriber(update.effective_user.id, update.effective_chat.id, update.effective_user.first_name, update.effective_user.last_name)
        logging.info('Bot started: user = {}'.format(subscriber))
        storage.save_subscriber(subscriber)
        context.bot.send_message(chat_id=subscriber.chat_id, text="I'm a tech news bot, I will send you news every day!")
        articles = await get_top_arcticles()
        context.bot.send_message(
            chat_id=subscriber.chat_id, 
            text=create_message(articles),
            parse_mode=ParseMode.MARKDOWN_V2
        )
    config.event_loop.create_task(_start())

commands = {
    'start': start
}