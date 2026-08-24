"""Onboarding analytics page."""

import pandas as pd
import streamlit as st

from src.dashboard.filters import filter_dataframe
from src.dashboard.layout import (
    render_empty_state,
    render_header,
)


def render(
    dataframe: pd.DataFrame | None = None,
    filters: dict[str, str] | None = None,
) -> None:
    """Render the onboarding page."""
    render_header(
        "Onboarding",
        "Monitor employee onboarding progress and task completion.",
    )

    if dataframe is None or dataframe.empty:
        render_empty_state(
            "Onboarding data unavailable",
            (
                "Upload or load a dataset to view "
                "onboarding information."
            ),
        )

        return

    filters = filters or {}

    filtered_dataframe = filter_dataframe(
        dataframe,
        department=filters.get(
            "department",
            "All",
        ),
        employee_type=filters.get(
            "employee_type",
            "All",
        ),
        onboarding_status=filters.get(
            "onboarding_status",
            "All",
        ),
    )

    st.subheader("Onboarding Progress")

    st.write(
        f"Showing {len(filtered_dataframe)} "
        f"employee record(s) after filtering."
    )

    if "onboarding_status" in filtered_dataframe.columns:
        status_counts = (
            filtered_dataframe[
                "onboarding_status"
            ]
            .value_counts()
            .rename_axis("status")
            .reset_index(name="employees")
        )

        st.dataframe(
            status_counts,
            use_container_width=True,
        )

    st.subheader("Filtered Onboarding Data")

    st.dataframe(
        filtered_dataframe,
        use_container_width=True,
    )