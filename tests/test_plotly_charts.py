"""Tests for reusable Plotly dashboard charts."""

import pandas as pd
import pytest

from src.visualization.plotly_charts import (
    create_activity_vs_support_chart,
    create_department_summary_chart,
    create_engagement_vs_completion_chart,
    create_learning_completion_chart,
    create_onboarding_completion_chart,
    create_performance_distribution_chart,
    create_productivity_by_department_chart,
    create_support_tickets_chart,
    create_tool_usage_chart,
)


@pytest.fixture
def sample_dataframe():
    """Return a small dataframe for chart tests."""
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
            "learning_completion_rate": [
                75.0,
                85.0,
                65.0,
                80.0,
            ],
            "average_daily_active_usage": [
                100.0,
                120.0,
                80.0,
                90.0,
            ],
            "total_support_tickets": [
                3,
                2,
                5,
                4,
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
                70,
                80,
                50,
                55,
            ],
            "total_teams_activity": [
                30,
                40,
                20,
                25,
            ],
            "total_workspace_activity": [
                90,
                100,
                70,
                75,
            ],
            "PerformanceScore": [
                "Exceeds",
                "Fully Meets",
                "Needs Improvement",
                "Fully Meets",
            ],
            "EngagementSurvey": [
                4.5,
                4.0,
                3.2,
                4.2,
            ],
        }
    )


def test_onboarding_completion_chart(sample_dataframe):
    figure = create_onboarding_completion_chart(
        sample_dataframe
    )

    assert figure is not None
    assert len(figure.data) == 1


def test_productivity_chart(sample_dataframe):
    figure = create_productivity_by_department_chart(
        sample_dataframe
    )

    assert figure is not None
    assert len(figure.data) == 1


def test_learning_completion_chart(sample_dataframe):
    figure = create_learning_completion_chart(
        sample_dataframe
    )

    assert figure is not None
    assert len(figure.data) == 1


def test_support_ticket_chart(sample_dataframe):
    figure = create_support_tickets_chart(
        sample_dataframe
    )

    assert figure is not None
    assert len(figure.data) == 1


def test_tool_usage_chart(sample_dataframe):
    figure = create_tool_usage_chart(
        sample_dataframe
    )

    assert figure is not None
    assert len(figure.data) == 1


def test_performance_distribution_chart(sample_dataframe):
    figure = create_performance_distribution_chart(
        sample_dataframe
    )

    assert figure is not None
    assert len(figure.data) == 1


def test_engagement_completion_chart(sample_dataframe):
    figure = create_engagement_vs_completion_chart(
        sample_dataframe
    )

    assert figure is not None
    assert len(figure.data) == 1


def test_activity_support_chart(sample_dataframe):
    figure = create_activity_vs_support_chart(
        sample_dataframe
    )

    assert figure is not None
    assert len(figure.data) == 1


def test_department_summary_chart(sample_dataframe):
    figure = create_department_summary_chart(
        sample_dataframe
    )

    assert figure is not None
    assert len(figure.data) == 2


def test_missing_column_raises_error():
    dataframe = pd.DataFrame(
        {
            "Department": ["IT/IS"],
        }
    )

    with pytest.raises(ValueError):
        create_onboarding_completion_chart(dataframe)