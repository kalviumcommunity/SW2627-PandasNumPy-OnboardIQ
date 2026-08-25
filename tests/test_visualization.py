"""Tests for OnboardIQ business visualizations."""

import pandas as pd
import pytest

from src.visualization.charts import (
    learning_completion_chart,
    onboarding_completion_chart,
    onboarding_vs_learning_chart,
    productivity_by_department_chart,
    support_ticket_chart,
)


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame(
        {
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
                75.0,
            ],
            "learning_completion_rate": [
                60.0,
                80.0,
                65.0,
                70.0,
            ],
            "average_daily_active_usage": [
                90,
                100,
                70,
                80,
            ],
            "EngagementSurvey": [
                4.2,
                4.5,
                3.8,
                4.0,
            ],
            "total_support_tickets": [
                5,
                3,
                8,
                4,
            ],
        }
    )


def test_onboarding_completion_chart(sample_dataframe):
    figure = onboarding_completion_chart(sample_dataframe)

    assert figure is not None
    assert len(figure.data) == 1
    assert figure.layout.title.text == (
        "Onboarding Completion Rate by Department"
    )


def test_productivity_by_department_chart(sample_dataframe):
    figure = productivity_by_department_chart(sample_dataframe)

    assert figure is not None
    assert len(figure.data) == 2


def test_support_ticket_chart(sample_dataframe):
    figure = support_ticket_chart(sample_dataframe)

    assert figure is not None
    assert len(figure.data) == 1


def test_learning_completion_chart(sample_dataframe):
    figure = learning_completion_chart(sample_dataframe)

    assert figure is not None
    assert len(figure.data) == 1


def test_onboarding_vs_learning_chart(sample_dataframe):
    figure = onboarding_vs_learning_chart(sample_dataframe)

    assert figure is not None
    assert len(figure.data) == 2


def test_missing_columns_raise_error():
    dataframe = pd.DataFrame(
        {
            "Department": ["IT/IS"],
        }
    )

    with pytest.raises(ValueError):
        onboarding_completion_chart(dataframe)