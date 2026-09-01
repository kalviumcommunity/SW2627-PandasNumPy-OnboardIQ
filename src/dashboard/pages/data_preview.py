import streamlit as st

from src.dashboard.layout import (
    render_empty_state,
    render_header,
)


def render() -> None:
    """Render the data preview page."""
    render_header(
        "Data Preview",
        "Preview uploaded datasets and inspect their structure.",
    )

    st.subheader("Dataset Preview")

    render_empty_state(
        "Dataset upload",
        (
            "Dataset upload and dynamic preview functionality "
            "is not yet implemented. Please upload a dataset to "
        ),
    )