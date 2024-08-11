from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.config import Config
from src.infra.metrics import setup_metrics
from src.presentation.fastapi.setup import setup_routes


def setup_fastapi(config: Config) -> FastAPI:
    """Установка fastapi."""
    app = FastAPI(title=config.api.project_name, debug=config.api.debug)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.api.cors_origins,
        allow_credentials=config.api.allow_credentials,
        allow_methods=config.api.allow_methods,
        allow_headers=config.api.allow_headers,
        expose_headers=['Content-Range'],
    )
    app.add_middleware(SessionMiddleware, secret_key=config.auth.secret_key)
    setup_metrics(app, config.api)
    setup_routes(app)

    return app
