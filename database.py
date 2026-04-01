import redis
import configparser

# Load the config file using the Config Parser module
config = configparser.ConfigParser()
config.read("config.cfg")

r = redis.Redis(
            host=config["Database"]["host"],
            port=config["Database"]["port"],
            password=config["Database"]["password"],
            decode_responses=True)

print(r)

r.set ("somekey", "somevalue")
value = r.get("somekey")
print(value)