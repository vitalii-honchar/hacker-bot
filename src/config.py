import logging, coloredlogs, sys, yaml

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
        return BotConfig(token=bot['token'], timeout_seconds=int(bot['timeout-seconds']))

def init():
    global bot_config
    _init_logging()
    bot_config = _create_config()

class BotConfig:
    def __init__(self, token: str, timeout_seconds: int):
        self.token = token
        self.timeout_seconds = timeout_seconds
    
    def __repr__(self) -> str:
        return f"BotConfig(token={self.token[:3]}***{self.token[len(self.token) - 3:]}, timeout_seconds={self.timeout_seconds})"
    
bot_config: BotConfig = None
