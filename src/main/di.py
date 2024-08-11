from collections.abc import AsyncIterable

from dishka import Provider
from dishka import Scope
from dishka import from_context
from dishka import provide
from dishka import provide_all
from fastapi import Request
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocket

from src.config import AuthConfig
from src.config import Config


class DishkaProvider(Provider):
    def __init__(
        self,
        config: Config,
    ) -> None:
        self.config = config
        super().__init__()

    @provide(scope=Scope.APP)
    async def _get_auth_config(self) -> AuthConfig:
        return self.config.auth

    @provide(scope=Scope.APP)
    async def _get_jinja_templates(self) -> Jinja2Templates:
        return Jinja2Templates(directory=self.config.api.templates_dir)

    @provide(scope=Scope.APP)
    async def _get_engine(self) -> AsyncIterable[AsyncEngine]:
        engine: AsyncEngine | None = None
        try:
            if engine is None:
                engine = create_async_engine(self.config.database.dsn)

            yield engine
        except ConnectionRefusedError as e:
            logger.error('Error connecting to database', e)
        finally:
            if engine is not None:
                await engine.dispose()

    @provide(scope=Scope.APP)
    async def _get_session_maker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)

    _request = from_context(provides=Request, scope=Scope.REQUEST)
    _websocket = from_context(provides=WebSocket, scope=Scope.SESSION)

    @provide(scope=Scope.REQUEST)
    async def _get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    _get_gateways = provide_all(
        scope=Scope.REQUEST,
    )

    _get_usecases = provide_all(
        scope=Scope.REQUEST,
    )
