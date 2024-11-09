from datetime import date

from db.session import SessionGetter
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from services.services import async_bulk_upload_trades
from services.services import async_upload_trades
from services.services import sync_bulk_upload_trades
from services.services import sync_upload_trades
from sqlalchemy.orm import Session


router = APIRouter()
get_sync_session = SessionGetter(start_async=False)
get_async_session = SessionGetter(start_async=True)


@router.post("/trades/sync/", status_code=status.HTTP_201_CREATED)
def sync_parse_trades(
    date: date,
    db: Session = Depends(get_sync_session),
) -> dict[str, str]:
    return_value = sync_upload_trades(date=date, session=db)
    if not return_value:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"Uploaded": f"All trades have been uploaded in {return_value} secs."}


@router.post("/trades/async/", status_code=status.HTTP_201_CREATED)
async def async_parse_trades(
    date: date,
    db: Session = Depends(get_async_session),
) -> dict[str, str]:
    return_value = await async_upload_trades(date=date, session=db)
    if not return_value:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"Uploaded": f"All trades have been uploaded in {return_value} secs."}


@router.post("/trades/bulk_async/", status_code=status.HTTP_201_CREATED)
async def async_bulk_parse_trades(
    date_start: date,
    date_end: date,
    db: Session = Depends(get_async_session),
) -> dict[str, str]:
    return_value = await async_bulk_upload_trades(
        date_start=date_start, date_end=date_end, session=db
    )
    if not return_value:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"Uploaded": f"All trades have been uploaded in {return_value} secs."}


@router.post("/trades/bulk_sync/", status_code=status.HTTP_201_CREATED)
def sync_bulk_parse_trades(
    date_start: date,
    date_end: date,
    db: Session = Depends(get_sync_session),
) -> dict[str, str]:
    return_value = sync_bulk_upload_trades(
        date_start=date_start, date_end=date_end, session=db
    )
    if not return_value:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"Uploaded": f"All trades have been uploaded in {return_value} secs."}
