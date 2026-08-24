"""Main dashboard page."""

import pandas as pd
import streamlit as st

from src.dashboard.filters import filter_dataframe
from src.dashboard.layout import (
    render_empty_state,
    render_header,
    render_metric_cards,
)


def render(
    dataframe: pd.DataFrame | None = None,
    filters: dict[str, str] | None = None,
) -> None:
    """Render the main dashboard page."""
    render_header(
        "OnboardIQ Dashboard",
        "Employee onboarding analytics and productivity overview.",
    )

    st.markdown(
        """
        Welcome to **OnboardIQ**.

        This dashboard brings employee onboarding, learning,
        internal tool usage, and support information into one place.
        """
    )

    if dataframe is None or dataframe.empty:
        render_empty_state(
            "No dataset available",
            (
                "Upload a dataset from the Data Preview page "
                "to enable interactive filtering."
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

    st.divider()

    render_metric_cards(
        [
            {
                "label": "Filtered Employees",
                "value": str(len(filtered_dataframe)),
                "help": (
                    "Number of employees remaining "
                    "after applying the active filters."
                ),
            },
            {
                "label": "Total Columns",
                "value": str(
                    len(filtered_dataframe.columns)
                ),
                "help": "Columns available in the filtered dataset.",
            },
        ]
    )

    st.divider()

    st.subheader("Filtered Dataset")

    st.dataframe(
        filtered_dataframe.head(100),
        use_container_width=True,
    )