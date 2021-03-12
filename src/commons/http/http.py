"""Http common functions"""

import http.client
import decimal
import json as jsonb

from flask import Response

from src.commons.errors import HandlerError
from src.commons.logging import logger
from src.config import load

CONFIG = load()


def json(code: int = 200, body: dict = None, error=None, headers: dict = None):
    """
    Http JSON lambda response
    :param code: Http response code
    :param body: Response json body
    :param error: Possible error on response body
    :param headers: Response headers
    :return: Chalice response
    """

    if not body:
        body = {}

    if not headers:
        headers = {}

    if error is not None:
        error_code, error_message, root_causes = _process_error(code, error)
        body["error"] = error_code
        body["message"] = error_message
        body["root_causes"] = root_causes

    logger.field("res", body)

    if "error" in body and body["error"] is not None:
        logger.error("handled request", error=body["error"])
    else:
        logger.info("handled request")

    headers["Content-Type"] = "application/json"

    return response(code=code, body=_build_json(body), headers=headers)


def json_error(error, headers: dict = None):
    """
    Respond with an standard XML error description
    :param error: Possible error to handle
    :param headers: Add extra response headers
    """

    if not headers:
        headers = {}

    if isinstance(error, HandlerError):
        return json(code=error.get_code(), error=error, headers=headers)

    return json(code=500, error=error, headers=headers)


def response(code: int = 200, body: (str, dict) = None, headers: dict = None):
    """
    Http lambda response formatting
    :param code: Http response code
    :param body: Response json body
    :param headers: Response headers
    :return: Chalice response
    """

    if not headers:
        headers = {}

    if "CORS" in CONFIG.keys() and str(CONFIG["CORS"]).lower() == "true":
        headers.update(cors_headers())

    return Response(response=body, headers=headers, status=code)


def get_error_from_code(code):
    """
    Transform http status code into a standard error message
    :param code: HTTP status code
    """
    error = http.client.responses[code]
    error = error.lower().replace(" ", "-")
    return error


def cors_headers():
    """
    Add cors headers to response headers
    :return: new headers dict
    """

    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
    }


def _process_error(status_code, error):
    """
    Get proper messages from errors according his name
    :param status_code: Current status code of the handled error
    :param error: Error to be handled
    :return: tuple of error code and error message
    """

    if isinstance(error, HandlerError):
        code = error.get_message()
        message = error.get_description()
        root_causes = error.get_root_causes()
    else:
        code = get_error_from_code(status_code)
        message = str(error).replace("\n", "")
        root_causes = None

    return code, message, root_causes


def _handle_extra_types(obj):
    """
    Monkey patch function to support json serialization response of not known types by Chalice Response object
    :param obj: Object data to serialize
    :return: Serialized value
    """

    # Lambda will automatically serialize decimals so we need
    # to support that as well.
    if isinstance(obj, decimal.Decimal):
        return float(obj)

    try:
        return str(obj)
    except Exception as err:
        raise TypeError(
            'Object of name %s is not JSON serializable' % obj.__class__.__name__
        ) from err


def _build_json(data):
    """
    Serialize object as JSON string
    :param data: Data to be serialized
    :return: JSON string
    """

    return jsonb.dumps(data, default=_handle_extra_types)
