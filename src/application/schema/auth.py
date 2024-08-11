from dataclasses import dataclass


@dataclass(slots=True)
class TokenSchema:
    access_token: str
    refresh_token: str
