from ..models.user import User
from common.redis import (
    redis_client, USER_TOKEN_HSET, TOKEN_USER_HSET, AUTH_DB,
    get_redis_lock)


def cache_user_token(username: str, token: str):
    redcli = redis_client(AUTH_DB)
    # check if old cache existed
    lock_name = f"username_{username}"
    lock = get_redis_lock(lock_name)
    if lock.acquire(False):
        try:
            old_token = redcli.hget(USER_TOKEN_HSET, username)
            if old_token:
                # if token existed, del token_user first
                redcli.hdel(TOKEN_USER_HSET, old_token)
            redcli.hset(USER_TOKEN_HSET, username, token)
            redcli.hset(TOKEN_USER_HSET, token, username)
        finally:
            lock.release()


def get_all_userinfos(**kwargs):
    return User.get_users(**kwargs)
