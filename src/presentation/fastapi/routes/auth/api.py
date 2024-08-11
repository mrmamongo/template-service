from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi import Response
from starlette import status

ROUTER = APIRouter(route_class=DishkaRoute)


@ROUTER.post('/register', status_code=status.HTTP_201_CREATED)
async def register(
    response: Response,
) -> None:
    """Регистрирует пользователя в Keycloak."""
    tokens = object()
    # await generate_avatar_url.kiq(user_id=user_id, username=data.username)
    response.set_cookie('access_token', tokens.access_token, httponly=True)
    response.set_cookie('refresh_token', tokens.refresh_token, httponly=True)


@ROUTER.post('/login')
async def login_route(
    response: Response,
) -> None:
    """Логин пользователя в Keycloak."""
    tokens = object()
    response.set_cookie('access_token', tokens.access_token, httponly=True)
    response.set_cookie('refresh_token', tokens.refresh_token, httponly=True)


@ROUTER.post('/refresh-token')
async def refresh_token(
    response: Response,
) -> None:
    """Обновление токена."""
    tokens = object()
    response.set_cookie('access_token', tokens.access_token, httponly=True)
    response.set_cookie('refresh_token', tokens.refresh_token, httponly=True)


@ROUTER.post('/logout')
async def logout_route(
    response: Response,
) -> None:
    """Логаут пользователя в keycloak."""
    response.delete_cookie('access_token', httponly=True)
    response.delete_cookie('refresh_token', httponly=True)
