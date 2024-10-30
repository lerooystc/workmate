import asyncio
from io import BytesIO

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup

SITE_URL = "https://spimex.com"


async def fetch(session: aiohttp.ClientSession, url: str, delay: int = 0) -> int:
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


async def download_file(session: aiohttp.ClientSession, url: str) -> pd.DataFrame:
    async with session.get(url) as response:
        content = await response.read()
    return pd.read_excel(BytesIO(content))


async def main():
    new_session = aiohttp.ClientSession()
    async with new_session as session:
        links = [
            f"https://spimex.com/markets/oil_products/trades/results/?page=page-{num}"
            for num in range(1, 2)
        ]
        fetchers = [asyncio.create_task(fetch(session, url)) for url in links]

        done, _ = await asyncio.wait(fetchers)
        dl_links = set()

        for task in done:
            res = await task
            dl_links = dl_links | res

        loaders = [
            asyncio.create_task(download_file(session, SITE_URL + url))
            for url in dl_links
        ]

        done, _ = await asyncio.wait(loaders)

        for task in done:
            xls_data = await task
            print(xls_data)


if __name__ == "__main__":
    asyncio.run(main())
