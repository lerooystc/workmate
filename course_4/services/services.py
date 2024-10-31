from datetime import datetime

import pandas as pd
from db.models import Trade
from sqlalchemy.ext.asyncio import AsyncSession
from util.util import COLUMN_NAMES
from util.util import DeadLinkException
from util.util import TO_REMOVE


def process_sheet(url: str) -> pd.DataFrame:
    try:
        df: pd.DataFrame = pd.read_excel(url)
    except Exception:
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


def date_to_link(date: datetime) -> str:
    formatted_date = date.strftime("%Y%m%d")
    return (
        f"https://spimex.com/upload/reports/oil_xls/oil_xls_{formatted_date}162000.xls"
    )


async def upload_trades(date: datetime, session: AsyncSession):
    url = date_to_link(date)
    try:
        df = process_sheet(url)
    except DeadLinkException:
        return None
    async with session.begin():
        trades = [Trade(**row.to_dict()) for _, row in df.iterrows()]
        session.add_all(trades)
    await session.commit()
    return "Good!"
