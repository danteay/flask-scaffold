
"""Mongo Client creation"""

import re
from contextlib import ContextDecorator

import pymongo
from pymongo.errors import ConnectionFailure

from src.commons.logging import logger
from src.commons.errors import DuplicationError
from src.config import load

CONFIG = load()


class Mongo(ContextDecorator):
    """Mongo connection Class"""

    def __init__(self):
        self._database = CONFIG["MONGO_DB"]
        self._url = CONFIG["MONGO_URL"]

        logger.fields({
            "url": self._url,
            "database": self._database
        }).debug("connect mongo _database")

        self._connection = pymongo.MongoClient(self._url)
        self.ping()

    def __enter__(self):
        """Enter as context"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closing context"""
        self._connection.close()

    def ping(self):
        """Check database Connection"""
        res = self._connection[self._database].command("ping")

        if res["ok"] != 1.0:
            raise ConnectionFailure("unhealthy database connection")

    def use_database(self, database: str):
        """
        Set database or change for other
        :param database: Database to use on connection
        """

        self._database = database

    def count(self, collection: str, filters: dict = None):
        """
        Count all matching documents
        :param collection: Mongo collection name
        :param filters: Mongo query to be executed
        :return: Total of documents
        """

        try:
            search = self._connection[self._database][collection]

            if filters:
                total = search.find(filters).count()
            else:
                total = search.find().count()

            return total
        except Exception as error:
            raise self._process_errors(error)

    def find_one(self, collection: str, filters: dict):
        """
        Find first element of a query in a specific collection
        :param collection: Mongo collection name
        :param filters: Mongo query to be executed
        :return: Found document or None
        """

        return self._connection[self._database][collection].find_one(filters)

    def find_many(
        self,
        collection: str,
        filters: dict,
        order_by: str = None,
        order: str = None,
        limit: str = None,
        offset: str = None
    ):
        """
        Find all documents by filtering params
        :param collection: Mongo collection name
        :param filters: Mongo query to be executed
        :param order_by: Order data by a specific field
        :param order: order type ascending (1) or descending (-1)
        :param limit: Number or retrieved documents for the query
        :param offset: Number of omitted documents before the result
        :return: Found documents or None
        """

        try:
            find = self._connection[self._database][collection].find(filters)

            if order_by:
                if order:
                    find = find.sort(order_by, order)
                else:
                    find = find.sort(order_by)

            if offset:
                find = find.skip(offset)

            if limit:
                find = find.limit(limit)

            return find
        except Exception as error:
            raise self._process_errors(error)

    def insert_one(self, collection: str, data: dict):
        """
        Insert a document into a collection
        :param collection: Mongo collection name
        :param data: Document data to be inserted
        :return: Inserted ID
        """

        try:
            return self._connection[self._database][collection].insert(data)
        except Exception as error:
            raise self._process_errors(error)

    def insert_many(self, collection: str, data: dict):
        """
        Insert many documents into a collection
        :param collection: Mongo collection name
        :param data: Document data to be inserted
        :return: Inserted IDs
        """

        try:
            return self._connection[self._database][collection].insert_many(data).inserted_ids
        except Exception as error:
            raise self._process_errors(error)

    def update_many(self, collection: str, filters: dict, new_data: dict):
        """
        Update many documents of a collection by given filters
        :param collection: Mongo collection name
        :param filters: Mongo query to match document
        :param new_data: New data to update
        """

        try:
            return self._connection[self._database][collection] \
                .update_many(filters, new_data).modified_count
        except Exception as error:
            raise self._process_errors(error)

    def update_one(self, collection: str, filters: dict, new_data: dict):
        """
        Update one document of a collection by given filters
        :param collection: Mongo collection name
        :param filters: Mongo query to match document
        :param new_data: New data to update
        """

        try:
            return self._connection[self._database][collection] \
                .update_one(filters, new_data).modified_count
        except Exception as error:
            raise self._process_errors(error)

    def delete_many(self, collection: str, filters: dict):
        """
        Update one document of a collection by given filters
        :param collection: Mongo collection name
        :param filters: Mongo query to match document
        """
        try:
            deletes = self._connection[self._database][collection].delete_many(filters)
            return deletes.deleted_count
        except Exception as error:
            raise self._process_errors(error)

    def delete_one(self, collection: str, filters: dict):
        """
        Delete a single document matching filters
        :param collection: Mongo collection name
        :param filters: Mongo query to be executed
        """

        self._connection[self._database][collection].delete_one(filters)

    @staticmethod
    def _process_errors(error: Exception):
        """
        Get Database errors and transform into handler errors
        :param error: Error to process
        :raise: HandlerError
        """

        if re.search("E11000", error.args[0]):
            raise DuplicationError()

        raise error
