from dataclasses import dataclass
from dataclasses import field
from typing import Generic
from typing import TypeVar

TWithSchema = TypeVar('TWithSchema')
TSchema = TypeVar('TSchema')


@dataclass
class WithSchema(Generic[TWithSchema, TSchema]):
    with_data: TWithSchema
    data: TSchema


@dataclass(frozen=True)
class ErrorData(Generic[TSchema]):
    title: str = 'Unknown error occurred'
    data: TSchema | None = None


@dataclass
class ErrorResponseSchema(Generic[TSchema]):
    error: ErrorData[TSchema] = field(default_factory=ErrorData)
