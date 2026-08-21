import streamlit as st

from src.dashboard.layout import (
    render_empty_state,
    render_header,
)


def render() -> None:
    """Render the onboarding page."""
    render_header(
        "Onboarding",
        "Monitor employee onboarding progress and task completion.",
    )

    st.subheader("Onboarding Progress")

    render_empty_state(
        "Onboarding analytics",
        (
            "The page structure is ready. "
            "Detailed onboarding metrics and visualizations "
            "will be connected to the reporting layer in a later issue."
        ),
    )