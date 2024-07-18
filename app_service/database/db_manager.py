from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
    create_async_engine
)


class DatabaseManager:
    """
    Класс отвечающий за соединение с базой данных и обработку сеанса
    """
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = None

    def init_connection(self, db_url: str):
        """
        Инициализация подключения
        """
        self._engine = create_async_engine(url=db_url)
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False
        )

    async def close_connection(self) -> None:
        """
        Закрытие подключения
        """
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        Контекст менеджер для получения сессии
        """
        if self._sessionmaker is None:
            raise IOError('Database manager is not initialized')
        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    async def get_session(self) -> AsyncSession:
        """
        Зависимость для FastAPI
        """
        async with self.session() as session:
            yield session


db_manager = DatabaseManager()
