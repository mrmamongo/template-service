from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi import FastAPI

from src.presentation.fastapi.exception_handlers import setup_exception_handlers
from src.presentation.fastapi.routes.admin.assistants.api import (
    ROUTER as ADMIN_ASSISTANT_ROUTER,
)
from src.presentation.fastapi.routes.admin.categories.api import (
    ROUTER as CATEGORY_ROUTER,
)
from src.presentation.fastapi.routes.admin.chats.api import ROUTER as ADMIN_CHAT_ROUTER
from src.presentation.fastapi.routes.admin.queries.api import (
    ROUTER as ADMIN_QUERY_ROUTER,
)
from src.presentation.fastapi.routes.admin.users.api import ROUTER as ADMIN_USER_ROUTER
from src.presentation.fastapi.routes.auth.api import ROUTER as AUTH_ROUTER
from src.presentation.fastapi.routes.core.assistants.api import (
    ROUTER as ASSISTANT_ROUTER,
)
from src.presentation.fastapi.routes.core.chat.api import ROUTER as CHAT_ROUTER
from src.presentation.fastapi.routes.core.users.api import ROUTER as USER_ROUTER


def setup_routes(app: FastAPI) -> None:
    """Установка всех роутеров."""
    router = APIRouter(prefix='/api', route_class=DishkaRoute)

    router.include_router(router=AUTH_ROUTER, prefix='/auth', tags=['Authentication'])
    router.include_router(router=USER_ROUTER, prefix='/user', tags=['User'])
    router.include_router(
        router=ASSISTANT_ROUTER, prefix='/assistant', tags=['Assistant']
    )
    router.include_router(router=CHAT_ROUTER, prefix='/chat', tags=['Chat'])

    admin_router = APIRouter(route_class=DishkaRoute)
    admin_router.include_router(
        router=ADMIN_ASSISTANT_ROUTER, prefix='/assistant', tags=['Admin', 'Assistant']
    )
    admin_router.include_router(
        router=ADMIN_CHAT_ROUTER, prefix='/chat', tags=['Admin', 'Chat']
    )
    admin_router.include_router(
        router=ADMIN_QUERY_ROUTER, prefix='/query', tags=['Admin', 'Query']
    )
    admin_router.include_router(
        router=ADMIN_USER_ROUTER, prefix='/user', tags=['Admin', 'Users']
    )

    admin_router.include_router(
        router=CATEGORY_ROUTER, prefix='/category', tags=['Admin', 'Categories']
    )
    router.include_router(prefix='/admin', router=admin_router)
    app.include_router(router)
    setup_exception_handlers(app)
