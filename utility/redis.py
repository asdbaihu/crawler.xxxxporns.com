import redis
from config_crawler import *


def get_connection():
    redis_handler = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=None, decode_responses=True)

    return redis_handler


def set_key(key, val, expired_seconds=2592000):
    get_connection().set(key, val, expired_seconds)


def get_key(key):
    val = get_connection().get(key)

    return val
