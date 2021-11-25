import logging, config
from domain import Subscriber
from messages import create_message
from hackernews import get_top_arcticles
from telegram import Update, ParseMode
from scheduler import schedule
from subscriber_repository import get_subscribers, save_subscriber
from telegram.ext import Updater, CallbackContext, CommandHandler

config.init()
logging.info(f'Started bot with config: config = {config.bot_config}')

def _create_send_articles_by_timeout(updater: Updater):
    def send():
        for subscriber in get_subscribers():
            articles = get_top_arcticles()
           
            logging.info('Send articles: subscriber = {}, articles = {}'.format(subscriber, articles))
            updater.bot.send_message(
                chat_id=subscriber.chat_id, 
                text=create_message(articles),
                parse_mode=ParseMode.MARKDOWN_V2
            )
    
    def send_with_exception_handling():
        try:
            send()
        except Exception as e:
            logging.error('Unexpected error', e)

    return send_with_exception_handling
    
def _start_command(update: Update, context: CallbackContext):
    subscriber = Subscriber(update.effective_user.id, update.effective_chat.id, update.effective_user.first_name, update.effective_user.last_name)
    logging.info('Bot started: user = {}'.format(subscriber))
    save_subscriber(subscriber)
    context.bot.send_message(chat_id=subscriber.chat_id, text="I'm a hacker news bot, I will send you news every day!")

def start():
    updater = Updater(token=config.bot_config.token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', _start_command))
    schedule(config.bot_config.timeout_seconds, _create_send_articles_by_timeout(updater))
    updater.start_polling()

start()
