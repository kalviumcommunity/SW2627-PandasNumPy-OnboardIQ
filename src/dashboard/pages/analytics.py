"""Analytics workspace page."""

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
    """Render the analytics page."""
    render_header(
        "Analytics",
        "Explore onboarding, learning, tool usage, and support analytics.",
    )

    if dataframe is None or dataframe.empty:
        render_empty_state(
            "Analytics data unavailable",
            (
                "Upload or load a dataset to enable "
                "the analytics workspace."
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

    st.subheader("Analytics Workspace")

    st.write(
        f"Analytics currently contains "
        f"{len(filtered_dataframe)} record(s)."
    )

    st.dataframe(
        filtered_dataframe,
        use_container_width=True,
    )