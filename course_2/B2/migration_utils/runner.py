from typing import Any

from alembic.config import CommandLine
from alembic.config import Config
from config import settings


def make_config() -> Config:
    alembic_config = Config()
    alembic_config.set_main_option("script_location", settings.SCRIPT_LOCATION)
    alembic_config.set_main_option("version_locations", settings.VERSION_LOCATIONS)
    alembic_config.set_main_option("sqlalchemy.url", settings.get_db_url(is_async=True))
    alembic_config.set_main_option("file_template", settings.FILE_TEMPLATE)
    alembic_config.set_main_option("timezone", settings.TIMEZONE)
    return alembic_config


def alembic_runner(*args: Any) -> None:
    cli = CommandLine()
    cli.run_cmd(make_config(), cli.parser.parse_args(args))
