"""Tests for OnboardIQ Plotly dashboard visualizations."""

import pandas as pd
import pytest

from src.dashboard.visualizations import (
    create_learning_completion_chart,
    create_onboarding_completion_chart,
    create_onboarding_learning_scatter,
    create_productivity_by_department_chart,
    create_support_tickets_chart,
    create_tool_usage_chart,
)


@pytest.fixture
def sample_dashboard_data():
    """Return representative dashboard data."""

    return pd.DataFrame(
        {
            "Employee_Name": [
                "Employee A",
                "Employee B",
                "Employee C",
                "Employee D",
            ],
            "Department": [
                "IT/IS",
                "IT/IS",
                "Production",
                "Production",
            ],
            "onboarding_completion_rate": [
                80.0,
                90.0,
                70.0,
                85.0,
            ],
            "average_daily_active_usage": [
                90.0,
                100.0,
                70.0,
                80.0,
            ],
            "total_support_tickets": [
                3,
                4,
                8,
                5,
            ],
            "learning_completion_rate": [
                75.0,
                85.0,
                60.0,
                80.0,
            ],
            "total_slack_activity": [
                100,
                120,
                80,
                90,
            ],
            "total_jira_usage": [
                50,
                60,
                40,
                45,
            ],
            "total_github_activity": [
                80,
                90,
                30,
                40,
            ],
            "total_teams_activity": [
                40,
                50,
                70,
                60,
            ],
            "total_workspace_activity": [
                100,
                110,
                90,
                95,
            ],
            "average_completion_percentage": [
                80.0,
                90.0,
                70.0,
                85.0,
            ],
            "average_assessment_score": [
                75.0,
                88.0,
                65.0,
                82.0,
            ],
        }
    )


def test_onboarding_completion_chart_returns_figure(
    sample_dashboard_data,
):
    fig = create_onboarding_completion_chart(
        sample_dashboard_data
    )

    assert fig is not None
    assert len(fig.data) == 1
    assert fig.layout.title.text == (
        "Onboarding Completion by Department"
    )


def test_productivity_chart_returns_figure(
    sample_dashboard_data,
):
    fig = create_productivity_by_department_chart(
        sample_dashboard_data
    )

    assert fig is not None
    assert len(fig.data) == 1


def test_support_chart_returns_figure(
    sample_dashboard_data,
):
    fig = create_support_tickets_chart(
        sample_dashboard_data
    )

    assert fig is not None
    assert len(fig.data) == 1


def test_learning_chart_returns_figure(
    sample_dashboard_data,
):
    fig = create_learning_completion_chart(
        sample_dashboard_data
    )

    assert fig is not None
    assert len(fig.data) == 1


def test_tool_usage_chart_returns_figure(
    sample_dashboard_data,
):
    fig = create_tool_usage_chart(
        sample_dashboard_data
    )

    assert fig is not None
    assert len(fig.data) == 1
    assert len(fig.data[0].x) == 5


def test_scatter_chart_returns_figure(
    sample_dashboard_data,
):
    fig = create_onboarding_learning_scatter(
        sample_dashboard_data
    )

    assert fig is not None
    assert len(fig.data) >= 1


def test_missing_columns_raise_error():
    df = pd.DataFrame(
        {
            "Department": ["IT/IS"],
        }
    )

    with pytest.raises(ValueError):
        create_onboarding_completion_chart(df)