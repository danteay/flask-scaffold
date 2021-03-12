"""Redis connection class"""

from contextlib import ContextDecorator

import redis

from src.config import load

CONFIG = load()


class Redis(ContextDecorator):
    """Redis connection class context"""

    def __init__(self):
        redis_db = 0

        if "REDIS_DB" in CONFIG.keys():
            redis_db = int(CONFIG["REDIS_DB"])

        self._connection = redis.Redis(
            host=CONFIG["REDIS_HOST"], password=CONFIG["REDIS_PASS"], db=redis_db
        )

    def __enter__(self):
        """Enter as a context object"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit from context"""
        self._connection.close()

    def get_connection(self):
        """
        Return base connection object
        :return redis.Redis: Connection object
        """

        return self._connection

    def get_value(self, key: str):
        """
        Return one value from the given key
        :param key: Redis stored key
        :return: String value of the key
        """

        value = self._connection.get(key)

        if value is None:
            return None

        return value.decode("utf-8")

    def set_value(self, key: str, value: str, expires_in: int = None):
        """
        Store a key value pair on redis
        :param key: Key of the value
        :param value: Stored value for the given key
        :param expires_in: Expiration time in seconds
        """

        self._connection.set(key, value, ex=expires_in)

    def delete_key(self, key: str):
        """
        Delete some stored value in redis
        :param key: Key name to be deleted
        """

        self._connection.delete(key)

    def get_all_values(self):
        """
        Return a dict with all key value pairs stored on redis
        :return: dict with all redis values
        """

        keys = self._connection.keys("*")

        all_values = []

        for key in keys:
            all_values[key] = self.get_value(key)

        return all_values
