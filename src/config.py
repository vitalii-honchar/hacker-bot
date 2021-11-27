import logging, coloredlogs, sys, yaml, os

PARAM_TOKEN = 'token'
PARAM_TIMEOUT_SECONDS = 'timeout-seconds'
PARAM_STORAGE = 'storage'
CONFIG_FILE = 'hacker-bot.yaml'

def _init_logging():
    coloredlogs.install()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def _create_config():
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = CONFIG_FILE

    with open(config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        bot = config['bot']
        return BotConfig(
            token=_get_param(bot, PARAM_TOKEN), 
            timeout_seconds=int(_get_param(bot, PARAM_TIMEOUT_SECONDS)), 
            storage=_get_param(bot, PARAM_STORAGE)
        )

def _get_param(bot_config, param):
    env_param = f"BOT_{param.replace('-', '_').upper()}"
    value = os.environ.get(env_param)
    if value is not None:
        return value
    return bot_config[param]

def init():
    global bot_config
    _init_logging()
    bot_config = _create_config()

class BotConfig:
    def __init__(self, token: str, timeout_seconds: int, storage: str):
        self.token = token
        self.timeout_seconds = timeout_seconds
        self.storage = storage
    
    def __repr__(self) -> str:
        return f"BotConfig(token={self.token[:3]}***{self.token[len(self.token) - 3:]}, timeout_seconds={self.timeout_seconds}, storage={self.storage})"
    
bot_config: BotConfig = None
