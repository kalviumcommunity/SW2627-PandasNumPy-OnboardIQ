"""Dashboard dataset loading utilities."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "employee_onboarding_analytics.csv"
)

SUPPORTED_FILE_TYPES = {"csv", "json"}


def load_uploaded_dataset(uploaded_file) -> pd.DataFrame:
    """Load and validate an uploaded CSV or JSON dataset.

    Args:
        uploaded_file: Streamlit UploadedFile instance.

    Returns:
        Loaded dataset as a pandas DataFrame.

    Raises:
        ValueError: If the file type is unsupported, empty,
            or cannot be parsed.
    """
    extension = Path(uploaded_file.name).suffix.lower()

    if extension not in {".csv", ".json"}:
        raise ValueError(
            "Unsupported file type. "
            "Please upload a CSV or JSON file."
        )

    file_content = uploaded_file.getvalue()

    if not file_content:
        raise ValueError("The uploaded file is empty.")

    try:
        if extension == ".csv":
            dataframe = pd.read_csv(
                BytesIO(file_content)
            )
        else:
            dataframe = pd.read_json(
                BytesIO(file_content)
            )
    except (
        ValueError,
        OSError,
        pd.errors.ParserError,
    ) as exc:
        raise ValueError(
            "Unable to read the uploaded dataset. "
            "Please verify the file format."
        ) from exc

    if dataframe.empty:
        raise ValueError(
            "The uploaded dataset contains no data."
        )

    return dataframe


def load_default_dataset() -> pd.DataFrame:
    """Load the processed employee analytics dataset.

    Returns:
        Processed employee-level analytical DataFrame.

    Raises:
        FileNotFoundError: If the processed dataset does not exist.
        ValueError: If the dataset is empty or cannot be read.
    """
    if not DEFAULT_DATASET_PATH.exists():
        raise FileNotFoundError(
            "Default dashboard dataset not found: "
            f"{DEFAULT_DATASET_PATH}"
        )

    try:
        dataframe = pd.read_csv(DEFAULT_DATASET_PATH)
    except (
        OSError,
        pd.errors.ParserError,
    ) as exc:
        raise ValueError(
            "Unable to read the default dashboard dataset."
        ) from exc

    if dataframe.empty:
        raise ValueError(
            "Default dashboard dataset contains no data."
        )

    return dataframe


def load_dashboard_dataset() -> pd.DataFrame:
    """Return the dataset currently available to the dashboard.

    Uploaded data takes priority over the processed project
    dataset. A copy is returned so dashboard operations do not
    mutate the stored session data.
    """
    uploaded_dataframe = st.session_state.get(
        "uploaded_dataframe"
    )

    if uploaded_dataframe is not None:
        return uploaded_dataframe.copy()

    try:
        return load_default_dataset()
    except (
        FileNotFoundError,
        ValueError,
    ):
        return pd.DataFrame()


def store_uploaded_dataset(
    dataframe: pd.DataFrame,
    filename: str,
) -> None:
    """Store an uploaded dataset in Streamlit session state."""
    if dataframe.empty:
        raise ValueError(
            "Cannot store an empty dataset."
        )

    st.session_state["uploaded_dataframe"] = dataframe.copy()
    st.session_state["uploaded_filename"] = filename


def clear_uploaded_dataset() -> None:
    """Remove the currently uploaded dataset."""
    st.session_state["uploaded_dataframe"] = None
    st.session_state["uploaded_filename"] = None


def get_uploaded_filename() -> str | None:
    """Return the name of the currently uploaded dataset."""
    return st.session_state.get("uploaded_filename")