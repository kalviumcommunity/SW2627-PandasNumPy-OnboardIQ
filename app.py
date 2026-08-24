"""Main Streamlit entry point for OnboardIQ."""

import io
from pathlib import Path

import pandas as pd
import streamlit as st

from src.config.settings import APP_NAME
from src.dashboard.filters import render_filter_sidebar
from src.dashboard.layout import (
    configure_page,
    render_active_filters,
    render_sidebar_footer,
)
from src.dashboard.navigation import render_navigation
from src.dashboard.session import initialize_session_state
from src.dashboard.pages import (
    analytics,
    dashboard,
    data_preview,
    employees,
    onboarding,
)


def load_uploaded_dataset(uploaded_file) -> pd.DataFrame:
    """Read and validate an uploaded CSV or JSON dataset."""
    file_name = uploaded_file.name
    extension = Path(file_name).suffix.lower()

    if extension not in {".csv", ".json"}:
        raise ValueError(
            "Unsupported file type. Please upload a CSV or JSON file."
        )

    file_content = uploaded_file.getvalue()

    if not file_content:
        raise ValueError(
            "The uploaded file is empty."
        )

    if extension == ".csv":
        dataframe = pd.read_csv(
            io.BytesIO(file_content)
        )

        if dataframe.empty:
            raise ValueError(
                "The uploaded CSV file contains no data."
            )

        return dataframe

    try:
        dataframe = pd.read_json(
            io.BytesIO(file_content)
        )
    except ValueError as exc:
        raise ValueError(
            "Unable to read the uploaded dataset. "
            "Please verify the file format."
        ) from exc

    if dataframe.empty:
        raise ValueError(
            "The uploaded JSON file contains no data."
        )

    return dataframe


def display_dataset() -> None:
    """Display uploaded dataset metadata and preview."""
    dataframe = st.session_state.get(
        "uploaded_dataframe"
    )

    if dataframe is None:
        return

    filename = st.session_state.get(
        "uploaded_filename",
        "Uploaded dataset",
    )

    file_type = (
        Path(filename)
        .suffix
        .upper()
        .replace(".", "")
    )

    st.subheader("Dataset Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Rows",
        len(dataframe),
    )

    col2.metric(
        "Columns",
        len(dataframe.columns),
    )

    col3.metric(
        "Missing Values",
        int(dataframe.isna().sum().sum()),
    )

    memory_usage = dataframe.memory_usage(
        deep=True
    ).sum()

    col4.metric(
        "Memory Usage",
        f"{memory_usage / 1024:.1f} KB",
    )

    st.write(
        f"**Filename:** {filename}"
    )

    st.write(
        f"**File Type:** {file_type}"
    )

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

    st.subheader("Dataset Preview")

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
            dataframe[selected_columns].head(
                selected_rows
            ),
            use_container_width=True,
        )
    else:
        st.info(
            "Select at least one column to display the preview."
        )

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

    if st.button(
        "Clear uploaded dataset",
        key="clear_uploaded_dataset",
    ):
        st.session_state["uploaded_dataframe"] = None
        st.session_state["uploaded_filename"] = None

        st.rerun()


def render_dataset_upload() -> None:
    """Render the dataset upload interface."""
    st.header("Dataset Upload")

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
        current_filename = st.session_state.get(
            "uploaded_filename"
        )

        if current_filename != uploaded_file.name:
            try:
                dataframe = load_uploaded_dataset(
                    uploaded_file
                )

                st.session_state[
                    "uploaded_dataframe"
                ] = dataframe

                st.session_state[
                    "uploaded_filename"
                ] = uploaded_file.name

                st.success(
                    f"Successfully uploaded "
                    f"{uploaded_file.name}."
                )

            except (
                ValueError,
                OSError,
                pd.errors.ParserError,
            ):
                st.error(
                    "Unable to read the uploaded dataset. "
                    "Please verify the file format."
                )

            except Exception:
                st.error(
                    "Unable to read the uploaded dataset. "
                    "Please verify the file format."
                )

    display_dataset()


def get_dashboard_dataframe() -> pd.DataFrame | None:
    """
    Return the dataset currently available to the dashboard.

    Uploaded data takes priority over the processed project dataset.
    """
    uploaded_dataframe = st.session_state.get(
        "uploaded_dataframe"
    )

    if uploaded_dataframe is not None:
        return uploaded_dataframe.copy()

    processed_path = Path(
        "data/processed/employee_onboarding_analytics.csv"
    )

    if processed_path.exists():
        try:
            dataframe = pd.read_csv(
                processed_path
            )

            if not dataframe.empty:
                return dataframe

        except (
            OSError,
            pd.errors.ParserError,
        ):
            return None

    return None


def main() -> None:
    """Run the OnboardIQ Streamlit application."""
    configure_page()

    initialize_session_state()

    selected_page = render_navigation()

    dataframe = get_dashboard_dataframe()

    filters = render_filter_sidebar(
        dataframe
    )

    render_active_filters(filters)

    render_sidebar_footer()

    if selected_page == "dashboard":
        dashboard.render(
            dataframe=dataframe,
            filters=filters,
        )

    elif selected_page == "onboarding":
        onboarding.render(
            dataframe=dataframe,
            filters=filters,
        )

    elif selected_page == "employees":
        employees.render(
            dataframe=dataframe,
            filters=filters,
        )

    elif selected_page == "analytics":
        analytics.render(
            dataframe=dataframe,
            filters=filters,
        )

    elif selected_page == "data_preview":
        data_preview.render()

    else:
        st.error(
            f"Unknown dashboard page selected for "
            f"{APP_NAME}."
        )


if __name__ == "__main__":
    main()