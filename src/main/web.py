from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config import ApiConfig
from src.infra.metrics import setup_metrics
from src.presentation.fastapi.setup import setup_routes


def setup_fastapi(config: ApiConfig) -> FastAPI:
    """Установка fastapi."""
    app = FastAPI(title=config.project_name, debug=config.debug)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=config.allow_credentials,
        allow_methods=config.allow_methods,
        allow_headers=config.allow_headers,
        expose_headers=['Content-Range'],
    )
    setup_metrics(app, config)
    setup_routes(app)

    return app
