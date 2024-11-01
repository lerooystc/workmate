from contextlib import asynccontextmanager

from db.base import Base
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

SYNC_DATABASE_URL = "postgresql://postgres:1231231@localhost/workmate"
ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:1231231@localhost/workmate"

sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)

sync_session = sessionmaker(sync_engine)

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


# async def get_session(start_async: bool) -> Session:
#     if start_async:
#         async with async_session() as async_session:
#             yield async_session
#     else:
#         with sync_session() as sync_session:
#             yield sync_session


class SessionGetter:
    def __init__(self, start_async: bool):
        self.start_async = start_async

    async def __call__(self) -> Session:
        if self.start_async:
            async with async_session() as session:
                yield session
        else:
            with sync_session() as session:
                yield session
