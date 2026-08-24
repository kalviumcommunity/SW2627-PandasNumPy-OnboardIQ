"""Sidebar navigation for the OnboardIQ dashboard."""

from dataclasses import dataclass

import streamlit as st

from src.dashboard.session import initialize_session_state


@dataclass(frozen=True)
class NavigationItem:
    """Represents one dashboard navigation item."""

    label: str
    icon: str
    key: str


NAVIGATION_ITEMS = (
    NavigationItem(
        label="Dashboard",
        icon="🏠",
        key="dashboard",
    ),
    NavigationItem(
        label="Onboarding",
        icon="📋",
        key="onboarding",
    ),
    NavigationItem(
        label="Employees",
        icon="👥",
        key="employees",
    ),
    NavigationItem(
        label="Analytics",
        icon="📈",
        key="analytics",
    ),
    NavigationItem(
        label="Data Preview",
        icon="🗂️",
        key="data_preview",
    ),
)


def _select_page(page_key: str) -> None:
    """Update the currently selected dashboard page."""
    st.session_state["selected_page"] = page_key


def render_navigation() -> str:
    """
    Render sidebar navigation using clickable buttons.

    The selected page is stored in Streamlit session state so that
    navigation persists across Streamlit reruns.
    """
    initialize_session_state()

    st.sidebar.title("OnboardIQ")
    st.sidebar.caption("Employee Onboarding Analytics")

    st.sidebar.divider()

    selected_key = st.session_state.get(
        "selected_page",
        "dashboard",
    )

    for item in NAVIGATION_ITEMS:
        is_selected = item.key == selected_key

        button_label = f"{item.icon}  {item.label}"

        if st.sidebar.button(
            button_label,
            key=f"navigation_{item.key}",
            use_container_width=True,
            type="primary" if is_selected else "secondary",
        ):
            _select_page(item.key)

    return st.session_state["selected_page"]