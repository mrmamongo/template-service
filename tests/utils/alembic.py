import os

from argparse import Namespace

from alembic.config import Config

from src.config import ApiConfig


def make_alembic_config(cmd_opts: Namespace, base_path: str) -> Config:
    # Replace path to alembic.ini file to absolute
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)

    # Replace path to alembic folder to absolute
    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option(
            'script_location', os.path.join(base_path, alembic_location)
        )
    if cmd_opts.pg_url:
        config.set_main_option('sqlalchemy.url', cmd_opts.pg_url)

    return config


def alembic_config_from_url(
    config: ApiConfig,
    pg_url: str | None = None,
) -> Config:
    """
    Provides Python object, representing alembic.ini file.
    """
    cmd_options = Namespace(
        config='alembic.ini',
        name='alembic',
        pg_url=pg_url,
        raiseerr=False,
        x=None,
    )

    return make_alembic_config(cmd_options, base_path=config.project_path)
