from dataclasses import dataclass
from typing import NewType


@dataclass(slots=True)
class BaseUserSchema:
    id: int
    google_id: str


AdminUserSchema = NewType('AdminUserSchema', BaseUserSchema)
UserSchema = NewType('UserSchema', BaseUserSchema)
AnyUserSchema = NewType('AnyUserSchema', BaseUserSchema)
