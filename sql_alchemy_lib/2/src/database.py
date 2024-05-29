import asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings

# Создание синхронного движка
sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

# Создание асинхронного движка
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

# Фабрика сессий для синхронного использования
session_factory = sessionmaker(bind=sync_engine)

# Фабрика сессий для асинхронного использования
async_session_factory = async_sessionmaker(bind=async_engine, class_=AsyncSession)
