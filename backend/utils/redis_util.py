# -*- coding: utf-8 -*-
# @Time    : 2019/2/20 17:51
# @Author  : Lin Weixin
# @File    : redis_utils.py
# @Software: PyCharm
# @Descrption: 新增Redis的通用函数，包括加锁和解锁

import pickle
import time
import zlib
from io import StringIO

import pandas as pd

from fuadmin.settings import redis_conn

# 存储
def send_to_redis(key, value):
    redis_conn.set(key, value)
    pass


# 读取
def read_from_redis(key):
    value = redis_conn.get(key)
    return value


# 加分布式锁
def lock(lock_key, timeout=1):
    redis_lock = 0
    while redis_lock != 1:
        timestamp = time.time() + timeout
        redis_lock = redis_conn.setnx(lock_key, timestamp)
        if redis_lock == 1:
            # get lock because free
            break
        lock_value = redis_conn.get(lock_key)
        if lock_value and time.time() > float(lock_value) and time.time() > float(
                redis_conn.getset(lock_key, timestamp)):
            # get lock because timeout
            break
        time.sleep(0.3)
    pass


# 释放分布式锁
def release(lock_key):
    lock_value = redis_conn.get(lock_key)
    if lock_value and time.time() < float(lock_value):
        # release lock if still locked
        redis_conn.delete(lock_key)
    pass


def redis_dlm(lock_key, timeout=1):
    """
    分布式锁-decorator模式
    :param lock_key: 锁名称
    :param timeout: 锁超时时间，默认1s
    """

    def _deco(func):
        def __deco(*args, **kwargs):
            lock(lock_key, timeout=timeout)
            try:
                return func(*args, **kwargs)
            finally:
                release(lock_key)

        return __deco

    return _deco


def read_map_from_redis(key):
    '''
    从redis中读取hashmap数据
    :param key:
    :return:
    '''
    map = redis_conn.hgetall(key)
    return map


def send_df_to_redis(df, key):
    '''
    将df转换为csv流存入redis中
    以csv流存入redis中是为了防止数值类型的Nan数据读出来是类型变为字符串'Nan'

    :param df:
    :param key:
    :return:
    '''
    if not df.empty:
        csv_str = df.to_csv(encoding='utf-8', index=False)
        send_to_redis(key, csv_str)


def get_csv_from_redis(key):
    '''
    将csv流读出来转换为df

    :param key:
    :return:
    '''
    str = read_from_redis(key)
    if str:
        csv_str = StringIO(str)
        df = pd.read_csv(csv_str, encoding='utf-8')
    else:
        df = pd.DataFrame()
    return df


def read_map_value_from_redis(key, map_key):
    '''从redis中读取hashmap某个map中的一个value

    :param key: redis的key
    :param map_key: map的key
    :return:
    '''
    value = redis_conn.hget(key, map_key)
    return value


def send_map_value_to_redis(key, map_key, value):
    """将value存到redis的map中

    :param key:
    :param map_key:
    :param value:
    :return:
    """
    return redis_conn.hset(key, map_key, value)


def send_list_map_to_redis(key, mapping):
    """将mapping批量存入到redis的map中

    :param key:
    :param mapping:
    :return:
    """
    return redis_conn.hmset(key, mapping)


def save_df(df, key, map_key):
    """
    # 通过pickle完美实现redis读写pandas对象，df存取后df2和原df： df.equals(df2) >> True
    # 如有异常联系niuzhiyao
    :param df:
    :param key:
    :param map_key:
    :return:
    """
    bytes = zlib.compress(pickle.dumps(df), 5)
    redis_conn.hset(key, map_key, bytes)
    return 1


def read_df(key, map_key):
    bytes = redis_conn.hget(key, map_key)
    df = pickle.loads(zlib.decompress(bytes)) if bytes else pd.DataFrame()
    return df


def save_str(mystr, key, map_key):
    '''
    把字符串存入redis
    :param mystr: 字符串类型
    :param key:
    :param map_key:
    :return:
    '''
    redis_conn.hset(key, map_key, mystr)
    return 1
