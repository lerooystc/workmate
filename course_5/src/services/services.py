import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from datetime import date
from datetime import datetime
from functools import partial
from typing import List
from typing import Optional

import pandas as pd
from common.const import COLUMN_NAMES
from common.const import TO_REMOVE
from common.exceptions import DeadLinkException
from common.util import date_to_link
from common.util import range_to_links
from db.models import Trade
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


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


async def async_upload_trades(date: datetime, session: AsyncSession) -> bool:
    """
    Асинхронный сервис обработки данных о продажах для одного дня.

    :param date: Дата торгов.
    :param session: Сессия БД.
    """
    url = date_to_link(date)
    df = process_sheet_handler(url)
    async with session.begin():
        trades = [Trade(**row.to_dict()) for _, row in df.iterrows()]
        session.add_all(trades)
    await session.commit()
    return True


async def async_bulk_upload_trades(
    date_start: datetime, date_end: datetime, session: AsyncSession
) -> float:
    """
    Асинхронный сервис обработки данных о продажах для диапазона дат.

    :param date_start: Дата начала торгов.
    :param date_end: Дата начала торгов.
    :param session: Сессия БД.
    """
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
    return True


async def get_trading_dates(days: int, session: AsyncSession) -> list[date]:
    """
    Сервис получения последних дат.

    :param days: Кол-во дней, которые требуется получить.
    :param session: Сессия БД.
    """
    stmt = select(Trade.date).distinct().order_by(Trade.date.desc()).limit(days)
    results = await session.execute(stmt)
    return results.scalars().all()


async def get_trades(
    session: AsyncSession,
    oil_id: Optional[str],
    delivery_type_id: Optional[str],
    delivery_basis_id: Optional[str],
    limit: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> list[Trade]:
    """
    Сервис получения торгов.

    :param session: Сессия БД.
    :param oil_id: Опциональный фильтр по id нефти.
    :param delivery_type_id: Опциональный фильтр по id типа доставки.
    :param delivery_basis_id: Опциональный фильтр по id базиса доставки.
    :param limit: Опциональный лимитер.
    :param start_date: Опциональный фильтр по дате торгов (начало).
    :param end_date: Опциональный фильтр по дате торгов (конец).
    """
    stmt = select(Trade).order_by(Trade.date.desc())
    if start_date and end_date:
        stmt = stmt.filter(Trade.date >= start_date, Trade.date <= end_date)
    if oil_id:
        stmt = stmt.filter(Trade.oil_id == oil_id)
    if delivery_type_id:
        stmt = stmt.filter(Trade.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        stmt = stmt.filter(Trade.delivery_basis_id == delivery_basis_id)
    if limit:
        stmt = stmt.limit(limit)
    results = await session.execute(stmt)
    return results.scalars().all()
