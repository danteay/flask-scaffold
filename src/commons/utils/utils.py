"""Common utilities"""

import os
import uuid
from base64 import urlsafe_b64encode
from xml.etree import ElementTree
from xml.etree.ElementTree import SubElement
from xml.dom import minidom

import datetime
import requests
import fastjsonschema
from flask import request

import src.commons.context as context
from src.commons.errors import SchemaError, HandlerError
from src.commons.logging import logger
from src.config import load

CONFIG = load()


def short_id(length: int = 6):
    """
    Generate and return a short ID of N chars between 6 and 50
    :param length: total of characters of the short_id
    :return: Short ID string
    """

    if length < 6:
        length = 6

    if length > 50:
        length = 50

    rand = urlsafe_b64encode(os.urandom(100)).decode("utf-8").upper()
    rand = rand.replace("-", "").replace("_", "").replace("=", "")
    return rand[0:length]


def store_trace_id(headers):
    """
    Search for TraceId header and store it as global configuration for be used on all logs as part of the context
    :param headers: List of request headers
    """

    trace_id = headers.get("Trace-Id", None)

    if not trace_id:
        trace_id = str(uuid.uuid4())

    logger.context.field("trace_id", trace_id)
    context.set_value("trace_id", trace_id)


def prepare_request_data(schema: dict = None):
    """
    Process al request data, store trace_id in logger context and return request body
    :param schema: JSON schema definition to validate body
    :return: JSON request
    :raise: HandlerError if process fail
    """

    body = request.json
    query = dict(request.args)

    if schema is not None:
        body = validate_json_schema(data=body, schema=schema)

    store_trace_id(request.headers)

    if not body:
        body = {}

    if not query:
        query = {}

    return body, query


def validate_json_schema(data: dict, schema: dict):
    """
    Validate JSON request payload with a given JSON schema
    :param data: JSON request data
    :param schema: JSON schema definition
    """

    try:
        validate = fastjsonschema.compile(schema)
        return validate(data)
    except Exception as err:
        raise SchemaError(err) from err


def call_service(
    method: str,
    resource: str,
    headers: dict = None,
    json: dict = None,
    params: dict = None,
    service_name: str = None,
):
    """
    Generic call service to avoid code duplication
    :param method: Request method GET, POST, PUT or DELETE
    :param resource: Resource service endpoint
    :param headers: Request headers
    :param json: JSON body for the request
    :param params: URL params data on the request
    :param service_name: Name of the service that will be called
    :return: Tuple of status code and json response
    :raise: HandlerError if status code is not 200, 201 or 202
    """

    if service_name is None:
        service_name = "External.service"

    options = _build_request_options(method, resource, headers, json, params)

    logger.field("service", service_name).fields(options).debug("calling service")

    res = _execute_request(method, options)
    json_res = res.json()

    if res.status_code in {200, 201, 202}:
        return res.status_code, json_res

    logger.fields({
        "service": service_name,
        "status_code": res.status_code,
        "resp": json_res
    }).error("service call error")

    root_cause = f"Error calling {service_name}"

    if json_res["root_causes"] is None:
        json_res["root_causes"] = []

    json_res["root_causes"].append({"error": root_cause})

    raise HandlerError(
        code=res.status_code,
        message=json_res["error"],
        description=json_res["message"],
        root_causes=json_res["root_causes"]
    )


def _build_request_options(
    method: str, resource: str, headers: dict = None, json: dict = None, params: dict = None
):
    """
    Validate configs and build request options
    :param method: Request method GET, POST, PUT or DELETE
    :param resource: Resource service endpoint
    :param headers: Request headers
    :param json: JSON body for the request
    :param params: URL params data on the request
    :return: request options dict
    """

    if not headers:
        headers = {}

    headers.update({"Trace-Id": context.get_value("trace_id")})

    method = method.upper()

    if method not in {"GET", "POST", "PUT", "DELETE"}:
        raise requests.exceptions.RequestException("invalid request method")

    options = {
        "url": resource,
        "headers": headers,
    }

    if json is not None and method in {"POST", "PUT", "DELETE"}:
        options["json"] = json

    if params is not None and method == "GET":
        options["params"] = params

    return options


def _execute_request(method: str, options: dict):
    """
    Execute requests library call to any REST service configured
    :param method: HTTP request method to execute call
    :param options: Configured options for the call
    :return: requests library response
    """

    method = method.upper()

    if method == "GET":
        return requests.get(**options)

    if method == "POST":
        return requests.post(**options)

    if method == "PUT":
        return requests.put(**options)

    if method == "DELETE":
        return requests.delete(**options)

    raise requests.exceptions.RequestException("invalid request method")


def prettify_xml(elem: ElementTree):
    """
    Return a pretty-printed XML string for the Element
    :param elem: Root xml element to prettify
    :return: Formatted XML string
    """

    rough_string = ElementTree.tostring(elem, 'utf-8')
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent="  ")


def error_xml(message: str, description: str, root_cause: (str, list) = None):
    """
    Generate an xml payload response with error data
    :param message: Error message code
    :param description: Error description
    :param root_cause: Error root causes and explanations
    """

    error = ElementTree.Element("error")

    sub_message = SubElement(error, 'message')
    sub_message.text = message

    sub_description = SubElement(error, 'description')
    sub_description.text = description

    if root_cause:
        sub_causes = SubElement(error, 'root_causes')
        build_xml_root_causes(root_cause, sub_causes)

    return error


def build_xml_root_causes(root_cause: (str, dict, list), parent: SubElement):
    """
    Build error root causes as XML response
    :param root_cause: Error root causes
    :param parent: Parent xml element to attach root causes
    """

    if isinstance(root_cause, dict):
        _ = SubElement(parent, 'cause', root_cause)
        return

    if isinstance(root_cause, list):
        for cause in root_cause:
            if isinstance(cause, dict):
                _ = SubElement(parent, "cause", cause)
            else:
                _cause = SubElement(parent, "cause")
                _cause.text = str(cause)

        return

    _cause = SubElement(parent, "cause")
    _cause.text = str(root_cause)


def str_to_datetime(date: str):
    """
    Convert a string date into a datetime object
    :param date: String date of formats '%Y-%m-%d' or '%Y-%m-%d %H:%M:%S'
    :return datetime:
    """

    formats = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S']

    for date_format in formats:
        try:
            return datetime.datetime.strptime(date, date_format)
        except Exception:
            continue

    raise ValueError("String date should be one if the following formats: %s" % str(formats))
