"""Main Streamlit entry point for OnboardIQ."""

from __future__ import annotations

import streamlit as st

from src.config.settings import APP_NAME
from src.dashboard.data import load_dashboard_dataset
from src.dashboard.layout import (
    configure_page,
    render_sidebar_footer,
)
from src.dashboard.navigation import render_navigation
from src.dashboard.pages import (
    analytics,
    dashboard,
    data_preview,
    dataset_upload,
    employees,
    kpi_dashboard,
    onboarding,
)
from src.dashboard.session import initialize_session_state


def main() -> None:
    """Run the OnboardIQ Streamlit application."""

    configure_page()
    initialize_session_state()

    selected_page = render_navigation()
    dataframe = load_dashboard_dataset()

    # Filters are currently disabled.
    # An empty dictionary keeps the page interfaces
    # compatible until filtering is re-enabled.
    filters = {}

    render_sidebar_footer()

    pages = {
        "dashboard": lambda: dashboard.render(
            dataframe=dataframe,
            filters=filters,
        ),
        "onboarding": lambda: onboarding.render(
            dataframe=dataframe,
            filters=filters,
        ),
        "employees": lambda: employees.render(
            dataframe=dataframe,
            filters=filters,
        ),
        "analytics": lambda: analytics.render(
            dataframe=dataframe,
            filters=filters,
        ),
        "data_preview": data_preview.render,
        "kpi_dashboard": lambda: kpi_dashboard.render_kpi_dashboard(
            dataframe=dataframe,
        ),
        "dataset_upload": dataset_upload.render,
    }

    page = pages.get(selected_page)

    if page is not None:
        page()
    elif selected_page == "dataset_upload":
        st.info(
            "Dataset upload is currently managed through "
            "the dashboard data interface."
        )
    else:
        st.error(
            f"Unknown dashboard page selected for {APP_NAME}."
        )


if __name__ == "__main__":
    main()