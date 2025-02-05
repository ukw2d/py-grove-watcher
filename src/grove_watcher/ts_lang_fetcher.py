import importlib.util
import logging
import subprocess
import sys
from pathlib import Path
from typing import Optional

from tree_sitter import Language, Parser

from grove_watcher.config.config import TreeSitterConfig
from grove_watcher.models import TSGrammarModel
from grove_watcher.venv_manager import VenvManager


class TreeSitterInit:
    def __init__(self, venv_manager: VenvManager = None):
        """
        Initialize TreeSitterInit with a logger and optional virtual environment support.
        """
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.config = TreeSitterConfig()
        self.venv_manager = venv_manager
        self.logger.debug("TreeSitterInit initialized")

    def get_python_path(self) -> Optional[Path]:
        python_path = (
            self.venv_manager.python_path
            if self.venv_manager
            else Path(sys.executable)
        )
        return python_path if python_path.exists() else None

    def _get_site_packages(self) -> Optional[Path]:
        if self.venv_manager:
            site_packages = self.venv_manager._get_site_packages_path()
        else:
            site_packages = next(
                (Path(p) for p in sys.path if "site-packages" in p), None
            )
            if not site_packages or not site_packages.exists():
                self.logger.error(
                    "Site-packages directory not found in current environment."
                )
                return None
        return site_packages

    def install_package(self, package_name: str) -> bool:
        if not (python_path := self.get_python_path()):
            self.logger.error("Python executable not found.")
            return False

        pip_command = [str(python_path), "-m", "pip", "install", package_name]
        try:
            subprocess.run(pip_command, check=True, capture_output=True, text=True)
            self.logger.info(f"Successfully installed {package_name}.")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to install {package_name}: {e.stderr}")
            return False

    def _find_module_file(
        self, module_name: str, site_packages: Path
    ) -> Optional[Path]:
        """Find the module file within the site-packages directory."""
        module_path = site_packages / module_name
        if not module_path.exists():
            self.logger.warning(
                f"Module directory '{module_name}' not found at: {module_path}"
            )
            return None

        module_file = (module_path / "__init__.py") or next(
            (f for f in module_path.glob("*.py")), None
        )
        if not module_file:
            self.logger.error(
                f"No Python files found in module directory '{module_name}'."
            )
            return None
        return module_file

    def _load_grammar(self, module_name: str):
        site_packages = self._get_site_packages()
        if site_packages is None:
            self.logger.error("Module package directory not found in the current environment.")
            raise ValueError("Package directory not found.")

        module_file = self._find_module_file(module_name, site_packages)
        if module_file is None:
            self.logger.warning(f"Module file '{module_name}' not found in {site_packages}.")
            return None

        try:
            spec = importlib.util.spec_from_file_location(module_name, str(module_file))
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            self.logger.error(f"Failed to load module '{module_name}': {e}")
            raise ImportError(f"Failed to load module '{module_name}': {e}")

    def _create_ts_model(self, ts_grammar) -> Optional[TSGrammarModel]:
        lang = Language(ts_grammar.language())
        parser = Parser(lang)
        return TSGrammarModel(lang=lang, parser=parser)

    def get_grammar(
        self, language: str
    ) -> Optional[dict[str, Optional[Language | Parser]]]:
        """Initialize Tree-sitter parser for the specified language.
        Args:
            language: Programming language identifier (e.g., 'python', 'javascript').
        Returns:
            Dict containing 'lang' and 'parser' if successful, None otherwise.
        """
        language = language.lower().strip()
        for prefix in self.config.prefixes:
            module_name = f"{prefix}{language}"
            self.logger.info(f"Attempting to load module '{module_name}'...")

            ts_grammar = self._load_grammar(module_name)
            if not ts_grammar:
                self.logger.warning(
                    f"Unable to import {module_name} package. Attempting to install..."
                )
                if self.install_package(module_name):
                    ts_grammar = self._load_grammar(module_name)
                else:
                    self.logger.error(f"Failed to install {module_name}.")
                    return None

            if ts_grammar:
                self.logger.debug(
                    "Package has been imported successfully. Composing pydantic model for a response..."
                )
                result = self._create_ts_model(ts_grammar)
                return result
        self.logger.error(
            f"Failed to load module for '{language}' after installation."
        )
        return None
