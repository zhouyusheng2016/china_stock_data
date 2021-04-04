from dbutils.pooled_db import PooledDB
from mysql import connector
from .config import login


class DBPool(object):

    __pool = None
    if __pool is None:
        __pool = PooledDB(**login, creator=connector, mincached=1, maxcached=20)

    @classmethod
    def get_connection(cls):
        return cls.__pool.connection()

    @classmethod
    def close(cls):
        cls.__pool.close()

