import requests
from config_crawler import *
from pymongo import MongoClient
import json
import time

def get_proxy_by_random():
    r = requests.get(PROXY_API_URL)

    if r.status_code == 200:
        return r.text
    else:
        return None


def get_proxy_from_mogumiao():
    response = requests.get(PROXY_API_URL_OF_MOGUMIAO)
    proxies = json.loads(response.text)['msg']

    for proxy in proxies:
        item = {'proxy': proxy['ip'] + ':' + str(proxy['port']), 'is_banned': 0, 'banned_time': 0}
        save_proxy_to_mongo(item)


def get_one_proxy():
    client = MongoClient()
    db = client.proxies

    collection = db.mogumiao

    proxy = collection.find_one({'is_banned': 0})

    if proxy is not None:
        return proxy['proxy']
    else:
        return None


def save_proxy_to_mongo(proxy):

    client = MongoClient()
    db = client.proxies

    collection = db.mogumiao

    info = collection.find_one({'proxy': proxy['proxy']})

    if info is None:
        collection.insert_one(proxy)


def update_proxy_to_banned(proxy):
    client = MongoClient()
    db = client.proxies

    collection = db.mogumiao

    collection.update_one({'proxy': proxy}, {'$set': {'is_banned': 1, 'banned_time': int(time.time())}})


def proxy_request_done_for_break_defence(d):
    client = MongoClient()
    db = client.proxies

    collection = db.request_done_info

    collection.find_one({'proxy': d['proxy']})

    collection.insert_one(d)


def get_proxy_request_done_for_break_defence(where):
    client = MongoClient()
    db = client.proxies

    collection = db.request_done_info
    info = collection.find_one({'proxy': where['proxy']})

    if info is not None:
        return True
    else:
        return False


def get_proxies_banned():
    client = MongoClient()
    db = client.proxies

    collection = db.mogumiao

    result = collection.find({'is_banned': 1})

    return result


def unban_proxy(proxy):
    client = MongoClient()
    db = client.proxies

    collection = db.mogumiao

    collection.update_one({'proxy': proxy}, {'$set': {'is_banned': 0}})
