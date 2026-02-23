"""Configuration loading: YAML files with environment variable resolution + Pydantic validation."""

import os
from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pyaml_env import parse_config


class DatabaseConfig(BaseModel):
    host: str = "localhost"
    port: int = 5432
    name: str
    user: str
    password: str
    pool_size: int = 5
    max_overflow: int = 10
    echo: bool = False

    @property
    def url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class AppConfig(BaseModel):
    name: str
    version: str = "0.1.0"
    log_level: str = "INFO"


class Settings(BaseSettings):
    app: AppConfig
    server: ServerConfig
    database: DatabaseConfig


def _merge_dicts(base: dict, override: dict) -> dict:
    """Deep merge override into base."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def load_config() -> Settings:
    """Load YAML config, apply profile overlay, and return validated Settings."""
    config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "config")
    config_dir = os.path.abspath(config_dir)

    base = parse_config(os.path.join(config_dir, "application.yml"))

    profile = os.environ.get("APP_PROFILE")
    if profile:
        profile_path = os.path.join(config_dir, f"application-{profile}.yml")
        if os.path.exists(profile_path):
            overlay = parse_config(profile_path)
            base = _merge_dicts(base, overlay)

    return Settings(**base)


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton."""
    return load_config()
