import streamlit as st

from src.config.settings import APP_NAME
from src.dashboard.layout import (
    configure_page,
    render_sidebar_footer,
)
from src.dashboard.navigation import render_navigation
from src.dashboard.pages import (
    analytics,
    dashboard,
    data_preview,
    employees,
    onboarding,
)


def main() -> None:
    """Run the OnboardIQ Streamlit application."""
    configure_page()

    selected_page = render_navigation()

    render_sidebar_footer()

    if selected_page == "dashboard":
        dashboard.render()

    elif selected_page == "onboarding":
        onboarding.render()

    elif selected_page == "employees":
        employees.render()

    elif selected_page == "analytics":
        analytics.render()

    elif selected_page == "data_preview":
        data_preview.render()

    else:
        st.error(
            f"Unknown dashboard page selected for {APP_NAME}."
        )


if __name__ == "__main__":
    main()