from config.config import (
    BASE_DIR,
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    ERROR_DATA_DIR,
    LOG_DIR,
)


def test_base_directory_exists():
    assert BASE_DIR.exists()


def test_data_directories_are_correct():
    assert RAW_DATA_DIR == DATA_DIR / "raw"
    assert PROCESSED_DATA_DIR == DATA_DIR / "processed"
    assert ERROR_DATA_DIR == DATA_DIR / "errors"


def test_log_directory_is_inside_project():
    assert LOG_DIR == BASE_DIR / "logs"