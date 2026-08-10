from pathlib import Path

from config.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    ERROR_DATA_DIR,
    LOG_DIR,
)


def create_directory(path: Path) -> Path:
    """Create a directory if it does not already exist."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def prepare_project_directories() -> None:
    """Create all directories required by the data workflow."""
    directories = [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        ERROR_DATA_DIR,
        LOG_DIR,
    ]

    for directory in directories:
        create_directory(directory)