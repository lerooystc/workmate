from pydantic import Field
from pydantic_settings import BaseSettings

# могу закинуть все в .env, но и так понятно думаю (ну и бд разделить на компоненты)


class Settings(BaseSettings):
    project_name: str = Field("Parser")
    project_version: str = Field("1.2")
    spimex_url: str = "https://spimex.com/upload/reports/oil_xls/"
    script_location: str = "migration_utils"
    version_locations: str = "migration_utils/versions"
    file_template: str = "%%(rev)s_%%(slug)s"
    timezone: str = "UTC"
    spimex_excel_url: str = "oil_xls_{}162000.xls"
    pg_dsn: str = "postgresql://postgres:1231231@localhost:5432/workmate"
    async_pg_dsn: str = "postgresql+asyncpg://postgres:1231231@localhost:5432/workmate"


settings = Settings()
