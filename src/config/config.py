import logging
from pythonjsonlogger import jsonlogger
import gila

config_path = './src/config'
config_type = ".yaml"
config_name = "config"

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s - %(levelname)s - %(module)s - %(lineno)s - %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel("INFO")


def get_runenvmap():
    g = gila.Gila()
    g.automatic_env()

    env_map = {
        "server.env": g.get('ENV'),
        "server.host": g.get('HOST'),
        "server.port": g.get('SERVER_PORT'),
        "server.apipath": g.get('API_PATH'),
        "aws.s3bucket": g.get('S3BUCKET'),
        "aws.cdnlink": g.get('CDNLINK'),
        "database.database": g.get('DATABASE'),
        "database.user": g.get('DBUSER'),
        "database.password": g.get('PASSWORD'),
        "database.host": g.get('HOST'),
        "database.port": g.get('PORT'),

    }
    return env_map, g


def get_configurations(config_path, config_name, config_type, env_map, g):    
    g.add_config_path(config_path)
    g.set_config_type(config_type)
    g.set_config_name(config_name)
    try:
        g.read_config_file()
    except Exception as e:
        logger.debug("could not read config file %s", e)
    localconfig = {}
    for key, _ in env_map.items():
        localconfig[key] = g.get(key)
    for key, value in env_map.items():
        if value is not None:
            g.override(key, value)
        else:
            g.override(key,localconfig[key])
    return g.all_config()


env_map, g = get_runenvmap()
configurations = get_configurations(
    config_path, config_name, config_type, env_map, g)