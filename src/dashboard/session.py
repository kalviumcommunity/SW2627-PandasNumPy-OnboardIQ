"""Session-state helpers for the OnboardIQ dashboard."""

from __future__ import annotations

from typing import Any

import streamlit as st


DEFAULT_SESSION_STATE: dict[str, Any] = {
    "selected_department": "All",
    "selected_employee_type": "All",
    "selected_onboarding_status": "All",
    "selected_page": "dashboard",
    "uploaded_dataframe": None,
    "uploaded_filename": None,
}


def initialize_session_state() -> None:
    """Initialize dashboard session-state values if they do not exist."""
    for key, default_value in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def get_session_value(key: str, default: Any = None) -> Any:
    """Return a value stored in Streamlit session state."""
    return st.session_state.get(key, default)


def set_session_value(key: str, value: Any) -> None:
    """Store a value in Streamlit session state."""
    st.session_state[key] = value


def clear_filter_state() -> None:
    """Reset all dashboard filter selections."""
    st.session_state["selected_department"] = "All"
    st.session_state["selected_employee_type"] = "All"
    st.session_state["selected_onboarding_status"] = "All"


def clear_uploaded_dataset() -> None:
    """Remove the uploaded dataset from session state."""
    st.session_state.pop("uploaded_dataframe", None)
    st.session_state.pop("uploaded_filename", None)


def reset_dashboard_session() -> None:
    """Reset filters and uploaded dataset while keeping the app usable."""
    clear_filter_state()
    clear_uploaded_dataset()
    st.session_state["selected_page"] = "dashboard"