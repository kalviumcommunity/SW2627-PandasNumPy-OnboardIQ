import streamlit as st

from src.dashboard.layout import (
    render_empty_state,
    render_header,
)


def render() -> None:
    """Render the analytics page."""
    render_header(
        "Analytics",
        "Explore onboarding, learning, tool usage, and support analytics.",
    )

    st.subheader("Analytics Workspace")

    render_empty_state(
        "Analytics modules",
        (
            "The analytics workspace is ready for integration "
            "with the existing analysis and SQL reporting modules."
        ),
    )