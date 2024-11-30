from typing import Any, AsyncGenerator, Callable, Generator
from unittest import mock
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from datetime import date
from functools import wraps

from src.db.models import Trade
from .const import EXCEL_DF, EXCEL_ANOTHER_DF
import pandas as pd
from src.config import settings
from src.db.base import Base
import os
from pathlib import Path


def mock_cache(*args, **kwargs):
    """
    Мок кеша редиса, чтобы не ломалось при тестировании.
    """

    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            return await func(*args, **kwargs)

        return inner

    return wrapper


mock.patch("fastapi_cache.decorator.cache", mock_cache).start()

from src.main import app  # noqa E402

# Тут можно было юзать ТЕСТОВУЮ БД, но у меня и так вайпается база в лайфспане, так что все окей
async_engine = create_async_engine(
    settings.DB.get_postgres_url(is_async=True),
    future=True,  # Для использования движка из SQLAlchemy 2.x
    echo=True,  # Для вывода логов в консоль
)

AsyncSessionFactory = async_sessionmaker(
    async_engine,
    autoflush=False,  # Отключить автоматическую синхронизацию изменений
    expire_on_commit=False,  # Отключить очистку объектов после коммита
)


@pytest.fixture(scope="session")
async def async_db_engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Обеспечивает создание таблиц перед тестами и удаление после тестов.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_db(async_db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, Any]:
    """
    Обеспечивает откат изменений в базе данных после каждого теста для обеспечения изоляции.
    """
    async with AsyncSessionFactory() as session:
        await session.begin()

        yield session

        await session.rollback()

        for table in reversed(Base.metadata.sorted_tables):
            stmt = delete(table)
            await session.execute(stmt)
            await session.commit()


@pytest.fixture
async def async_client(
    async_db: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Предоставляет асинхронный HTTP-клиент для тестирования.
    """

    yield AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
def spimex_response() -> Generator[Path, None, None]:
    """
    Фикстура Pytest, создающая мок Excel-файл из DataFrame для тестирования.

    Эта фикстура записывает содержимое DataFrame EXCEL_DF во временный Excel-файл
    с именем 'mock_excel_file.xlsx'. Файл возвращается как объект Path, указывающий
    на его абсолютное местоположение. После завершения теста, использующего эту фикстуру,
    файл удаляется.

    Возвращает:
        Path: Абсолютный путь к мок Excel-файлу.
    """
    with pd.ExcelWriter("mock_excel_file.xlsx") as writer:
        EXCEL_DF.to_excel(writer, sheet_name="Sheet1", index=False)
    yield Path("mock_excel_file.xlsx").absolute()
    os.remove("mock_excel_file.xlsx")


@pytest.fixture
def different_spimex_response() -> Generator[Path, None, None]:
    """
    Фикстура Pytest, создающая второй мок Excel-файл из DataFrame для тестирования асинхронного парсинга.

    Эта фикстура записывает содержимое DataFrame EXCEL_DF во временный Excel-файл
    с именем 'mock_excel_file.xlsx'. Файл возвращается как объект Path, указывающий
    на его абсолютное местоположение. После завершения теста, использующего эту фикстуру,
    файл удаляется.

    Возвращает:
        Path: Абсолютный путь к мок Excel-файлу.
    """
    with pd.ExcelWriter("mock_excel_file_2.xlsx") as writer:
        EXCEL_ANOTHER_DF.to_excel(writer, sheet_name="Sheet1", index=False)
    yield Path("mock_excel_file_2.xlsx").absolute()
    os.remove("mock_excel_file_2.xlsx")


@pytest.fixture
async def trade_factory(async_db: AsyncSession) -> Callable[..., Trade]:
    """
    Фактори для создания трейдов.
    """

    async def create_trade(
        exchange_product_id: str = "12345",
        exchange_product_name: str = "Product",
        oil_id: str = "oil_id",
        delivery_basis_id: str = "basis_id",
        delivery_basis_name: str = "basis_name",
        delivery_type_id: str = "type_id",
        volume: int = 1000,
        total: int = 100000,
        count: int = 1,
        date: date = date(2020, 1, 1),
    ) -> Trade:
        fake_trade = Trade(
            exchange_product_id=exchange_product_id,
            exchange_product_name=exchange_product_name,
            oil_id=oil_id,
            delivery_basis_id=delivery_basis_id,
            delivery_basis_name=delivery_basis_name,
            delivery_type_id=delivery_type_id,
            volume=volume,
            total=total,
            count=count,
            date=date,
        )
        async_db.add(fake_trade)
        await async_db.commit()
        return fake_trade

    yield create_trade
