"""Dataset upload page for the OnboardIQ dashboard."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.dashboard.data import (
    clear_uploaded_dataset,
    get_uploaded_filename,
    load_uploaded_dataset,
    store_uploaded_dataset,
)


def _render_dataset_summary(dataframe: pd.DataFrame) -> None:
    """Display summary information for the uploaded dataset."""

    st.subheader("Dataset Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", len(dataframe))
    col2.metric("Columns", len(dataframe.columns))

    missing_values = int(dataframe.isna().sum().sum())
    col3.metric("Missing Values", missing_values)

    memory_usage = dataframe.memory_usage(deep=True).sum()
    col4.metric(
        "Memory Usage",
        f"{memory_usage / 1024:.1f} KB",
    )


def _render_dataset_metadata(
    dataframe: pd.DataFrame,
    filename: str,
) -> None:
    """Display uploaded dataset metadata."""

    file_type = (
        Path(filename)
        .suffix
        .upper()
        .replace(".", "")
    )

    st.write(f"**Filename:** {filename}")
    st.write(f"**File Type:** {file_type}")

    st.subheader("Columns")

    column_names = list(dataframe.columns)

    if not column_names:
        st.warning(
            "The uploaded dataset does not contain any columns."
        )
        return

    st.write(
        ", ".join(
            str(column)
            for column in column_names
        )
    )


def _render_dataset_preview(
    dataframe: pd.DataFrame,
) -> None:
    """Display an interactive preview of the dataset."""

    st.subheader("Dataset Preview")

    column_names = list(dataframe.columns)

    if not column_names:
        st.info("No columns are available for preview.")
        return

    selected_columns = st.multiselect(
        "Select columns to preview",
        options=column_names,
        default=column_names,
        key="preview_columns",
    )

    selected_rows = st.selectbox(
        "Number of rows to preview",
        options=[5, 10, 25, 50, 100],
        index=0,
        key="preview_row_count",
    )

    if selected_columns:
        st.dataframe(
            dataframe[selected_columns].head(selected_rows),
            use_container_width=True,
        )
    else:
        st.info(
            "Select at least one column to display the preview."
        )


def _render_missing_value_summary(
    dataframe: pd.DataFrame,
) -> None:
    """Display missing-value counts for each column."""

    st.subheader("Missing-Value Summary")

    missing_values = (
        dataframe.isna()
        .sum()
        .reset_index()
    )

    missing_values.columns = [
        "column",
        "missing_count",
    ]

    st.dataframe(
        missing_values,
        use_container_width=True,
    )


def _render_clear_dataset_button() -> None:
    """Display the button for clearing the uploaded dataset."""

    if st.button(
        "Clear uploaded dataset",
        key="clear_uploaded_dataset",
    ):
        clear_uploaded_dataset()
        st.rerun()


def render() -> None:
    """Render the dataset upload page."""

    st.title("Dataset Upload")

    st.write(
        "Upload a CSV or JSON dataset to preview "
        "its contents dynamically."
    )

    uploaded_file = st.file_uploader(
        "Upload a dataset",
        type=["csv", "json"],
        key="dataset_uploader",
    )

    if uploaded_file is not None:
        current_filename = get_uploaded_filename()

        if current_filename != uploaded_file.name:
            try:
                dataframe = load_uploaded_dataset(
                    uploaded_file
                )

                store_uploaded_dataset(
                    dataframe,
                    uploaded_file.name,
                )

                st.success(
                    f"Successfully uploaded "
                    f"{uploaded_file.name}."
                )

            except (
                ValueError,
                OSError,
                pd.errors.ParserError,
            ) as exc:
                st.error(
                    "Unable to read the uploaded dataset. "
                    "Please verify the file format."
                )
                st.caption(str(exc))

    dataframe = st.session_state.get(
        "uploaded_dataframe"
    )

    if dataframe is None:
        st.info(
            "Upload a CSV or JSON dataset to begin."
        )
        return

    filename = get_uploaded_filename()

    if filename is None:
        filename = "Uploaded dataset"

    _render_dataset_summary(dataframe)
    _render_dataset_metadata(
        dataframe,
        filename,
    )
    _render_dataset_preview(dataframe)
    _render_missing_value_summary(dataframe)
    _render_clear_dataset_button()