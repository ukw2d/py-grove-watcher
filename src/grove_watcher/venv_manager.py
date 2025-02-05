import logging
import shutil
import subprocess
import sys
from pathlib import Path

from .config.config import CacheDirConfig, VenvExecutableConfig


class VenvManager:
    def __init__(self, venv_name: str = "grove_watcher_cache_env"):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.venv_name = venv_name
        self.cache_dir_config = CacheDirConfig()
        self.venv_executable_config = VenvExecutableConfig()
        self.venv_path = self._get_venv_path()
        self.python_path = self.venv_executable_config.get_venv_executable(self.venv_path)
        self.logger.debug(f"Venv path: {self.venv_path}")
        self.create_venv()
        self.site_packages_path = self._get_site_packages_path()
        self.logger.debug(f"Site packages path: {self.site_packages_path}")


    def _get_venv_path(self) -> Path:
        cache_dir = self.cache_dir_config.get_cache_dir()
        venv_path = cache_dir / self.venv_name
        venv_path.mkdir(parents=True, exist_ok=True)
        return venv_path

    def create_venv(self):
        try:
            if not self.python_path.exists():
                self.logger.warning(f"Creating virtual environment at {self.venv_path}...")
                subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)], check=True)
            else:
                self.logger.info(f"Using existing virtual environment at {self.venv_path}...")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to create virtual environment: {e}")
            return False

    def _get_site_packages_path(self) -> Path:
        if not self.python_path:
            raise ImportError("Python executable not found.")

        result = subprocess.run(
            [str(self.python_path), "-c", "import site; print(site.getsitepackages()[0])"],
            capture_output=True,
            text=True,
            check=True
        )
        site_packages_path = Path(result.stdout.strip())
        if not site_packages_path.exists():
            raise ImportError(f"Site-packages directory not found at: {site_packages_path}")
        return site_packages_path

    def remove_venv(self) -> None:
        if self.venv_path.exists():
            shutil.rmtree(self.venv_path)
            self.logger.info(f"Removed virtual environment at: {self.venv_path}")
        else:
            self.logger.warning(f"Virtual environment not found at: {self.venv_path}")
