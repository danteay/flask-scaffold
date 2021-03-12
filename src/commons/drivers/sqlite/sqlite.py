"""Sqlite connection class"""

import pathlib
import sqlite3
from contextlib import ContextDecorator

from src.commons.logging import logger
from src.config import load

CONFIG = load()


class SQLite(ContextDecorator):
    """SQLite Context class"""

    DATA_PATH = pathlib.Path(__file__).parent.absolute()

    def __init__(self):
        self._database = f"{self.DATA_PATH}/../../../../{CONFIG['SQLITE_FILE']}"
        self._commit = str(CONFIG["SQLITE_COMMIT"]).lower() == "true"

        self._connection = sqlite3.connect(self._database)
        self._cursor = self._connection.cursor()

    def __enter__(self):
        """
        Return object context
        :return: Self instance
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Terminate context object"""
        self.close()

    def query(self, query: str, *args):
        """
        Execute a query and return all values
        :param query: SQL query statement
        :return: list
        """

        logger.fields({"query": query, "query_args": args}).debug("executing query")

        self._cursor.execute(query, args)

        if self._commit:
            self._connection.commit()

        return self._cursor.fetchall()

    def query_one(self, query: str, *args):
        """
        Execute a query and return just the first result
        :param query: SQL query statement
        :return: list
        """

        logger.fields({"query": query, "query_args": args}).debug("executing query_one")

        self._cursor.execute(query, args)

        if self._commit:
            self._connection.commit()

        return self._cursor.fetchone()

    def query_none(self, query: str, *args):
        """
        Execute a query and do not return any result value
        :param query: SQL query statement
        """

        logger.fields({"query": query, "query_args": args}).debug("executing query_none")

        self._cursor.execute(query, args)

        if self._commit:
            self._connection.commit()

    def last_added_id(self):
        """return the last inserted ID by a query"""
        return self._cursor.lastrowid

    def close(self):
        """Close current connection"""
        self._cursor.close()
        self._connection.close()
