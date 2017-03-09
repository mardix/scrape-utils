"""

scrape-utils

It contains
    - Spider
    - Task
    - Bloomfilter
    - UserAgents

- requirements
    requests==2.12.4

https://free-public-proxies.herokuapp.com

"""

import os
import uuid
import requests
import ua_list
import json
import random
import time
from .bloom import BloomFilter
from grab.spider import Spider, Task

redis_store = None
STORE_TYPE = "file"  # redis | file | memory

PUBLIC_PROXIES_URL = "https://free-public-proxies.herokuapp.com"
PROXY_LIST_TTL = 300
PUBLIC_PROXY_ENDPOINT = "all"
CACHE_FILE = "/tmp/public_proxies.cache"
REDIS_CACHE_KEY = "PUBLIC_PROXIES_CACHE"

_store = {
    "ttl": 0,
    "data": []
}


def request(url, **kwargs):
    """
    Fecth is wrapper around requests.get, but it adds random user agents
    and proxy
    :param url:
    :param kwargs:
    :return:
    """
    proxies = {
        "http": get_random_proxy(),
        "https": get_random_proxy(),
    }
    headers = {
        "Connection": "close",  # another way to cover tracks
        "User-Agent": get_random_user_agent()
    }

    r = requests.get(url.strip(), headers=headers, proxies=proxies, **kwargs)
    if r.status_code != 200:
        raise Exception(
            "Unable to fetch url '%s'. Status Code: %s" % (url, r.status_code))
    return r


def save_file(url, path, **kwargs):
    """
    To save a file into local path
    :param url: the url
    :param path: where to download the file to
    :param kwargs: request kwargs
    :return: str - the file path
    """

    _url2 = url
    if "?" in _url2:
        _url2 = os.path.splitext(_url2.split("?")[0])
    ext = os.path.splitext(_url2)[1][1:].lower()
    name = uuid.uuid4().hex
    name += ".%s" % ext
    filepath = os.path.join(path, name)
    #r = request(url, stream=True, **kwargs)
    r = requests.get(url, stream=True)
    with open(filepath, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    return filepath


def load_proxies_list(proxies):
    """
    To load custom proxies list and bypass the service one
    :param proxies: list
    :return:
    """
    _store.update({
        "ttl": int(time.time()) + (60 * 60 * 24 * 30 * 365),
    # 1 year, so it never gets expires
        "data": proxies
    })


# ------------------------------------------------------------------------------

def get_random_user_agent():
    return ua_list.get_random()


def get_random_proxy(scheme=None):
    """
    Return a random proxy
    :param scheme: when provided, it will try to find proxy that matches the
        scheme. If nothing found, it will return whatever found.
        options: https:// | http:// | socks4:// | socks5
        * for socks, you must have SOCKS as region in fetch public_proxies
    :return:
    """
    _method = STORE_TYPE.lower()
    ttime = int(time.time())
    ttl = PROXY_LIST_TTL + ttime
    data = None
    if _store.get("ttl", 0) < ttime:
        # redis
        if _method == "redis":
            data = redis_store.get(REDIS_CACHE_KEY)
            if data:
                ttl = int(redis_store.ttl(REDIS_CACHE_KEY)) + ttime
                data = json.loads(data)
            else:
                data = _fetch_public_proxies()
                redis_store.set(REDIS_CACHE_KEY, json.dumps(data))
                redis_store.expire(REDIS_CACHE_KEY, PROXY_LIST_TTL)
        # file
        elif _method == "file":
            _write = True
            if os.path.isfile(CACHE_FILE):
                _write = False
                with open(CACHE_FILE, "r") as f:
                    content = f.read()
                    _ttl = 0
                    if content:
                        dstore = json.loads(content)
                        _ttl = int(dstore.get("ttl", 0))
                        data = dstore.get("data")

                    if _ttl < ttime:
                        _write = True
                    else:
                        ttl = _ttl
            if _write:
                with open(CACHE_FILE, "w") as f:
                    data = _fetch_public_proxies()
                    _save_data = json.dumps({
                        "ttl": ttl,
                        "data": data
                    })
                    f.write(_save_data)
        # memory
        else:
            data = _fetch_public_proxies()

        _store.update({
            "ttl": ttl,
            "data": data
        })

    data = _store.get("data")

    _exhaustion = 25
    if scheme:
        while True:
            rand = random.choice(data)
            if rand.startswith(scheme):
                return rand
            else:
                _exhaustion -= 1
            if _exhaustion <= 0:
                return rand
    else:
        return random.choice(data)


def _fetch_public_proxies(region=None):
    region = region or PUBLIC_PROXY_ENDPOINT
    url = "%s/%s/" % (PUBLIC_PROXIES_URL, region)
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Error[%s] fetching %s" % (r.status_code, url))
    return r.json().get("data")

