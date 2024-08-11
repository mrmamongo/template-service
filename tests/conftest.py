import asyncio
import platform

from collections.abc import AsyncGenerator
from collections.abc import Generator

import pytest

from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from testcontainers.postgres import PostgresContainer

from src.config import Config
from src.config import get_config
from src.infra.postgres.tables import metadata_obj
from tests.utils.alembic import alembic_config_from_url


@pytest.fixture(scope='session')
def config() -> Config:
    return get_config()


@pytest.fixture(scope='session')
def pg_container_url() -> Generator[str, None, None]:
    """Инициализация тестового контейнера"""
    with PostgresContainer('postgres:16-alpine') as postgres:
        logger.error(postgres.get_connection_url(driver='asyncpg'))
        yield postgres.get_connection_url(driver='asyncpg')


@pytest.fixture(scope='session')
def alembic_config(pg_container_url, config):
    """
    Alembic configuration object, bound to temporary database.
    """
    return alembic_config_from_url(pg_url=pg_container_url, config=config.api)


@pytest.fixture(scope='session')
def alembic_engine(pg_container_url: str) -> AsyncEngine:
    return create_async_engine(pg_container_url)


@pytest.fixture(scope='session')
async def pg_engine(pg_container_url: str) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(pg_container_url)

    yield engine

    await engine.dispose()


@pytest.fixture(scope='function')
async def pg_session(pg_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(bind=pg_engine, expire_on_commit=False) as session:
        yield session


@pytest.fixture(scope='session')
def event_loop():
    """Фикстура для получения евент лупа.
    Проверяем, закрыт ли луп, и запущен ли он на винде.
    """
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def db_init(pg_engine: AsyncEngine):
    """Фикстура для скидывания состояния БД.

    Args:
        pg_engine: AsyncEngine
    """
    meta = metadata_obj

    async with pg_engine.connect() as conn:
        await conn.execute(text('DROP SCHEMA IF EXISTS template_schema CASCADE;'))
        await conn.execute(text('CREATE SCHEMA IF NOT EXISTS template_schema;'))

        await conn.run_sync(meta.create_all)
        await conn.commit()


@pytest.fixture(scope='session')
async def get_di_container():
    pass


@pytest.fixture(scope='session')
async def get_application(
    pg_container_url,
):
    logger.info('Initializing fastapi')
    # fastapi = setup_fastapi(config.api)
    # setup_dishka_fastapi(container, fastapi)

    return
