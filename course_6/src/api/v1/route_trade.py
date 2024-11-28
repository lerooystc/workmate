from datetime import date
from typing import Optional

from src.db.session import SessionGetter
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from src.services.services import async_bulk_upload_trades
from src.services.services import async_upload_trades
from src.services.services import get_trades
from src.services.services import get_trading_dates
from src.common.util import no_db_session_key_builder
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache


router = APIRouter()
get_sync_session = SessionGetter(start_async=False)
get_async_session = SessionGetter(start_async=True)


@router.post("/trades/async/", status_code=status.HTTP_201_CREATED)
async def async_parse_trades(
    date: date,
    db: AsyncSession = Depends(get_async_session),
) -> dict[str, str]:
    return_value = await async_upload_trades(date=date, session=db)
    if not return_value:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {
        "status": "success",
        "detail": "All trades have been uploaded.",
    }


@router.post("/trades/bulk_async/", status_code=status.HTTP_201_CREATED)
async def async_bulk_parse_trades(
    date_start: date,
    date_end: date,
    db: AsyncSession = Depends(get_async_session),
) -> dict[str, str]:
    return_value = await async_bulk_upload_trades(
        date_start=date_start, date_end=date_end, session=db
    )
    if not return_value:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {
        "status": "success",
        "detail": "All trades have been uploaded.",
    }


@router.get("/trades/get_last_trading_dates", status_code=status.HTTP_200_OK)
@cache(expire=90, key_builder=no_db_session_key_builder)
async def get_last_trading_dates(
    days: int = 5,
    db: AsyncSession = Depends(get_async_session),
):
    return_value = await get_trading_dates(days=days, session=db)
    return {"status": "success", "results": len(return_value), "data": return_value}


@router.get("/trades/get_dynamics", status_code=status.HTTP_200_OK)
@cache(expire=90, key_builder=no_db_session_key_builder)
async def get_dynamics(
    start_date: date,
    end_date: date,
    db: AsyncSession = Depends(get_async_session),
    oil_id: Optional[str] = None,
    delivery_type_id: Optional[str] = None,
    delivery_basis_id: Optional[str] = None,
):
    return_value = await get_trades(
        session=db,
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id,
        start_date=start_date,
        end_date=end_date,
    )
    return {"status": "success", "results": len(return_value), "data": return_value}


@router.get("/trades/get_trading_results", status_code=status.HTTP_200_OK)
@cache(expire=90, key_builder=no_db_session_key_builder)
async def get_trading_results(
    db: AsyncSession = Depends(get_async_session),
    limit: int = 100,
    oil_id: Optional[str] = None,
    delivery_type_id: Optional[str] = None,
    delivery_basis_id: Optional[str] = None,
):
    return_value = await get_trades(
        limit=limit,
        session=db,
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id,
    )
    return {"status": "success", "results": len(return_value), "data": return_value}
