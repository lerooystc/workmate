import asyncio
import logging
from asyncio.events import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from io import BytesIO

import aiohttp
import asyncpg
import pandas as pd
from asyncpg.pool import Pool
from bs4 import BeautifulSoup
from course_4.util.commands import CREATE_TRADING_RESULTS_TABLE
from course_4.util.util import COLUMN_NAMES
from course_4.util.util import TO_REMOVE

SITE_URL = "https://spimex.com"

# я запутался уже 20:41 (НО ВРОДЕ ВСЕ РАБОТАЕТ 21:16)


def process_sheet(url: str) -> list[list]:
    df: pd.DataFrame = pd.read_excel(url)
    trades_date = df.iloc[2]["Форма СЭТ-БТ"][-10:]
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
    df["date"] = trades_date
    df["created_on"] = "now"
    df["updated_on"] = "now"
    return df.values.tolist()


async def fetch(session: aiohttp.ClientSession, url: str, delay: int = 0) -> set[str]:
    if delay:
        await asyncio.sleep(delay)
    async with session.get(url) as result:
        content = await result.text()
        soup = BeautifulSoup(content, "html.parser")
        res = set()
        clean_page = soup.select("div.page-content__tabs__block")
        for link in clean_page[0].find_all("a", class_="accordeon-inner__item-title"):
            res.add(link.get("href"))
        return res


async def add_trade(pool: Pool, values: list):
    async with pool.acquire() as connection:
        connection: asyncpg.connection.Connection
        try:
            async with connection.transaction():
                query = f"""INSERT INTO spimex_trading_results(exchange_product_id,
                exchange_product_name,
                delivery_basis_name,
                volume,
                total,
                count,
                oil_id,
                delivery_basis_id,
                delivery_type_id,
                date,
                created_on,
                updated_on) VALUES {*values, }"""
                return await connection.execute(query)
        except Exception:
            logging.exception("Ошибка!", query)


async def process_into_db(
    session: aiohttp.ClientSession,
    url: str,
    loop: AbstractEventLoop,
    process_pool: ProcessPoolExecutor,
    db_pool: Pool,
) -> pd.DataFrame:
    async with session.get(url) as response:
        content = await response.read()
    call = partial(process_sheet, BytesIO(content))
    # ??? вот после этого я не уверен
    values = await loop.run_in_executor(process_pool, call)
    insert_calls = [add_trade(db_pool, insert_values) for insert_values in values]
    results = await asyncio.gather(*insert_calls)
    return results


async def get_links_from_site(
    session: aiohttp.ClientSession, page_start: int, page_end: int
) -> set[str]:
    links = [
        f"https://spimex.com/markets/oil_products/trades/results/?page=page-{num}"
        for num in range(page_start, page_end)
    ]
    fetchers = [asyncio.create_task(fetch(session, url)) for url in links]

    done, _ = await asyncio.wait(fetchers)
    dl_links = set()

    for task in done:
        res = await task
        dl_links = dl_links | res

    return dl_links


async def setup_db():
    master_connection: asyncpg.connection.Connection = await asyncpg.connect(
        host="127.0.0.1",
        port=5432,
        user="postgres",
        database="workmate",
        password="1231231",
    )

    await master_connection.execute(CREATE_TRADING_RESULTS_TABLE)
    await master_connection.close()


async def main():
    new_session = aiohttp.ClientSession()
    loop = asyncio.get_running_loop()

    async with new_session as session:
        dl_links = await get_links_from_site(session, 1, 31)
        await setup_db()
        async with asyncpg.create_pool(
            host="127.0.0.1",
            port=5432,
            user="postgres",
            password="1231231",
            database="workmate",
            min_size=10,
            max_size=10,
        ) as db_pool:
            with ProcessPoolExecutor() as process_pool:
                loaders = [
                    asyncio.create_task(
                        process_into_db(
                            session, SITE_URL + url, loop, process_pool, db_pool
                        )
                    )
                    for url in dl_links
                ]

                done, _ = await asyncio.wait(loaders)

                for task in done:
                    await task


if __name__ == "__main__":
    asyncio.run(main())
