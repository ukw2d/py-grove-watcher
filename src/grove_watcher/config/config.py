import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


def json_config_settings_source() -> Dict[str, Any]:
    config_file_path = Path(__file__).parent / 'config.json'
    with open(config_file_path) as file:
        contents = json.load(file)
    return contents

class TreeSitterConfig(BaseSettings):
    prefixes: List[str]

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ):
        return (json_config_settings_source,)

class CacheDirConfig(BaseSettings):
    win32: str
    unix: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="CACHE_DIR_",
        extra="ignore"
    )

    @classmethod
    def get_cache_dir(cls) -> Path:
        """Constructs the full path to the cache directory."""
        instance = cls()
        if sys.platform == "win32":
            if '/' not in instance.win32 and '\\' not in instance.win32:
                # Assuming it's an environment variable
                cache_dir = os.environ.get(instance.win32)
                if not cache_dir:
                    raise EnvironmentError(f"Environment variable {instance.win32} is not set.")
            else:
                cache_dir = str(Path.home() / instance.win32)
        else:
            # For Unix-like systems
            cache_dir = str(Path.home() / instance.unix)
        return Path(cache_dir)

class VenvExecutableConfig(BaseSettings):
    win32: str
    unix: str
    default_executable: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="VENV_EXECUTABLE_",
        extra="ignore"
    )

    @classmethod
    def get_venv_executable(cls, venv_path: Path, executable: str = None) -> Path:
        """Constructs the full path to the virtual environment executable."""
        instance = cls()
        executable = executable or instance.default_executable
        if sys.platform == "win32":
            venv_executable = instance.win32
            # Ensure we use backslashes for Windows paths
            venv_executable_path = venv_path / venv_executable
        else:
            venv_executable = instance.unix
            venv_executable_path = venv_path / venv_executable
        return venv_executable_path

