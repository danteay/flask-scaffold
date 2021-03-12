"""Prices routes"""

from flask import Blueprint

import src.commons.utils as utils
import src.commons.http as http

router = Blueprint("ping", __name__)


@router.route("/ping", methods=["GET"])
def get_prices():
    """Obtain the price calculations"""

    try:
        _, _ = utils.prepare_request_data()
        return http.json(body={"data": "pong"})
    except Exception as err:
        return http.json_error(err)
