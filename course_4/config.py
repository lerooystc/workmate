from pydantic import Field
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = Field("Parser")
    PROJECT_VERSION: str = Field("1.2")
    SPIMEX_URL: str = "https://spimex.com/upload/reports/oil_xls/"
    SCRIPT_LOCATION: str = "migration_utils"
    VERSION_LOCATIONS: str = "migration_utils/versions"
    FILE_TEMPLATE: str = "%%(rev)s_%%(slug)s"
    TIMEZONE: str = "UTC"
    SPIMEX_EXCEL_URL: str = "oil_xls_{}162000.xls"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "1231231"
    DB_HOST: str = "localhost"
    DB_NAME: str = "workmate"
    DB_PORT: int = 5432

    def get_db_url(self, is_async: bool = False) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg" if is_async else "postgresql",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            path=self.DB_NAME,
            port=self.DB_PORT,
        ).unicode_string()


settings = Settings()
