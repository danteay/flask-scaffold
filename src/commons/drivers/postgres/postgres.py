"""Postgres database connection class"""

from contextlib import ContextDecorator

import psycopg2

from src.config import load

CONFIG = load()


class Postgres(ContextDecorator):
    """Postgres connection manager"""

    def __init__(self):
        self._conn = psycopg2.connect(CONFIG["DATABASE_URL"])
        self._conn.autocommit = str(CONFIG["DATABASE_COMMIT"]).lower() == "true"
        self._cursor = self._conn.cursor()

    def __enter__(self):
        """
        Enter as context class
        :return: Self instance
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit from context mode"""
        self.close()

    def query(self, query: str):
        """
        Execute a query and return all values
        :param query: SQL query statement
        :return: list
        """

        self._cursor.execute(query)
        return self._cursor.fetchall()

    def query_one(self, query: str):
        """
        Execute a query and return just the first result
        :param query: SQL query statement
        :return: list
        """

        self._cursor.execute(query)
        return self._cursor.fetchone()

    def query_none(self, query: str):
        """
        Execute a query and do not return any result value
        :param query: SQL query statement
        """

        self._cursor.execute(query)

    def close(self):
        """Close database connection"""
        self._cursor.close()
        self._conn.close()
