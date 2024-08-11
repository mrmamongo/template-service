from authlib.integrations.base_client import OAuthError
from authlib.integrations.starlette_client import OAuth
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse

ROUTER = APIRouter(route_class=DishkaRoute)


@ROUTER.get('/login')
async def login_route(request: Request, oauth: FromDishka[OAuth]) -> RedirectResponse:
    """Логин пользователя."""
    return await oauth.google.authorize_redirect(request, request.url_for('auth_route'))


@ROUTER.get('/auth')
async def auth_route(request: Request, oauth: FromDishka[OAuth]) -> RedirectResponse:
    """Auth callback для google OAuth."""
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        raise error
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')


@ROUTER.get('/logout')
async def logout_route(request: Request) -> RedirectResponse:
    """Логаут пользователя в keycloak."""
    request.session.pop('user', None)
    return RedirectResponse(url='/')
