"""holidays adapter functions"""

from datetime import date

from src.commons.drivers.sqlite import SQLite
from src.repositories import HolidaysRepository


def is_holiday(lift_date: date):
    """
    Validate if a given date is a marked holiday
    :param lift_date: Lift date
    :return boolean: assertion
    """

    with SQLite() as database:
        holiday = HolidaysRepository.find_by_date(database=database, date=lift_date)

    if holiday is None:
        return False

    return True
