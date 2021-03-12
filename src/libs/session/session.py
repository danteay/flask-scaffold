"""Session configuration"""

from flask import Flask, session
from flask.ext.session import Session

import src.commons.context as context
from src.commons.drivers import Redis


def setup_session(app: Flask):
    """
    Setup session extension manager
    :param app: Flask base application
    """

    app.config["SESSION_TYPE"] = "redis"
    app.config["SESSION_REDIS"] = Redis().get_connection()

    context.set_value("session", Session(app))


def set_value(key: str, value: str):
    """
    Set new session value
    :param key: Key identifier of the value
    :param value: corresponding value of the key
    """
    session[key] = value


def get_value(key: str):
    """
    Get stored session value
    :param key: request stored key
    :return str: corresponding value
    """
    return session[key]
