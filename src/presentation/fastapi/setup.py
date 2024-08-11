from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi import FastAPI

from src.presentation.fastapi.exception_handlers import setup_exception_handlers
from src.presentation.fastapi.routes.views.api import ROUTER as VIEWS_ROUTER
from src.presentation.fastapi.routes.auth.api import ROUTER as AUTH_ROUTER


def setup_routes(app: FastAPI) -> None:
    """Установка всех роутеров."""
    app.include_router(router=VIEWS_ROUTER)

    router = APIRouter(prefix='/api', route_class=DishkaRoute)
    router.include_router(router=AUTH_ROUTER, prefix='/auth')

    app.include_router(router)
    setup_exception_handlers(app)
