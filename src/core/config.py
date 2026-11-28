from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

_BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_BASE_DIR / ".env"
    )

    # DATABASE
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # TEST DATABASE
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str

    # Alembic uses sync connections
    @property
    def sync_db_url(self) -> str:
        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME
        ).render_as_string(hide_password=False)

    # Alembic uses sync connections
    @property
    def test_sync_db_url(self) -> str:
        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.TEST_DB_USER,
            password=self.TEST_DB_PASSWORD,
            host=self.TEST_DB_HOST,
            port=self.TEST_DB_PORT,
            database=self.TEST_DB_NAME
        ).render_as_string(hide_password=False)

    @property
    def async_db_url(self) -> str:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME
        ).render_as_string(hide_password=False)

    @property
    def test_async_db_url(self) -> str:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.TEST_DB_USER,
            password=self.TEST_DB_PASSWORD,
            host=self.TEST_DB_HOST,
            port=self.TEST_DB_PORT,
            database=self.TEST_DB_NAME
        ).render_as_string(hide_password=False)


settings = Settings()