"""Main Streamlit entry point for OnboardIQ."""

import io
from pathlib import Path

import pandas as pd
import streamlit as st

from src.analysis.kpis import calculate_kpis
from src.config.settings import APP_NAME
from src.dashboard.filters import render_filter_sidebar
from src.dashboard.layout import (
    configure_page,
    render_active_filters,
    render_kpi_cards,
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


PROJECT_ROOT = Path(__file__).resolve().parent

DEFAULT_DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "employee_onboarding_analytics.csv"
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
        raise ValueError("The uploaded file is empty.")

    if extension == ".csv":
        dataframe = pd.read_csv(io.BytesIO(file_content))

        if dataframe.empty:
            raise ValueError(
                "The uploaded CSV file contains no data."
            )

        return dataframe

    try:
        dataframe = pd.read_json(io.BytesIO(file_content))
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


def load_default_dataset() -> pd.DataFrame:
    """Load the default processed employee analytics dataset."""

    if not DEFAULT_DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Default dataset not found: {DEFAULT_DATASET_PATH}"
        )

    dataframe = pd.read_csv(DEFAULT_DATASET_PATH)

    if dataframe.empty:
        raise ValueError("Default dataset contains no data.")

    return dataframe


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

    if DEFAULT_DATASET_PATH.exists():
        try:
            dataframe = pd.read_csv(DEFAULT_DATASET_PATH)

            if not dataframe.empty:
                return dataframe

        except (OSError, pd.errors.ParserError):
            return None

    return None


def display_dataset() -> None:
    """Display uploaded dataset metadata and preview."""

    dataframe = st.session_state.get("uploaded_dataframe")

    if dataframe is None:
        st.info("Upload a CSV or JSON dataset to begin.")
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

    col1.metric("Rows", len(dataframe))
    col2.metric("Columns", len(dataframe.columns))
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
        ", ".join(str(column) for column in column_names)
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
            dataframe[selected_columns].head(selected_rows),
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


def display_kpi_dashboard(
    dataframe: pd.DataFrame,
) -> None:
    """Display KPI cards for the supplied dataframe."""

    st.title("OnboardIQ KPI Dashboard")

    st.write(
        "Monitor employee onboarding, learning, "
        "tool adoption, support, assessment, "
        "and productivity readiness."
    )

    try:
        kpi_dataframe = calculate_kpis(dataframe)

        if kpi_dataframe.empty:
            st.warning("No KPI results are available.")
            return

        kpis = (
            kpi_dataframe
            .iloc[0]
            .to_dict()
        )

        render_kpi_cards(kpis)

    except (KeyError, ValueError, TypeError) as exc:
        st.warning(
            "KPI dashboard cannot be calculated "
            "for this dataset."
        )
        st.caption(str(exc))


def render_dataset_upload() -> None:
    """Render the dataset upload interface."""

    st.header("Dataset Upload")

    st.write(
        "Upload a CSV or JSON dataset to preview "
        "its contents dynamically."
    )

    uploaded_file = st.sidebar.file_uploader(
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
                    f"Successfully uploaded {uploaded_file.name}."
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

    display_dataset()


def main() -> None:
    """Run the OnboardIQ Streamlit application."""

    configure_page()
    initialize_session_state()

    selected_page = render_navigation()

    dataframe = get_dashboard_dataframe()

    # ------------------------------------------------------------------
    # Filters temporarily disabled.
    # The original filter functionality is kept below for future use.
    # ------------------------------------------------------------------

    # filters = render_filter_sidebar(dataframe)

    # ------------------------------------------------------------------
    # Use an empty filter dictionary while filters are disabled.
    # This keeps the existing page interfaces unchanged.
    # ------------------------------------------------------------------

    filters = {}

    # ------------------------------------------------------------------
    # Active filter display temporarily disabled.
    # ------------------------------------------------------------------

    # render_active_filters(filters)

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

    elif selected_page == "kpi_dashboard":
        if dataframe is not None:
            display_kpi_dashboard(dataframe)
        else:
            st.error(
                "Unable to load dashboard dataset."
            )

    elif selected_page == "dataset_upload":
        render_dataset_upload()

    else:
        st.error(
            f"Unknown dashboard page selected for "
            f"{APP_NAME}."
        )


if __name__ == "__main__":
    main()