"""Reusable Streamlit layout components."""

from __future__ import annotations

import streamlit as st

from src.config.settings import APP_NAME, VERSION
from src.dashboard.session import reset_dashboard_session


def configure_page() -> None:
    """Configure the Streamlit page."""
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_header(
    title: str,
    subtitle: str | None = None,
) -> None:
    """Render a reusable page header."""
    st.title(title)

    if subtitle:
        st.caption(subtitle)


def render_sidebar_footer() -> None:
    """Render application information and session controls."""
    st.sidebar.divider()

    st.sidebar.caption(APP_NAME)
    st.sidebar.caption(f"Version {VERSION}")

    st.sidebar.divider()

    if st.sidebar.button(
        "Reset Dashboard Session",
        use_container_width=True,
    ):
        reset_dashboard_session()
        st.rerun()


def render_metric_cards(
    metrics: list[dict[str, str]],
) -> None:
    """
    Render reusable metric cards.

    Each metric dictionary should contain:
    - label
    - value
    - optional help
    """
    columns = st.columns(len(metrics))

    for column, metric in zip(columns, metrics):
        with column:
            help_text = metric.get("help")

            st.metric(
                label=metric["label"],
                value=metric["value"],
                help=help_text,
            )


def render_empty_state(
    title: str,
    message: str,
) -> None:
    """Render a reusable empty-state message."""
    st.info(
        f"**{title}**\n\n{message}"
    )


def render_active_filters(
    filters: dict[str, str],
) -> None:
    """Display currently active filters."""
    active_filters = {
        key: value
        for key, value in filters.items()
        if value != "All"
    }

    if not active_filters:
        st.caption("No filters applied.")

        return

    st.caption("Active filters:")

    columns = st.columns(len(active_filters))

    for column, (key, value) in zip(
        columns,
        active_filters.items(),
    ):
        label = key.replace("_", " ").title()

        column.info(
            f"**{label}**\n\n{value}"
        )