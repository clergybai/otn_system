import redis
import redis_lock
import urllib.parse
from common.config import settings


AUTH_DB = 'auth_db'
LOCK_DB = 'lock_db'
USER_TOKEN_HSET = "user_token"
TOKEN_USER_HSET = "token_user" 


class redis_client(object):

    def __init__(self, db_name) -> None:
        parts = urllib.parse.urlparse(settings.redis)
        assert parts.scheme == 'redis'
        host, port = parts.netloc.split(':')
        print(f"host: {host}, port: {port}")
        self.client = redis.Redis(host=host, port=int(port), db=REDIS_DB_NAMES[db_name])

    def set(self, key, val):
        self.client.set(key, val)

    def get_str(self, key):
        val = self.client.get(key)
        return val.decode('utf-8') if val is not None else val

    def hset(self, set_name, key, val) -> None:
        self.client.hset(set_name, key, val)

    def hget(self, set_name, key) -> str:
        val = self.client.hget(set_name, key)
        return val.decode('utf-8') if val is not None else val

    def hdel(self, set_name, key):
        self.client.hdel(set_name, key)

    def get_redis_obj(self):
        self.client


def get_redis_client(redis_db_name):
    parts = urllib.parse.urlparse(settings.redis)
    assert parts.scheme == 'redis'
    host, port = parts.netloc.split(':')
    return redis.Redis(host=host, port=int(port), db=REDIS_DB_NAMES[redis_db_name])


def get_redis_lock(lock_name, expire=1):
    redis_obj = get_redis_client(LOCK_DB)
    return redis_lock.Lock(redis_obj, lock_name, expire)


REDIS_DB_NAMES = {
    AUTH_DB: 0,
    LOCK_DB: 1
}
