"""HTTP API authorizer middleware"""

import re
import functools

from flask import request

import src.commons.utils as utils
import src.commons.http as http
from src.config import load
from src.commons.logging import logger
from src.commons.errors import HandlerError

CONFIG = load()


def bearer_api_key():
    """
    Authorize raw token from Authorization header
    :return: Function response
    """

    def inner(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Middleware function"""

            utils.store_trace_id(request.headers)

            auth_header = request.headers.get("Authorization", None)
            logger.field("auth_header", auth_header).debug("getting authorization header")

            unauthorized = HandlerError(
                code=401,
                message="invalid-credentials",
                description="Invalid authorization credentials",
            )

            if not auth_header:
                unauthorized.root_causes = [{"error": "Empty Authorization header"}]
                return http.json_error(error=unauthorized)

            if re.search("^Bearer", auth_header) is None:
                unauthorized.root_causes = [{"error": "Invalid type of Authorization token"}]
                return http.json_error(error=unauthorized)

            api_key = auth_header.split(" ")[1]

            if api_key != CONFIG["API_KEY"]:
                unauthorized.root_causes = [{"error": "Invalid token"}]
                return http.json_error(error=unauthorized)

            return func(*args, **kwargs)

        return wrapper

    return inner
