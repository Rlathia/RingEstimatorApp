import redis
import configparser

# Load the config file using the Config Parser module
config = configparser.ConfigParser()
config.read("config.cfg")

class RedisClient:

    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.r = redis.Redis(
            host=config["Database"]["host"],
            port=config["Database"]["port"],
            password=config["Database"]["password"],
            decode_responses=True)

#redis_client = RedisClient(config)
