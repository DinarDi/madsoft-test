import os

import pytest_asyncio
from httpx import (
    AsyncClient,
    ASGITransport
)
from dotenv import load_dotenv

from database import db_manager
from main import memes_app


load_dotenv(dotenv_path='.env.test')
TEST_DB_URL = os.getenv('DB_URL_FOR_TEST')


@pytest_asyncio.fixture()
async def client():
    db_manager.init_connection(db_url=TEST_DB_URL)
    await db_manager.create_table()

    async with AsyncClient(transport=ASGITransport(memes_app), base_url='http://test') as ac:
        yield ac

    await db_manager.drop_table()
