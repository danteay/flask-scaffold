"""Swagger path configuration"""

import os
import pathlib

from flask import Blueprint, render_template, Response
from jinja2 import TemplateNotFound

from src.commons.logging import logger

router = Blueprint('swagger', __name__, template_folder='templates')


@router.route('/.swagger', methods=["GET"])
def swagger():
    """Render Swagger UI"""

    try:
        return render_template('index.html')
    except TemplateNotFound as err:
        logger.err(err).warning("template not found")
        return Response(status=404)


@router.route("/.swagger/<file>", methods=["GET"])
def swagger_file(file: str):
    """Return Swagger JSON specification"""

    path = pathlib.Path(__file__).parent.absolute()
    full_path = f"{path}/openapi/{file}"

    if not os.path.exists(full_path):
        Response(status=404)

    with open(full_path) as file_open:
        swagger_data = file_open.read()

    return Response(response=swagger_data, headers={"Content-Type": "application/json"}, status=200)
