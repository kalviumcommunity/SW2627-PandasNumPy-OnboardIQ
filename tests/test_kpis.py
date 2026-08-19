import pandas as pd
import pytest

from src.analysis.kpis import (
    calculate_kpis,
    classify_kpi_health,
    run_kpi_pipeline,
)


@pytest.fixture
def kpi_dataframe():
    return pd.DataFrame(
        {
            "EmpID": [1, 2, 3, 4],
            "onboarding_completion_rate": [
                60,
                80,
                90,
                100,
            ],
            "learning_completion_rate": [
                50,
                70,
                90,
                100,
            ],
            "total_usage_records": [
                10,
                20,
                0,
                30,
            ],
            "total_support_tickets": [
                2,
                4,
                6,
                8,
            ],
            "open_support_tickets": [
                1,
                0,
                2,
                0,
            ],
            "average_assessment_score": [
                70,
                80,
                90,
                100,
            ],
            "average_resolution_time_hours": [
                10,
                20,
                30,
                40,
            ],
        }
    )


def test_calculate_kpis(kpi_dataframe):
    result = calculate_kpis(
        kpi_dataframe
    )

    assert len(result) == 1

    row = result.iloc[0]

    assert row["employee_count"] == 4

    assert row[
        "onboarding_completion_rate"
    ] == pytest.approx(82.5)

    assert row[
        "learning_completion_rate"
    ] == pytest.approx(77.5)

    assert row[
        "tool_adoption_rate"
    ] == pytest.approx(75.0)

    assert row[
        "average_support_tickets"
    ] == pytest.approx(5.0)

    assert row[
        "average_open_support_tickets"
    ] == pytest.approx(0.75)

    assert row[
        "open_ticket_rate"
    ] == pytest.approx(50.0)

    assert row[
        "average_assessment_score"
    ] == pytest.approx(85.0)

    assert row[
        "average_resolution_time_hours"
    ] == pytest.approx(25.0)


def test_productivity_readiness_score(
    kpi_dataframe,
):
    result = calculate_kpis(
        kpi_dataframe
    )

    row = result.iloc[0]

    expected = (
        82.5 * 0.4
        + 77.5 * 0.3
        + 75.0 * 0.3
    )

    assert row[
        "productivity_readiness_score"
    ] == pytest.approx(expected)


def test_kpi_health_classification(
    kpi_dataframe,
):
    kpis = calculate_kpis(
        kpi_dataframe
    )

    result = classify_kpi_health(
        kpis
    )

    assert "onboarding_health" in result.columns
    assert "learning_health" in result.columns
    assert "tool_adoption_health" in result.columns
    assert "support_health" in result.columns

    row = result.iloc[0]

    assert row[
        "onboarding_health"
    ] == "healthy"

    assert row[
        "learning_health"
    ] == "attention"

    assert row[
        "tool_adoption_health"
    ] == "attention"

    assert row[
        "support_health"
    ] == "critical"


def test_empty_dataframe_raises_error():
    df = pd.DataFrame()

    with pytest.raises(ValueError):
        calculate_kpis(df)


def test_pipeline_can_save_results(
    kpi_dataframe,
    tmp_path,
):
    input_path = (
        tmp_path / "employee_analytics.csv"
    )

    output_directory = (
        tmp_path / "kpi_results"
    )

    kpi_dataframe.to_csv(
        input_path,
        index=False,
    )

    results = run_kpi_pipeline(
        input_path,
        output_directory,
    )

    assert "kpis" in results
    assert "kpi_health" in results

    assert (
        output_directory / "kpis.csv"
    ).exists()

    assert (
        output_directory / "kpi_health.csv"
    ).exists()