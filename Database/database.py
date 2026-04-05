import redis
import configparser

# Load the config file using the Config Parser module
config = configparser.ConfigParser()
config.read("config.cfg")

class RedisClient:

    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):

        if self._initialized:
            return

        self.r = redis.Redis(
            host=config["Database"]["host"],
            port=config["Database"]["port"],
            password=config["Database"]["password"],
            decode_responses=True)
        self._initialized = True

    def save_estimate(self, key, data):
        self.r.hset(key, mapping=data)

    def get_all_estimates(self):
        keys = self.r.keys("estimate:*")
        return [self.r.hgetall(k) for k in keys]