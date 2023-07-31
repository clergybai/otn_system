from ..models.user import User
from datetime import datetime
from common.utils.crypto_helper import Md5Generator
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


def add_user(user_info):
    encrypt_salt = Md5Generator.md5(user_info['salt'])
    User.add_user(
        user_name=user_info['user_name'],
        name=user_info['name'],
        salt=encrypt_salt,
        user_email=user_info['user_email'],
        cellphone_num=user_info['cellphone_num'],
        city=user_info['city'],
        role=int(user_info['role']),
        department=user_info['department'],
        post=user_info['post'],
        remark=user_info['remark'],
        is_active=1, last_update_person=user_info['last_update_person'])


def remove_user(user_info):
    return User.update_user(user_name=user_info['user_name'],
                            is_active=0, update_time=datetime.now(),
                            last_update_person=user_info['last_update_person'])


def edit_user(user_info):
    return User.update_user(user_name=user_info['user_name'],
                            name=user_info['name'], user_email=user_info['user_email'],
                            cellphone_num=user_info['cellphone_num'],
                            department=user_info['department'],
                            post=user_info['post'],
                            remark=user_info['remark'],
                            update_time=datetime.now(),
                            last_update_person=user_info['last_update_person'])


def pwd_update(info):
    encrypt_salt = Md5Generator.md5(info["salt"])
    return User.update_user(user_name=info["userName"],
                            salt=encrypt_salt)
