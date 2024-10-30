import asyncio

import pandas as pd
import sqlalchemy as sa


TO_REMOVE = [
    "Unnamed: 0",
    "Unnamed: 6",
    "Unnamed: 7",
    "Unnamed: 8",
    "Unnamed: 9",
    "Unnamed: 10",
    "Unnamed: 11",
    "Unnamed: 12",
    "Unnamed: 13",
]
COLUMN_NAMES = [
    "exchange_product_id",
    "exchange_product_name",
    "delivery_basis_name",
    "volume",
    "total",
    "count",
]


async def main():
    engine = sa.create_engine("sqlite:///foo.db")
    df: pd.DataFrame = pd.read_excel("oil.xls")
    index = df[df["Форма СЭТ-БТ"] == "Единица измерения: Метрическая тонна"].index[0]
    df.drop(index=df.index[: index + 3], inplace=True)
    df.drop(TO_REMOVE, axis=1, inplace=True)
    df.columns = COLUMN_NAMES
    df.drop(df[df["count"] == "-"].index, inplace=True)
    df.drop(df.tail(2).index, inplace=True)
    df.to_sql(
        name="spimex_trading_results", con=engine, if_exists="append", index=False
    )


if __name__ == "__main__":
    asyncio.run(main())
