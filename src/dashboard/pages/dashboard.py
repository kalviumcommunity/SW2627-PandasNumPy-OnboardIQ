import streamlit as st

from src.dashboard.layout import (
    render_header,
    render_metric_cards,
)


def render() -> None:
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

    st.divider()

    render_metric_cards(
        [
            {
                "label": "Employees",
                "value": "311",
                "help": "Total employees currently available in the project dataset.",
            },
            {
                "label": "Onboarding Completion",
                "value": "100%",
                "help": "Current onboarding task coverage from the SQL reporting layer.",
            },
            {
                "label": "Learning Completion",
                "value": "69.89%",
                "help": "Learning record completion rate.",
            },
            {
                "label": "Support Tickets",
                "value": "1,048",
                "help": "Total support tickets in the reporting dataset.",
            },
        ]
    )

    st.divider()

    st.subheader("Dashboard Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            """
            **Onboarding**

            Track onboarding progress, task completion,
            delayed tasks, and onboarding health.
            """
        )

    with col2:
        st.info(
            """
            **Analytics**

            Explore employee, department, learning,
            tool usage, and support metrics.
            """
        )