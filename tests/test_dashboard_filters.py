"""Tests for dashboard filtering helpers."""

import pandas as pd

from src.dashboard.filters import filter_dataframe


def create_test_dataframe() -> pd.DataFrame:
    """Create a small dataframe for filter tests."""
    return pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "department": [
                "Engineering",
                "Engineering",
                "HR",
                "Sales",
            ],
            "employee_type": [
                "Full-time",
                "Contract",
                "Full-time",
                "Full-time",
            ],
            "onboarding_status": [
                "Completed",
                "In Progress",
                "Completed",
                "In Progress",
            ],
        }
    )


def test_no_filters_returns_all_rows():
    """All rows should remain when no filters are applied."""
    dataframe = create_test_dataframe()

    result = filter_dataframe(dataframe)

    assert len(result) == 4


def test_department_filter():
    """Department filtering should return matching rows only."""
    dataframe = create_test_dataframe()

    result = filter_dataframe(
        dataframe,
        department="Engineering",
    )

    assert len(result) == 2
    assert set(result["department"]) == {
        "Engineering"
    }


def test_employee_type_filter():
    """Employee type filtering should return matching rows."""
    dataframe = create_test_dataframe()

    result = filter_dataframe(
        dataframe,
        employee_type="Contract",
    )

    assert len(result) == 1
    assert result.iloc[0]["employee_id"] == 2


def test_onboarding_status_filter():
    """Onboarding status filtering should work correctly."""
    dataframe = create_test_dataframe()

    result = filter_dataframe(
        dataframe,
        onboarding_status="Completed",
    )

    assert len(result) == 2
    assert set(result["onboarding_status"]) == {
        "Completed"
    }


def test_multiple_filters():
    """Multiple filters should be applied together."""
    dataframe = create_test_dataframe()

    result = filter_dataframe(
        dataframe,
        department="Engineering",
        employee_type="Full-time",
        onboarding_status="Completed",
    )

    assert len(result) == 1
    assert result.iloc[0]["employee_id"] == 1


def test_missing_filter_column_does_not_crash():
    """Missing optional columns should not cause an exception."""
    dataframe = pd.DataFrame(
        {
            "employee_id": [1, 2],
            "department": [
                "Engineering",
                "HR",
            ],
        }
    )

    result = filter_dataframe(
        dataframe,
        employee_type="Full-time",
        onboarding_status="Completed",
    )

    assert len(result) == 2


def test_original_dataframe_is_not_modified():
    """Filtering should not mutate the original dataframe."""
    dataframe = create_test_dataframe()
    original_columns = list(dataframe.columns)
    original_length = len(dataframe)

    filter_dataframe(
        dataframe,
        department="Engineering",
    )

    assert list(dataframe.columns) == original_columns
    assert len(dataframe) == original_length