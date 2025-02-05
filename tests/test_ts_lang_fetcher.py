import pytest


class TestTreeSitterInit:
    def test__load_grammar_success(
        self, mock_module_name, tree_sitter_init, mock_get_site_packages,
        mock_find_module_file, mock_importlib
    ):
        result = tree_sitter_init._load_grammar(mock_module_name)
        assert result == mock_importlib

    @pytest.mark.parametrize("mock_get_site_packages", [False], indirect=True)
    def test__load_grammar_no_site_packages(
        self, mock_module_name, tree_sitter_init,
        mock_get_site_packages, caplog
    ):
        with pytest.raises(ValueError, match="Package directory not found."):
            tree_sitter_init._load_grammar(mock_module_name)

    @pytest.mark.parametrize("mock_find_module_file", [False], indirect=True)
    def test__load_grammar_no_module_file(
        self, tree_sitter_init, mock_module_name,
        mock_get_site_packages, mock_find_module_file
    ):
        result = tree_sitter_init._load_grammar(mock_module_name)
        assert result is None

    @pytest.mark.parametrize("mock_importlib", [False], indirect=True)
    def test__load_grammar_import_exception(
        self, tree_sitter_init, mock_module_name, mock_get_site_packages,
        mock_find_module_file, mock_importlib, caplog
    ):
        """
        Test that _load_grammar raises an ImportError when an import error occurs.
        """
        with pytest.raises(ImportError, match=f"Failed to load module '{mock_module_name}': Simulated import error"):
            tree_sitter_init._load_grammar(mock_module_name)


    def test_get_grammar_existing_module(
        self, tree_sitter_init, mock_language, mock_module_name,
        mock_load_grammar, mock_create_ts_model, mock_tsg_model
    ):
        result = tree_sitter_init.get_grammar(mock_language)
        mock_load_grammar.assert_called_once_with(mock_module_name)
        assert result == mock_tsg_model

    def test_get_grammar_install_and_load(
        self, tree_sitter_init, mock_language, mock_module_name,
        mock_install_package, mock_create_ts_model, mock_tsg_model, mock_load_grammar
    ):
        """
        Test get_grammar when the module does not exist and needs to be installed and loaded.
        """
        mock_load_grammar.side_effect = [None, mock_tsg_model]
        result = tree_sitter_init.get_grammar(mock_language)
        assert mock_load_grammar.call_count == 2
        mock_install_package.assert_called_once_with(mock_module_name)

        assert result == mock_tsg_model

    def test_get_grammar_install_failed(
        self, tree_sitter_init, mock_language, mock_module_name,
        mock_install_package, mock_create_ts_model, mock_tsg_model, mock_load_grammar
    ):
        """
        Test get_grammar when the module does not exist and needs to be installed and loaded.
        """
        mock_load_grammar.side_effect = [None]
        mock_install_package.side_effect = [False]
        result = tree_sitter_init.get_grammar(mock_language)
        mock_load_grammar.assert_called_once_with(mock_module_name)
        mock_install_package.assert_called_once_with(mock_module_name)

        assert result is None

    def test_get_grammar_not_loaded(
        self, tree_sitter_init, mock_language, mock_module_name,
        mock_install_package, mock_create_ts_model, mock_tsg_model, mock_load_grammar
    ):
        """
        Test get_grammar when the module does not exist and needs to be installed and loaded.
        """
        mock_load_grammar.side_effect = [None, None]
        result = tree_sitter_init.get_grammar(mock_language)
        assert mock_load_grammar.call_count == 2
        mock_install_package.assert_called_once_with(mock_module_name)

        assert result is None