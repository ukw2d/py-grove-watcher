from pathlib import Path

import pytest
from tree_sitter import Language, Parser

from grove_watcher.models import TSGrammarModel
from grove_watcher.ts_lang_fetcher import TreeSitterInit
from grove_watcher.venv_manager import VenvManager


@pytest.fixture
def mock_venv_manager(mocker):
    return mocker.MagicMock(spec=VenvManager)

@pytest.fixture
def venv_manager():
    return VenvManager()

@pytest.fixture
def mock_venv_path(mocker, request):
    """Fixture to provide a mocked venv path."""
    exists = getattr(request, "param", True)
    venv_path = mocker.MagicMock(spec=Path)
    venv_path.exists.return_value = exists
    return venv_path

@pytest.fixture
def mock_python_path(mocker, request):
    """Fixture to provide a mocked Python executable path."""
    exists = getattr(request, "param", True)
    mock_path = mocker.MagicMock(spec=Path)
    mock_path.exists.return_value = exists
    return mock_path

@pytest.fixture
def tree_sitter_init(mock_venv_manager):
    return TreeSitterInit(mock_venv_manager)

@pytest.fixture
def mock_language():
    return "python"

@pytest.fixture
def mock_module_name(mock_language):
    return f"tree_sitter_{mock_language}"

@pytest.fixture
def mock_get_site_packages(tree_sitter_init, mocker, request):
    mock_site_packages = Path("/mock/site-packages")
    if hasattr(request, "param") and not request.param:
        mock_site_packages = None
    return mocker.patch.object(tree_sitter_init, "_get_site_packages", return_value=mock_site_packages)

@pytest.fixture
def mock_find_module_file(tree_sitter_init, mocker, request):
    mock_site_packages = Path("/mock/module/file.py")
    if hasattr(request, "param") and not request.param:
        mock_site_packages = None
    return mocker.patch.object(tree_sitter_init, "_find_module_file", return_value=mock_site_packages)

@pytest.fixture
def mock_importlib(mocker, request):
    # Create mock objects for spec and module
    mock_spec = mocker.MagicMock()
    mock_module = mocker.MagicMock()

    # Mock importlib functions
    mocker.patch('importlib.util.spec_from_file_location', return_value=mock_spec)
    mocker.patch('importlib.util.module_from_spec', return_value=mock_module)

    # Set up the loader and configure exec_module to raise an exception if needed
    mock_spec.loader = mocker.MagicMock()  # Ensure the loader exists
    if hasattr(request, "param") and not request.param:
        mock_spec.loader.exec_module.side_effect = Exception("Simulated import error")
    else:
        mock_spec.loader.exec_module.return_value = None

    mock_module.language = mocker.MagicMock()
    return mock_module

@pytest.fixture
def mock_ts_language(mocker):
    """
    Fixture to mock the Language class.
    """
    mock_language = mocker.MagicMock(spec=Language)
    return mock_language

@pytest.fixture
def mock_ts_parser(mocker):
    """
    Fixture to mock the Parser class.
    """
    mock_parser = mocker.MagicMock(spec=Parser)
    return mock_parser

@pytest.fixture
def mock_tsg_model(mocker, mock_ts_language, mock_ts_parser):
    """
    Fixture to mock the TSGrammarModel class.
    """
    mock_tsg_model = mocker.MagicMock(spec=TSGrammarModel)
    # Define behavior for the language() and parser() methods
    mock_tsg_model.language = mocker.MagicMock(return_value=mock_ts_language)
    mock_tsg_model.parser = mocker.MagicMock(return_value=mock_ts_parser)
    mocker.patch('grove_watcher.ts_lang_fetcher.TSGrammarModel', return_value=mock_tsg_model)
    return mock_tsg_model

@pytest.fixture
def mock_create_ts_model(mocker, tree_sitter_init, mock_tsg_model, request):
    result = mock_tsg_model
    if hasattr(request, "param") and not request.param:
        result = None
    return mocker.patch.object(tree_sitter_init, "_create_ts_model", return_value=result)


@pytest.fixture
def mock_install_package(tree_sitter_init, mocker):
    return mocker.patch.object(
        tree_sitter_init,
        "install_package"
    )

@pytest.fixture
def mock_load_grammar(tree_sitter_init, mocker):
    """
    Fixture to mock the _load_grammar method.
    """
    return mocker.patch.object(tree_sitter_init, "_load_grammar")