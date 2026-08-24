import io
from pathlib import Path

import pandas as pd
import streamlit as st

from src.analysis.kpis import calculate_kpis
from src.dashboard.layout import render_kpi_cards
from src.ingestion.loader import IngestionError, load_csv, load_json


st.set_page_config(
    page_title="OnboardIQ",
    page_icon="📊",
    layout="wide",
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


def initialize_session_state() -> None:
    """Initialize session-state values used by the application."""

    if "uploaded_dataframe" not in st.session_state:
        st.session_state["uploaded_dataframe"] = None

    if "uploaded_filename" not in st.session_state:
        st.session_state["uploaded_filename"] = None


def load_default_dataset() -> pd.DataFrame:
    """Load the default processed employee analytics dataset."""

    if not DEFAULT_DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Default dataset not found: {DEFAULT_DATASET_PATH}"
        )

    dataframe = pd.read_csv(
        DEFAULT_DATASET_PATH
    )

    if dataframe.empty:
        raise ValueError(
            "Default dataset contains no data."
        )

    return dataframe


def display_dataset() -> None:
    """Display metadata, controls, preview, and missing-value summary."""

    dataframe = st.session_state.get(
        "uploaded_dataframe"
    )

    if dataframe is None:
        st.info(
            "Upload a CSV or JSON dataset to begin."
        )
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

    column_names = list(
        dataframe.columns
    )

    if column_names:
        st.write(
            ", ".join(
                str(column)
                for column in column_names
            )
        )
    else:
        st.warning(
            "The uploaded dataset does not contain any columns."
        )
        return

    st.subheader("Dataset Preview")

    selected_columns = st.multiselect(
        "Select columns to preview",
        options=column_names,
        default=column_names,
    )

    selected_rows = st.selectbox(
        "Number of rows to preview",
        options=[
            5,
            10,
            25,
            50,
            100,
        ],
        index=0,
    )

    if selected_columns:
        st.dataframe(
            dataframe[
                selected_columns
            ].head(selected_rows),
            use_container_width=True,
        )
    else:
        st.info(
            "Select at least one column to display the preview."
        )

    st.subheader("Missing-Value Summary")

    missing_values = (
        dataframe
        .isna()
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
        "Clear uploaded dataset"
    ):
        st.session_state.pop(
            "uploaded_dataframe",
            None,
        )

        st.session_state.pop(
            "uploaded_filename",
            None,
        )

        st.rerun()


def display_kpi_dashboard(
    dataframe: pd.DataFrame,
) -> None:
    """Display KPI cards for the supplied dataframe."""

    st.title(
        "OnboardIQ KPI Dashboard"
    )

    st.write(
        "Monitor employee onboarding, learning, "
        "tool adoption, support, assessment, "
        "and productivity readiness."
    )

    try:
        kpi_dataframe = calculate_kpis(
            dataframe
        )

        if kpi_dataframe.empty:
            st.warning(
                "No KPI results are available."
            )
            return

        kpis = (
            kpi_dataframe
            .iloc[0]
            .to_dict()
        )

        render_kpi_cards(kpis)

    except (
        KeyError,
        ValueError,
        TypeError,
    ) as exc:
        st.warning(
            "KPI dashboard cannot be calculated "
            "for this dataset."
        )

        st.caption(
            str(exc)
        )


def main() -> None:
    """Run the OnboardIQ Streamlit application."""

    initialize_session_state()

    st.title("OnboardIQ")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dataset Upload",
            "KPI Dashboard",
        ],
    )

    uploaded_file = st.sidebar.file_uploader(
        "Upload a dataset",
        type=[
            "csv",
            "json",
        ],
    )

    if uploaded_file is not None:
        current_filename = (
            st.session_state.get(
                "uploaded_filename"
            )
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

                st.sidebar.success(
                    f"Successfully uploaded "
                    f"{uploaded_file.name}."
                )

            except (
                ValueError,
                IngestionError,
                OSError,
                pd.errors.ParserError,
            ):
                st.sidebar.error(
                    "Unable to read the uploaded dataset. "
                    "Please verify the file format."
                )

            except Exception:
                st.sidebar.error(
                    "Unable to read the uploaded dataset. "
                    "Please verify the file format."
                )

    uploaded_dataframe = st.session_state.get(
        "uploaded_dataframe"
    )

    if page == "Dataset Upload":
        display_dataset()

    elif page == "KPI Dashboard":

        if uploaded_dataframe is not None:
            display_kpi_dashboard(
                uploaded_dataframe
            )
        else:
            try:
                default_dataframe = (
                    load_default_dataset()
                )

                display_kpi_dashboard(
                    default_dataframe
                )

            except (
                FileNotFoundError,
                ValueError,
                pd.errors.ParserError,
            ) as exc:
                st.error(
                    f"Unable to load dashboard dataset: {exc}"
                )


if __name__ == "__main__":
    main()