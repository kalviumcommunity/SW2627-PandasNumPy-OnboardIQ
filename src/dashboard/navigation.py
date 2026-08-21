from dataclasses import dataclass

import streamlit as st


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


def render_navigation() -> str:
    """
    Render the sidebar navigation and return the selected page key.
    """
    st.sidebar.title("OnboardIQ")
    st.sidebar.caption("Employee Onboarding Analytics")

    st.sidebar.divider()

    labels = [
        f"{item.icon}  {item.label}"
        for item in NAVIGATION_ITEMS
    ]

    selected_label = st.sidebar.radio(
        "Navigation",
        labels,
        label_visibility="collapsed",
    )

    selected_item = next(
        item
        for item in NAVIGATION_ITEMS
        if f"{item.icon}  {item.label}" == selected_label
    )

    return selected_item.key