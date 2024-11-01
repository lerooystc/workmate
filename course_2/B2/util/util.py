from datetime import datetime

from dateutil import rrule

TO_REMOVE = [
    "Unnamed: 0",
    "Unnamed: 6",
    "Unnamed: 7",
    "Unnamed: 8",
    "Unnamed: 9",
    "Unnamed: 10",
    "Unnamed: 11",
    "Unnamed: 12",
    "Unnamed: 13",
]

COLUMN_NAMES = [
    "exchange_product_id",
    "exchange_product_name",
    "delivery_basis_name",
    "volume",
    "total",
    "count",
]


class DeadLinkException(Exception):
    pass


def date_to_link(date: datetime) -> str:
    formatted_date = date.strftime("%Y%m%d")
    return f"https://spimex.com/upload/reports/oil_xls/\
        oil_xls_{formatted_date}162000.xls"


def range_to_links(date_start: datetime, date_end: datetime) -> set[str]:
    links = set()
    for dt in rrule.rrule(rrule.DAILY, dtstart=date_start, until=date_end):
        formatted_date = dt.strftime("%Y%m%d")
        links.add(
            f"https://spimex.com/upload/reports/oil_xls/\
            oil_xls_{formatted_date}162000.xls"
        )
    return links
