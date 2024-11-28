from datetime import datetime
from types import NoneType
import pytest
from pytest_lazy_fixtures import lf
import pandas as pd
from contextlib import nullcontext as does_not_raise

from src.services.services import get_trades, get_trading_dates, process_sheet_handler
from src.common.util import date_to_link, range_to_links
from src.config import settings


@pytest.mark.parametrize(
    "url, res",
    [
        (lf("spimex_response"), pd.DataFrame),
        ("https://randomlinkthatdoesntwork.com", NoneType),
    ],
)
def test_process_sheet_handler(url, res):
    result = process_sheet_handler(url)
    assert isinstance(result, res)


@pytest.mark.parametrize(
    "date, res, expectation",
    [
        (
            datetime(2022, 1, 1),
            settings.SPIMEX_URL + settings.SPIMEX_EXCEL_URL.format("20220101"),
            does_not_raise(),
        ),
        ("2022-01-01", None, pytest.raises(AttributeError)),
    ],
)
def test_date_to_link(date, res, expectation):
    with expectation:
        result = date_to_link(date)
        assert result == res


@pytest.mark.parametrize(
    "date_start, date_end, middle, expectation",
    [
        (
            datetime(2022, 1, 1),
            datetime(2022, 2, 1),
            datetime(2022, 1, 15),
            does_not_raise(),
        ),
        ("2022-01-01", "2022-02-20", "2022-01-15", pytest.raises(AttributeError)),
    ],
)
def test_range_to_link(date_start, date_end, middle, expectation):
    with expectation:
        result = range_to_links(date_start, date_end)
        middle_link = settings.SPIMEX_URL + settings.SPIMEX_EXCEL_URL.format(
            middle.strftime("%Y%m%d")
        )
        assert middle_link in result


@pytest.mark.anyio
async def test_get_trading_dates(async_db, trade_factory):
    await trade_factory(
        oil_id="oil1", delivery_type_id="type1", delivery_basis_id="basis1"
    )
    trading_dates = await get_trading_dates(days=1, session=async_db)
    assert len(trading_dates) == 1


@pytest.mark.anyio
async def test_get_trades_with_filters(async_db, trade_factory):
    trade1 = await trade_factory(
        oil_id="oil1",
        delivery_type_id="type1",
        delivery_basis_id="basis1",
        date=datetime(2022, 1, 1),
    )
    trade2 = await trade_factory(
        oil_id="oil2",
        delivery_type_id="type2",
        delivery_basis_id="basis2",
        date=datetime(2023, 1, 1),
    )

    # Фильтр по oil_id
    trades = await get_trades(session=async_db, oil_id="oil1")
    assert trade1 in trades
    assert trade2 not in trades

    # Фильтр по delivery_type_id
    trades = await get_trades(session=async_db, delivery_type_id="type2")
    assert trade2 in trades
    assert trade1 not in trades

    # Фильтр по delivery_basis_id
    trades = await get_trades(session=async_db, delivery_basis_id="basis1")
    assert trade1 in trades
    assert trade2 not in trades

    # Фильтр по датам
    trades = await get_trades(
        session=async_db, start_date=trade1.date, end_date=trade1.date
    )
    assert trade1 in trades
    assert trade2 not in trades

    # Проверка лимита
    trades = await get_trades(session=async_db, limit=1)
    assert len(trades) == 1
