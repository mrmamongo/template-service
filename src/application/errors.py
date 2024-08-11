from starlette import status


class BaseError(Exception):
    def __init__(
        self,
        message='An unknown error occurred.',
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        self.status_code = status_code
        self.message = message

    def __str__(self) -> str:
        return self.message


class BaseErrorGroup(ExceptionGroup[BaseError]):
    def __init__(self, errors: list[BaseError], **_) -> None:
        super().__init__('Some errors occurred', errors)


class DatabaseError(BaseError):
    def __init__(
        self, message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ) -> None:
        super().__init__(message=message, status_code=status_code)


class NotFoundError(DatabaseError):
    def __init__(self, model_name: str) -> None:
        super().__init__(
            message=f'Модель {model_name} не найдена',
            status_code=status.HTTP_404_NOT_FOUND,
        )


class UniqueError(DatabaseError):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, model_name: str) -> None:
        super().__init__(
            f'Модель {model_name} содержит неуникальные значения',
            status_code=status.HTTP_409_CONFLICT,
        )


class NotAuthorizedError(BaseError):
    def __init__(self) -> None:
        super().__init__(
            message='У вас недостаточно прав для этого действия',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
