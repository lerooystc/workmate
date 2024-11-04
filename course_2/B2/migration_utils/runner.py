from typing import Any

from alembic.config import CommandLine
from alembic.config import Config
from config import settings


def make_config() -> Config:
    alembic_config = Config()
    alembic_config.set_main_option("script_location", settings.script_location)
    alembic_config.set_main_option("version_locations", settings.version_locations)
    alembic_config.set_main_option("sqlalchemy.url", settings.async_pg_dsn)
    alembic_config.set_main_option("file_template", settings.file_template)
    alembic_config.set_main_option("timezone", settings.timezone)
    return alembic_config


def alembic_runner(*args: Any) -> None:
    cli = CommandLine()
    cli.run_cmd(make_config(), cli.parser.parse_args(args))
