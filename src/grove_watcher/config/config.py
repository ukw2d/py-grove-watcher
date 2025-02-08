import json
import os
import sys
from pathlib import Path
from typing import Any, List

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


def json_config_settings_source(key: str = None) -> Any:
    """Loads JSON config and retrieves a specific key if provided."""
    config_file_path = Path(__file__).parent / "config.json"
    with open(config_file_path) as file:
        config_data = json.load(file)
    return config_data if key is None else config_data.get(key, {})

class TreeSitterConfig(BaseSettings):
    prefixes: List[str] = Field(default_factory=lambda:
        json_config_settings_source("prefixes"))


class CacheDirConfig(BaseSettings):
    win32: str = Field(default_factory=lambda:
        json_config_settings_source("cacheDir").get("win32", ""))
    unix: str = Field(default_factory=lambda:
        json_config_settings_source("cacheDir").get("unix", ""))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="GW_CACHE_DIR_",
        extra="ignore"
    )

    @classmethod
    def get_cache_dir(cls) -> Path:
        """Resolves the cache directory, expanding environment variables if needed."""
        instance = cls()
        if sys.platform == "win32":
            cache_dir = os.getenv(instance.win32, str(Path.home() / instance.win32))
        else:
            cache_dir = str(Path.home() / instance.unix)
        return Path(cache_dir)

class VenvExecutableConfig(BaseSettings):
    win32: str = Field(default_factory=lambda:
        json_config_settings_source("venvExecutable").get("win32", ""))
    unix: str = Field(default_factory=lambda:
        json_config_settings_source("venvExecutable").get("unix", ""))
    default_executable: str = Field(default_factory=lambda:
        json_config_settings_source("venvExecutable").get("default", ""))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="GW_VENV_EXECUTABLE_",
        extra="ignore",
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



if __name__ == "__main__":
    print(CacheDirConfig.get_cache_dir())
    print(VenvExecutableConfig.get_venv_executable(Path(".")))
    print(VenvExecutableConfig.get_venv_executable(Path("."), "python3"))