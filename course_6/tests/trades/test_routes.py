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
    print(trades.json())
    assert trades.json()["results"] == 2

    trades = await async_client.get("/trades/get_trading_results?oil_id=oil1")
    print(trades.json())
    assert trades.json()["results"] == 1

    trades = await async_client.get(
        "/trades/get_trading_results?delivery_type_id=type1"
    )
    print(trades.json())
    assert trades.json()["results"] == 1

    trades = await async_client.get(
        "/trades/get_trading_results?delivery_basis_id=basis1"
    )
    print(trades.json())
    assert trades.json()["results"] == 1

    trades = await async_client.get("/trades/get_trading_results?limit=1")
    print(trades.json())
    assert trades.json()["results"] == 1
