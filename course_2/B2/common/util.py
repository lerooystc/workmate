from datetime import datetime

from config import settings
from dateutil import rrule


def date_to_link(date: datetime) -> str:
    formatted_date = date.strftime("%Y%m%d")
    return settings.SPIMEX_URL + settings.SPIMEX_EXCEL_URL.format(formatted_date)


def range_to_links(date_start: datetime, date_end: datetime) -> set[str]:
    links = set()
    for dt in rrule.rrule(rrule.DAILY, dtstart=date_start, until=date_end):
        formatted_date = dt.strftime("%Y%m%d")
        links.add(
            settings.SPIMEX_URL + settings.SPIMEX_EXCEL_URL.format(formatted_date)
        )
    return links
