from datetime import datetime
from typing import Callable
import pytest
from httpx import AsyncClient
from src.db.models import Trade


@pytest.mark.anyio
async def test_get_trading_results(
    async_client: AsyncClient, trade_factory: Callable[..., Trade]
):
    await trade_factory(
        oil_id="oil1", delivery_type_id="type1", delivery_basis_id="basis1"
    )
    await trade_factory(
        oil_id="oil2", delivery_type_id="type2", delivery_basis_id="basis2"
    )

    trades = await async_client.get("/trades/get_trading_results")
    assert trades.json()["results"] == 2

    trades = await async_client.get("/trades/get_trading_results?oil_id=oil1")
    assert trades.json()["results"] == 1

    trades = await async_client.get(
        "/trades/get_trading_results?delivery_type_id=type1"
    )
    assert trades.json()["results"] == 1

    trades = await async_client.get(
        "/trades/get_trading_results?delivery_basis_id=basis1"
    )
    assert trades.json()["results"] == 1

    trades = await async_client.get("/trades/get_trading_results?limit=1")
    assert trades.json()["results"] == 1


@pytest.mark.anyio
async def test_get_trading_dates(
    async_client: AsyncClient, trade_factory: Callable[..., Trade]
):
    await trade_factory(
        oil_id="oil1",
        delivery_type_id="type1",
        delivery_basis_id="basis1",
        date=datetime(2022, 1, 1),
    )
    await trade_factory(
        oil_id="oil2",
        delivery_type_id="type2",
        delivery_basis_id="basis2",
        date=datetime(2023, 1, 1),
    )

    trades = await async_client.get("/trades/get_last_trading_dates?days=1")
    assert trades.json()["results"] == 1
    assert trades.json()["data"][0] == "2023-01-01"

    trades = await async_client.get("/trades/get_last_trading_dates?days=2")
    assert trades.json()["results"] == 2
    assert trades.json()["data"][0] == "2023-01-01"

    trades = await async_client.get("/trades/get_last_trading_dates?days=3")
    assert trades.json()["results"] == 2
    assert trades.json()["data"][0] == "2023-01-01"


@pytest.mark.anyio
async def test_get_trades_dynamics(
    async_client: AsyncClient, trade_factory: Callable[..., Trade]
):
    await trade_factory(
        oil_id="oil1",
        delivery_type_id="type1",
        delivery_basis_id="basis1",
        date=datetime(2022, 1, 1),
    )
    await trade_factory(
        oil_id="oil2",
        delivery_type_id="type2",
        delivery_basis_id="basis2",
        date=datetime(2023, 1, 1),
    )

    trades = await async_client.get(
        "/trades/get_dynamics?start_date=2022-01-01&end_date=2023-01-01"
    )
    assert trades.json()["results"] == 2

    trades = await async_client.get(
        "/trades/get_dynamics?start_date=2022-01-01&end_date=2023-01-01&oil_id=oil1"
    )
    assert trades.json()["results"] == 1

    trades = await async_client.get(
        "/trades/get_dynamics?start_date=2022-01-01&end_date=2022-02-01"
    )
    assert trades.json()["results"] == 1
