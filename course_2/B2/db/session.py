from contextlib import asynccontextmanager

from config import settings
from db.base import Base
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker


sync_engine = create_engine(settings.pg_dsn, echo=True)

sync_session = sessionmaker(sync_engine)

async_engine = create_async_engine(settings.async_pg_dsn, echo=True)

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


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
