import subprocess

import pytest


class TestVenvManager:
    @pytest.mark.parametrize("mock_python_path", [True], indirect=True)
    def test_create_venv_existing(self, mocker, venv_manager, mock_python_path):
        """Test using an existing virtual environment."""
        # Set the mocked Python path on the venv_manager
        mocker.patch.object(venv_manager, "python_path", mock_python_path)
        mock_subprocess_run = mocker.patch("subprocess.run")
        result = venv_manager.create_venv()
        assert result is True
        mock_subprocess_run.assert_not_called()

    @pytest.mark.parametrize("mock_python_path", [False], indirect=True)
    def test_create_venv_non_existing(self, venv_manager, mock_python_path, mocker):
        """Test creating a new virtual environment when none exists."""
        mocker.patch.object(venv_manager, "python_path", mock_python_path)
        mock_subprocess_run = mocker.patch("subprocess.run")
        result = venv_manager.create_venv()
        assert result is True
        mock_subprocess_run.assert_called_once()

    @pytest.mark.parametrize("mock_python_path", [False], indirect=True)
    def test_create_venv_failure(self, venv_manager, mock_python_path, mocker):
        """Test handling failure during virtual environment creation."""
        mocker.patch.object(venv_manager, "python_path", mock_python_path)
        # Mock subprocess.run to raise a CalledProcessError
        mock_subprocess_run = mocker.patch(
            "subprocess.run",
            side_effect=subprocess.CalledProcessError(returncode=1, cmd="python -m venv")
        )
        result = venv_manager.create_venv()
        assert result is False
        mock_subprocess_run.assert_called_once()