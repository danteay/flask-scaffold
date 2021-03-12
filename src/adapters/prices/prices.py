"""Prices adapter actions"""

from src.commons.drivers.sqlite import SQLite
from src.commons.errors import InvalidPriceTypeError
from src.repositories import PricesRepository


def find_price(lift_type: str):
    """
    Get some Price record by his lift name
    :param lift_type: name to be searched
    :return Price: Price model
    """

    with SQLite() as database:
        price = PricesRepository.find_one_by_lift_type(database=database, lift_type=lift_type)

    if price is None:
        raise InvalidPriceTypeError(root_causes=[{"lift_type": lift_type}])

    return price
