import orjson
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

ROUTER = APIRouter(
    route_class=DishkaRoute
)


@ROUTER.get('/')
async def homepage(request: Request, templates: FromDishka[Jinja2Templates]):
    user = request.session.get('user', None)
    if user:
        user = orjson.dumps(user).decode('utf-8')
    return templates.TemplateResponse(request=request, name='index.html', context={
        'user': user
    })
