import logging, coloredlogs, sys, yaml, os

PARAM_BOT = 'bot'
PARAM_BOT_TOKEN = 'token'
PARAM_BOT_TIMEOUT_SECONDS = 'timeout-seconds'

PARAM_DATABASE = 'database'
PARAM_DATABASE_HOST = 'host'
PARAM_DATABASE_NAME = 'name'
PARAM_DATABASE_USER = 'user'
PARAM_DATABASE_PASSWORD = 'password'
PARAM_DATABASE_PORT = 'port'

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
        bot = config[PARAM_BOT]
        database = config[PARAM_DATABASE]
        return (_create_bot_config(bot), _create_database_config(database))

def _create_bot_config(bot_config):
    return BotConfig(
        token=_get_param(bot_config, PARAM_BOT_TOKEN, PARAM_BOT), 
        timeout_seconds=int(_get_param(bot_config, PARAM_BOT_TIMEOUT_SECONDS, PARAM_BOT)), 
    )

def _create_database_config(db_config):
    return DatabaseConfig(
        host=_get_param(db_config, PARAM_DATABASE_HOST, PARAM_DATABASE),
        name=_get_param(db_config, PARAM_DATABASE_NAME, PARAM_DATABASE),
        user=_get_param(db_config, PARAM_DATABASE_USER, PARAM_DATABASE),
        password=_get_param(db_config, PARAM_DATABASE_PASSWORD, PARAM_DATABASE),
        port=int(_get_param(db_config, PARAM_DATABASE_PORT, PARAM_DATABASE))
    )

def _get_param(config, param, prefix):
    env_param = f"{prefix}_{param.replace('-', '_').upper()}"
    value = os.environ.get(env_param)
    if value is not None:
        return value
    return config[param]

def init():
    global bot_config, db_config
    _init_logging()
    bot_config, db_config = _create_config()

class BotConfig:
    def __init__(self, token: str, timeout_seconds: int):
        self.token = token
        self.timeout_seconds = timeout_seconds
    
    def __repr__(self) -> str:
        return f"BotConfig(token={self.token[:3]}***{self.token[len(self.token) - 3:]}, timeout_seconds={self.timeout_seconds})"

class DatabaseConfig:
    def __init__(self, host: str, name: str, user: str, password: str, port: int):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.port = port

    def __repr__(self) -> str:
        return f"DatabaseConfig(host={self.host}, name={self.name}, user={self.user}, password=***, port={self.port})"

bot_config: BotConfig = None
db_config: DatabaseConfig = None
