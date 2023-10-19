import enum
import os
from pathlib import Path
from tempfile import gettempdir
from pydantic_settings import BaseSettings, SettingsConfigDict

from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "0.0.0.0"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = True

    log_level: LogLevel = LogLevel.INFO
    # Variables for the database
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = os.getenv("DB_PORT", 3306)
    db_user: str = os.getenv("DB_USER", "root")
    db_pass: str = os.getenv("DB_PASS", "root")
    db_base: str = os.getenv("DB_NAME", "bake_connect")
    db_echo: bool = False

    # Secret key for JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret")

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """

        return URL.build(
            scheme="mysql+aiomysql",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        env_file_encoding="utf-8",
    )


settings = Settings()
