from pathlib import Path

from src.utils.file_utils import create_directory


def test_create_directory(tmp_path):
    test_directory = tmp_path / "test_directory"

    result = create_directory(test_directory)

    assert test_directory.exists()
    assert test_directory.is_dir()
    assert result == test_directory