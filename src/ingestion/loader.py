from pathlib import Path
from typing import Iterable

import pandas as pd

from src.utils.logging_utils import setup_logger


logger = setup_logger("onboardiq.ingestion")


class IngestionError(Exception):
    """Raised when a data file cannot be ingested successfully."""


def _validate_file(path: Path, expected_extension: str) -> None:
    """Validate that a file exists and has the expected extension."""
    if not path.exists():
        raise FileNotFoundError(f"Data file does not exist: {path}")

    if not path.is_file():
        raise IngestionError(f"Path is not a file: {path}")

    if path.suffix.lower() != expected_extension:
        raise ValueError(
            f"Unsupported file extension for {path.name}. "
            f"Expected '{expected_extension}'."
        )


def _validate_dataframe(
    dataframe: pd.DataFrame,
    path: Path,
    required_columns: Iterable[str] | None = None,
    primary_key: str | None = None,
) -> pd.DataFrame:
    """Perform basic validation without modifying the DataFrame."""

    if dataframe.empty:
        raise ValueError(f"Loaded dataset is unexpectedly empty: {path}")

    if required_columns is not None:
        missing_columns = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns in {path.name}: "
                f"{missing_columns}"
            )

    if primary_key is not None:
        if primary_key not in dataframe.columns:
            raise ValueError(
                f"Primary key '{primary_key}' is not present "
                f"in {path.name}."
            )

        duplicate_count = dataframe[primary_key].duplicated().sum()

        if duplicate_count > 0:
            logger.warning(
                "%s contains %d duplicate values in primary key '%s'.",
                path.name,
                duplicate_count,
                primary_key,
            )

    return dataframe


def load_csv(
    path: str | Path,
    required_columns: Iterable[str] | None = None,
    primary_key: str | None = None,
) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.

    The function performs basic ingestion validation but does not
    clean, transform, or modify the loaded data.
    """
    file_path = Path(path)

    _validate_file(file_path, ".csv")

    try:
        dataframe = pd.read_csv(file_path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(
            f"CSV file contains no data: {file_path}"
        ) from exc
    except (OSError, pd.errors.ParserError) as exc:
        raise IngestionError(
            f"Failed to load CSV file '{file_path}': {exc}"
        ) from exc

    _validate_dataframe(
        dataframe,
        file_path,
        required_columns=required_columns,
        primary_key=primary_key,
    )

    logger.info(
        "Loaded CSV file '%s' with shape %s.",
        file_path,
        dataframe.shape,
    )

    return dataframe


def load_json(
    path: str | Path,
    required_columns: Iterable[str] | None = None,
    primary_key: str | None = None,
) -> pd.DataFrame:
    """
    Load a JSON file into a Pandas DataFrame.

    The function performs basic ingestion validation but does not
    clean, transform, or modify the loaded data.
    """
    file_path = Path(path)

    _validate_file(file_path, ".json")

    try:
        dataframe = pd.read_json(file_path)
    except ValueError as exc:
        raise ValueError(
            f"Malformed or invalid JSON file '{file_path}': {exc}"
        ) from exc
    except OSError as exc:
        raise IngestionError(
            f"Failed to load JSON file '{file_path}': {exc}"
        ) from exc

    _validate_dataframe(
        dataframe,
        file_path,
        required_columns=required_columns,
        primary_key=primary_key,
    )

    logger.info(
        "Loaded JSON file '%s' with shape %s.",
        file_path,
        dataframe.shape,
    )

    return dataframe