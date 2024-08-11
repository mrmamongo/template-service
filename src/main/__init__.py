from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from fastapi import FastAPI
from loguru import logger

from src.config import Config
from src.config import get_config
from src.infra.loguru import setup_logging
from src.main.di import DishkaProvider
from src.main.security import SecurityProvider
from src.main.web import setup_fastapi

def app() -> FastAPI:
    """Инициализация основного приложения."""
    config: Config = get_config()
    setup_logging(config.logging)

    container = make_async_container(DishkaProvider(config=config), SecurityProvider())
    logger.info('Initializing fastapi')
    fastapi = setup_fastapi(config)
    setup_dishka_fastapi(container, fastapi)

    return fastapi
