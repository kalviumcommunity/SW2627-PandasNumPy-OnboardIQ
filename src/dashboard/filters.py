"""Reusable filtering controls for the OnboardIQ dashboard."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.dashboard.session import (
    clear_filter_state,
    get_session_value,
)


def _get_unique_values(
    dataframe: pd.DataFrame,
    column_name: str,
) -> list[str]:
    """Return sorted non-null unique values from a dataframe column."""
    if column_name not in dataframe.columns:
        return []

    values = (
        dataframe[column_name]
        .dropna()
        .astype(str)
        .str.strip()
    )

    values = values[values != ""]

    return sorted(values.unique().tolist())


def filter_dataframe(
    dataframe: pd.DataFrame,
    department: str = "All",
    employee_type: str = "All",
    onboarding_status: str = "All",
) -> pd.DataFrame:
    """
    Apply dashboard filters to a dataframe.

    Filters are only applied when their corresponding columns exist.
    """
    filtered = dataframe.copy()

    if (
        department != "All"
        and "department" in filtered.columns
    ):
        filtered = filtered[
            filtered["department"].astype(str).str.strip()
            == department
        ]

    if (
        employee_type != "All"
        and "employee_type" in filtered.columns
    ):
        filtered = filtered[
            filtered["employee_type"].astype(str).str.strip()
            == employee_type
        ]

    if (
        onboarding_status != "All"
        and "onboarding_status" in filtered.columns
    ):
        filtered = filtered[
            filtered["onboarding_status"].astype(str).str.strip()
            == onboarding_status
        ]

    return filtered.reset_index(drop=True)


def render_filter_sidebar(
    dataframe: pd.DataFrame | None,
) -> dict[str, str]:
    """
    Render reusable dashboard filters in the sidebar.

    Filter selections are stored in Streamlit session state so they
    persist when the user navigates between dashboard pages.
    """
    if dataframe is None or dataframe.empty:
        return {
            "department": "All",
            "employee_type": "All",
            "onboarding_status": "All",
        }

    st.sidebar.subheader("Filters")

    departments = ["All"] + _get_unique_values(
        dataframe,
        "department",
    )

    employee_types = ["All"] + _get_unique_values(
        dataframe,
        "employee_type",
    )

    onboarding_statuses = ["All"] + _get_unique_values(
        dataframe,
        "onboarding_status",
    )

    selected_department = st.sidebar.selectbox(
        "Department",
        options=departments,
        key="selected_department",
    )

    selected_employee_type = st.sidebar.selectbox(
        "Employee Type",
        options=employee_types,
        key="selected_employee_type",
    )

    selected_onboarding_status = st.sidebar.selectbox(
        "Onboarding Status",
        options=onboarding_statuses,
        key="selected_onboarding_status",
    )

    if st.sidebar.button(
        "Reset Filters",
        use_container_width=True,
    ):
        clear_filter_state()
        st.rerun()

    return {
        "department": selected_department,
        "employee_type": selected_employee_type,
        "onboarding_status": selected_onboarding_status,
    }


def get_filtered_dataframe(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Return a dataframe filtered using current session-state values."""
    return filter_dataframe(
        dataframe,
        department=get_session_value(
            "selected_department",
            "All",
        ),
        employee_type=get_session_value(
            "selected_employee_type",
            "All",
        ),
        onboarding_status=get_session_value(
            "selected_onboarding_status",
            "All",
        ),
    )