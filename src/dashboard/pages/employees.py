"""Employee directory page."""

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
    """Render the employees page."""
    render_header(
        "Employees",
        "Explore employee-level onboarding and productivity information.",
    )

    if dataframe is None or dataframe.empty:
        render_empty_state(
            "Employee data unavailable",
            (
                "Upload or load a dataset to view "
                "employee information."
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

    st.subheader("Employee Directory")

    st.write(
        f"Showing {len(filtered_dataframe)} "
        f"employee record(s)."
    )

    st.dataframe(
        filtered_dataframe,
        use_container_width=True,
    )