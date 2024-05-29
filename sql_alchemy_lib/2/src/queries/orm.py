from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.database import sync_engine, async_engine, session_factory, async_session_factory
from src.models import Base, WorkersORM


def create_tables():
    """Создает все таблицы, определенные в модели, удаляя существующие."""
    sync_engine.echo = True
    Base.metadata.drop_all(bind=sync_engine)  # Удаляет существующие таблицы
    Base.metadata.create_all(bind=sync_engine)  # Создает таблицы заново
    sync_engine.echo = False  # Отключает логирование SQL


def insert_data():
    """Вставляет данные в таблицу workers в синхронном режиме."""
    with session_factory() as session:
        worker_bobr = WorkersORM(username="Bobr")
        worker_volk = WorkersORM(username="Volk")
        session.add_all([worker_bobr, worker_volk])
        session.commit()


async def async_insert_data():
    """Вставляет данные в таблицу workers в асинхронном режиме."""
    async with async_session_factory() as session:
        worker_bobr = WorkersORM(username="Bobr")
        worker_volk = WorkersORM(username="Volk")
        session.add_all([worker_bobr, worker_volk])
        await session.commit()
