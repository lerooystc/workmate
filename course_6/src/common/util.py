from datetime import datetime
import hashlib
from typing import Any, Callable, Optional

from fastapi import Request, Response

from src.config import settings
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


def no_db_session_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> str:
    # remove db from kwargs so that it's not included in the cache key
    kwargs.pop("db")
    cache_key = hashlib.md5(
        f"{func.__module__}:{func.__name__}:{args}:{kwargs}".encode()
    ).hexdigest()  # noqa: S324
    return f"{namespace}:{cache_key}"
