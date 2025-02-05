import sys

# Handle versioning
if sys.version_info[:2] >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    dist_name = "grove-watcher"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from .__main__ import find
from .models import TSGrammarModel
from .ts_lang_fetcher import TreeSitterInit
from .venv_manager import VenvManager

__all__ = ["TreeSitterInit", "VenvManager", "TSGrammarModel", "__version__", "find"]
