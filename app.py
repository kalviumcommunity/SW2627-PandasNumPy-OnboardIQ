import io
from pathlib import Path

import pandas as pd
import streamlit as st

from src.ingestion.loader import IngestionError, load_csv, load_json


st.set_page_config(
    page_title="OnboardIQ - Dataset Upload",
    page_icon="📊",
    layout="wide",
)


def load_uploaded_dataset(uploaded_file) -> pd.DataFrame:
    """Read and validate an uploaded CSV or JSON dataset."""
    file_name = uploaded_file.name
    extension = Path(file_name).suffix.lower()

    if extension not in {".csv", ".json"}:
        raise ValueError("Unsupported file type. Please upload a CSV or JSON file.")

    file_content = uploaded_file.getvalue()

    if not file_content:
        raise ValueError("The uploaded file is empty.")

    if extension == ".csv":
        dataframe = pd.read_csv(io.BytesIO(file_content))

        if dataframe.empty:
            raise ValueError("The uploaded CSV file contains no data.")

        return dataframe

    try:
        dataframe = pd.read_json(io.BytesIO(file_content))
    except ValueError as exc:
        raise ValueError(
            "Unable to read the uploaded dataset. Please verify the file format."
        ) from exc

    if dataframe.empty:
        raise ValueError("The uploaded JSON file contains no data.")

    return dataframe


def initialize_session_state() -> None:
    """Initialize session-state values used by the upload page."""
    if "uploaded_dataframe" not in st.session_state:
        st.session_state["uploaded_dataframe"] = None

    if "uploaded_filename" not in st.session_state:
        st.session_state["uploaded_filename"] = None


def display_dataset() -> None:
    """Display metadata, controls, preview, and missing-value summary."""
    dataframe = st.session_state.get("uploaded_dataframe")

    if dataframe is None:
        st.info("Upload a CSV or JSON dataset to begin.")
        return

    filename = st.session_state.get("uploaded_filename", "Uploaded dataset")
    file_type = Path(filename).suffix.upper().replace(".", "")

    st.subheader("Dataset Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", len(dataframe))
    col2.metric("Columns", len(dataframe.columns))
    col3.metric(
        "Missing Values",
        int(dataframe.isna().sum().sum()),
    )

    memory_usage = dataframe.memory_usage(deep=True).sum()
    col4.metric(
        "Memory Usage",
        f"{memory_usage / 1024:.1f} KB",
    )

    st.write(f"**Filename:** {filename}")
    st.write(f"**File Type:** {file_type}")

    st.subheader("Columns")

    column_names = list(dataframe.columns)

    if column_names:
        st.write(", ".join(str(column) for column in column_names))
    else:
        st.warning("The uploaded dataset does not contain any columns.")
        return

    st.subheader("Dataset Preview")

    selected_columns = st.multiselect(
        "Select columns to preview",
        options=column_names,
        default=column_names,
    )

    selected_rows = st.selectbox(
        "Number of rows to preview",
        options=[5, 10, 25, 50, 100],
        index=0,
    )

    if selected_columns:
        st.dataframe(
            dataframe[selected_columns].head(selected_rows),
            use_container_width=True,
        )
    else:
        st.info("Select at least one column to display the preview.")

    st.subheader("Missing-Value Summary")

    missing_values = dataframe.isna().sum().reset_index()
    missing_values.columns = ["column", "missing_count"]

    st.dataframe(
        missing_values,
        use_container_width=True,
    )

    if st.button("Clear uploaded dataset"):
        st.session_state.pop("uploaded_dataframe", None)
        st.session_state.pop("uploaded_filename", None)
        st.rerun()


def main() -> None:
    """Run the OnboardIQ Streamlit application."""
    initialize_session_state()

    st.title("OnboardIQ")
    st.header("Dataset Upload")

    st.write(
        "Upload a CSV or JSON dataset to preview its contents dynamically."
    )

    uploaded_file = st.file_uploader(
        "Upload a dataset",
        type=["csv", "json"],
    )

    if uploaded_file is not None:
        current_filename = st.session_state.get("uploaded_filename")

        if current_filename != uploaded_file.name:
            try:
                dataframe = load_uploaded_dataset(uploaded_file)

                st.session_state["uploaded_dataframe"] = dataframe
                st.session_state["uploaded_filename"] = uploaded_file.name

                st.success(
                    f"Successfully uploaded {uploaded_file.name}."
                )

            except (ValueError, IngestionError, OSError, pd.errors.ParserError):
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


if __name__ == "__main__":
    main()