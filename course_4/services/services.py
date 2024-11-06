import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from functools import partial
from time import perf_counter
from typing import List

import pandas as pd
from common.const import COLUMN_NAMES
from common.const import TO_REMOVE
from common.exceptions import DeadLinkException
from common.util import date_to_link
from common.util import range_to_links
from db.models import Trade
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


def process_sheet(url: str) -> pd.DataFrame:
    """
    Производит перевод .xls файла в Pandas DataFrame.

    :param url: URL .xls файла.
    """
    try:
        df: pd.DataFrame = pd.read_excel(url)
    except Exception:
        print(url)
        raise DeadLinkException
    trades_date = datetime.strptime(df.iloc[2]["Форма СЭТ-БТ"][-10:], "%d.%m.%Y")
    index = df[df["Форма СЭТ-БТ"] == "Единица измерения: Метрическая тонна"].index[0]
    df.drop(index=df.index[: index + 3], inplace=True)
    df.drop(TO_REMOVE, axis=1, inplace=True)
    df.columns = COLUMN_NAMES
    df.drop(df[df["count"] == "-"].index, inplace=True)
    df.drop(df.tail(2).index, inplace=True)
    df = df[df["delivery_basis_name"].notna()]
    df["oil_id"] = df["exchange_product_id"].str[:4]
    df["delivery_basis_id"] = df["exchange_product_id"].str[4:7]
    df["delivery_type_id"] = df["exchange_product_id"].str[-1]
    df["count"] = pd.to_numeric(df["count"])
    df["volume"] = pd.to_numeric(df["volume"])
    df["total"] = pd.to_numeric(df["total"])
    df["date"] = trades_date
    return df


def process_sheet_handler(url: str) -> pd.DataFrame | None:
    """
    Оборот для функции process_sheet, возвращающий None в случае мертвой ссылки.

    :param url: URL .xls файла.
    """
    try:
        df = process_sheet(url)
        return df
    except DeadLinkException:
        return None


def sync_upload_trades(date: datetime, session: Session) -> float:
    """
    Синхронный сервис обработки данных о продажах для одного дня.

    :param date: Дата торгов.
    :param session: Сессия БД.
    """
    s = perf_counter()
    url = date_to_link(date)
    df = process_sheet_handler(url)
    trades = [Trade(**row.to_dict()) for _, row in df.iterrows()]
    session.add_all(trades)
    session.commit()
    return perf_counter() - s


async def async_upload_trades(date: datetime, session: AsyncSession) -> float:
    """
    Асинхронный сервис обработки данных о продажах для одного дня.

    :param date: Дата торгов.
    :param session: Сессия БД.
    """
    s = perf_counter()
    url = date_to_link(date)
    df = process_sheet_handler(url)
    async with session.begin():
        trades = [Trade(**row.to_dict()) for _, row in df.iterrows()]
        session.add_all(trades)
    await session.commit()
    return perf_counter() - s


async def async_bulk_upload_trades(
    date_start: datetime, date_end: datetime, session: AsyncSession
) -> float:
    """
    Асинхронный сервис обработки данных о продажах для диапазона дат.

    :param date_start: Дата начала торгов.
    :param date_end: Дата начала торгов.
    :param session: Сессия БД.
    """
    s = perf_counter()
    url_set = range_to_links(date_start, date_end)
    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        calls: List[partial[str]] = [
            partial(process_sheet_handler, url) for url in url_set
        ]
        call_coros = [loop.run_in_executor(process_pool, call) for call in calls]
        done, _ = await asyncio.wait(call_coros)
        for done_task in done:
            df = await done_task
            async with session.begin():
                if df is not None:
                    trades = [Trade(**row.to_dict()) for _, row in df.iterrows()]
                    session.add_all(trades)
    await session.commit()
    return perf_counter() - s


def sync_bulk_upload_trades(
    date_start: datetime, date_end: datetime, session: Session
) -> float:
    """
    Синхронный сервис обработки данных о продажах для диапазона дат.

    :param date_start: Дата начала торгов.
    :param date_end: Дата начала торгов.
    :param session: Сессия БД.
    """
    s = perf_counter()
    url_set = range_to_links(date_start, date_end)
    for url in url_set:
        df = process_sheet_handler(url)
        if df is not None:
            trades = [Trade(**row.to_dict()) for _, row in df.iterrows()]
            session.add_all(trades)
    session.commit()
    return perf_counter() - s
