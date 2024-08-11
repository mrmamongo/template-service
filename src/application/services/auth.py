from dataclasses import dataclass

from src.application.schema.user import BaseUserSchema


@dataclass(slots=True)
class AuthService:
    client_id: str

    def ensure_has_access(self, user: BaseUserSchema, *claims: str) -> None:
        """Проверяет, имеет ли пользователь доступ к ресурсу."""
