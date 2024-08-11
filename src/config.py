import os

from dataclasses import dataclass
from dataclasses import field

from adaptix import Retort
from dynaconf import Dynaconf


@dataclass(slots=True)
class ApiConfig:
    host: str
    port: int

    templates_dir: str
    debug: bool = False
    workers: int = 1
    cors_origins: list[str] = field(default_factory=list)
    allow_headers: list[str] = field(default_factory=list)
    allow_methods: list[str] = field(default_factory=list)
    allow_credentials: bool = True

    project_name: str = 'template'
    project_path: str = field(
        default_factory=lambda: os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..')
        )
    )


@dataclass(slots=True)
class DatabaseConfig:
    host: str
    port: int
    username: str
    password: str
    database: str
    driver: str = 'postgresql+asyncpg'

    @property
    def dsn(self) -> str:
        """Сборка dsn для базы данных."""
        return f'{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'

@dataclass(slots=True)
class LoggingConfig:
    level: str
    human_readable_logs: bool = True


@dataclass(slots=True)
class Config:
    api: ApiConfig
    database: DatabaseConfig
    logging: LoggingConfig


def get_config() -> Config:
    """Парсинг dotenv и получение конфига."""
    dynaconf = Dynaconf(
        settings_files=['../config.toml'], envvar_prefix='ERGPT', load_dotenv=True
    )
    retort = Retort()

    return retort.load(dynaconf, Config)