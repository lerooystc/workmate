from datetime import date

from db.session import get_session
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from services.services import upload_trades
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/trades/", status_code=status.HTTP_200_OK)
async def parse_trades(
    date: date,
    db: Session = Depends(get_session),
):
    return_value = await upload_trades(date=date, session=db)
    if not return_value:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"Uploaded": "All trades have been uploaded to the database."}
