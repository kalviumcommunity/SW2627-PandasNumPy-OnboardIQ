import streamlit as st

from src.dashboard.layout import (
    render_empty_state,
    render_header,
)


def render() -> None:
    """Render the employees page."""
    render_header(
        "Employees",
        "Explore employee-level onboarding and productivity information.",
    )

    st.subheader("Employee Directory")

    render_empty_state(
        "Employee data",
        (
            "The employee page structure is ready. "
            "Employee-level tables, filters, and details "
            "will be connected to the project data in a later issue."
        ),
    )