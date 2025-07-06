import pathlib

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # type: ignore[misc]
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    excel_absolute_path: pathlib.Path = Field(alias="EXCEL_ABSOLUTE_PATH")


settings = Settings()
