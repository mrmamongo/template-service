from typing import cast

from dishka import Provider
from dishka import Scope
from dishka import provide
from fastapi import HTTPException
from fastapi import Request
from starlette import status

from src.application.enums.role import RoleEnum
from src.application.schema.auth import TokenSchema
from src.application.schema.user import BaseUserSchema, UserSchema, AdminUserSchema, AnyUserSchema
from src.application.services.auth import AuthService


class SecurityProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def _get_tokens_schema_optional(self, request: Request) -> TokenSchema | None:
        if (
                'access_token' not in request.cookies
                or 'refresh_token' not in request.cookies
        ):
            return None

        return TokenSchema(
            access_token=request.cookies['access_token'],
            refresh_token=request.cookies['refresh_token'],
        )

    @provide(scope=Scope.REQUEST)
    async def _get_tokens_schema(self, tokens: TokenSchema | None) -> TokenSchema:
        if tokens is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Tokens required'
            )
        return tokens

    @provide(scope=Scope.REQUEST)
    async def _authenticated(
            self, tokens: TokenSchema
    ) -> BaseUserSchema:
        """Authenticates a user with a token."""

    @provide(scope=Scope.REQUEST)
    async def _authenticated_optional(
            self, tokens: TokenSchema | None) -> BaseUserSchema | None:
        """Authenticate user optionally with a token."""

    @provide(scope=Scope.REQUEST)
    async def _any_user(
            self, user: BaseUserSchema
    ) -> AnyUserSchema:
        """Ensure any user has access to resource."""
        return cast(AnyUserSchema, user)

    @provide(scope=Scope.REQUEST)
    async def _authorized_user(
            self, user: BaseUserSchema, authorization_service: AuthService
    ) -> UserSchema:
        authorization_service.ensure_has_access(user, RoleEnum.USER.value)
        return cast(UserSchema, user)

    @provide(scope=Scope.REQUEST)
    async def _authorized_admin(
            self, user: BaseUserSchema, authorization_service: AuthService
    ) -> AdminUserSchema:
        authorization_service.ensure_has_access(user, RoleEnum.ADMIN.value)
        return cast(AdminUserSchema, user)
