"""Logging bootstrapping"""

import logging

from elasticlogger import Logger
from src.config import load

CONFIG = load()

if "LOG_LEVEL" not in CONFIG:
    LEVEL = logging.INFO
else:
    if CONFIG["LOG_LEVEL"].upper() == "DEBUG":
        LEVEL = logging.DEBUG
    elif CONFIG["LOG_LEVEL"].upper() == "INFO":
        LEVEL = logging.INFO
    elif CONFIG["LOG_LEVEL"].upper() == "WARNING":
        LEVEL = logging.WARNING
    elif CONFIG["LOG_LEVEL"].upper() == "ERROR":
        LEVEL = logging.ERROR
    else:
        LEVEL = logging.INFO

LOGGER = Logger(CONFIG["APP_NAME"], level=LEVEL)

if "ELASTIC_URL" in CONFIG and "ELASTIC_INDEX" in CONFIG:
    LOGGER.enable_elastic(url=CONFIG["ELASTIC_URL"], index=CONFIG["ELASTIC_INDEX"])

if "SENTRY_URL" in CONFIG:
    LOGGER.enable_sentry(url=CONFIG["SENTRY_URL"], level=LEVEL)


def config_logs():
    """Bootstrap logger configuration options"""
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    LOGGER.logger.propagate = False
