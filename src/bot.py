import logging, config, storage, command
from domain import Subscriber
from messages import create_message
from hackernews import get_top_arcticles
from telegram import Update, ParseMode
from scheduler import schedule
from telegram.ext import Updater, CallbackContext, CommandHandler

config.init()
storage.init()
logging.info(f'Started bot with config: config = {config.bot_config}')

def _create_send_articles_by_timeout(updater: Updater):
    async def send():
        subsribers_for_save = []
        articles = await get_top_arcticles()
        for subscriber in storage.get_subscribers_for_notifications():
            logging.info('Send articles to subscriber: subscriber = {}'.format(subscriber))
            updater.bot.send_message(
                chat_id=subscriber.chat_id, 
                text=create_message(articles),
                parse_mode=ParseMode.MARKDOWN_V2
            )
            subsribers_for_save.append(subscriber.update_notification_time())
        storage.save_subscribers(subsribers_for_save)
    
    async def send_with_exception_handling():
        try:
            await send()
        except Exception as e:
            logging.error('Unexpected error', e)

    return send_with_exception_handling
    
# def _start_command(update: Update, context: CallbackContext):
#     subscriber = Subscriber(update.effective_user.id, update.effective_chat.id, update.effective_user.first_name, update.effective_user.last_name)
#     logging.info('Bot started: user = {}'.format(subscriber))
#     storage.save_subscriber(subscriber)
#     context.bot.send_message(chat_id=subscriber.chat_id, text="I'm a tech news bot, I will send you news every day!")
#     articles = get_top_arcticles()
#     context.bot.send_message(
#         chat_id=subscriber.chat_id, 
#         text=create_message(articles),
#         parse_mode=ParseMode.MARKDOWN_V2
#     )

def start():
    updater = Updater(token=config.bot_config.token, use_context=True)

    for name, handler in command.commands.items():
        updater.dispatcher.add_handler(CommandHandler(name, handler))

    schedule(config.bot_config.timeout_seconds, _create_send_articles_by_timeout(updater))
    updater.start_polling()

start()
