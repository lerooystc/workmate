from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CONVENTION: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
    SCHEMA: str = "bookstore"
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
