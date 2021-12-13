import logging, config, command, news_sender
from storage import storage
from aiogram import Bot, Dispatcher, executor

config.init()
storage.init()
logging.info(f'Started bot with config: config = {config.bot_config}')

def start():
    bot = Bot(token=config.bot_config.token)
    db = Dispatcher(bot)
    
    for name, handler in command.commands.items():
        db.register_message_handler(handler, commands=[name])

    news_sender.start_send_news(config.bot_config.timeout_seconds, bot)    
    executor.start_polling(db, skip_updates=True)

start()
