from pydantic import Field
from pydantic import PostgresDsn
from pydantic import RedisDsn
from pydantic_settings import BaseSettings


class DbSettings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "1231231"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_NAME: str = "workmate"
    POSTGRES_PORT: int = 5432
    REDIS_HOST: str = "redis-cache"
    REDIS_PORT: int = 6379

    def get_postgres_url(self, is_async: bool = False) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg" if is_async else "postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            path=self.POSTGRES_NAME,
            port=self.POSTGRES_PORT,
        ).unicode_string()

    def get_redis_url(self) -> str:
        return RedisDsn.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
        ).unicode_string()


class Settings(BaseSettings):
    PROJECT_NAME: str = Field("Parser")
    PROJECT_VERSION: str = Field("1.2")
    SPIMEX_URL: str = "https://spimex.com/upload/reports/oil_xls/"
    SCRIPT_LOCATION: str = "migration_utils"
    VERSION_LOCATIONS: str = "migration_utils/versions"
    FILE_TEMPLATE: str = "%%(rev)s_%%(slug)s"
    TIMEZONE: str = "UTC"
    SPIMEX_EXCEL_URL: str = "oil_xls_{}162000.xls"
    DB: DbSettings = DbSettings()


settings = Settings()
