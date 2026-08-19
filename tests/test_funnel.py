import pandas as pd
import pytest

from src.analysis.funnel import (
    calculate_funnel_analysis,
    identify_funnel_dropoffs,
    run_funnel_pipeline,
)


@pytest.fixture
def funnel_dataframe():
    return pd.DataFrame(
        {
            "EmpID": range(1, 11),
            "onboarding_completion_rate": [
                100,
                100,
                90,
                80,
                75,
                60,
                50,
                40,
                20,
                0,
            ],
            "learning_completion_rate": [
                100,
                100,
                100,
                90,
                80,
                70,
                60,
                50,
                20,
                0,
            ],
            "total_usage_records": [
                10,
                10,
                10,
                10,
                10,
                10,
                10,
                10,
                0,
                0,
            ],
        }
    )


def test_funnel_contains_expected_stages(
    funnel_dataframe,
):
    result = calculate_funnel_analysis(
        funnel_dataframe
    )

    assert list(result["stage"]) == [
        "employees",
        "onboarding_started",
        "onboarding_50_percent",
        "onboarding_75_percent",
        "onboarding_completed",
        "learning_completed",
        "tool_adopted",
    ]


def test_funnel_employee_counts(
    funnel_dataframe,
):
    result = calculate_funnel_analysis(
        funnel_dataframe
    )

    assert result.loc[
        result["stage"] == "employees",
        "employee_count",
    ].iloc[0] == 10

    assert result.loc[
        result["stage"] == "onboarding_50_percent",
        "employee_count",
    ].iloc[0] == 7

    assert result.loc[
        result["stage"] == "onboarding_75_percent",
        "employee_count",
    ].iloc[0] == 5

    assert result.loc[
        result["stage"] == "onboarding_completed",
        "employee_count",
    ].iloc[0] == 2


def test_funnel_conversion_rates(
    funnel_dataframe,
):
    result = calculate_funnel_analysis(
        funnel_dataframe
    )

    employees = result.iloc[0]

    assert employees["overall_conversion_rate"] == pytest.approx(
        100.0
    )

    completed = result[
        result["stage"] == "onboarding_completed"
    ].iloc[0]

    assert completed["overall_conversion_rate"] == pytest.approx(
        20.0
    )


def test_dropoff_identification(
    funnel_dataframe,
):
    funnel = calculate_funnel_analysis(
        funnel_dataframe
    )

    result = identify_funnel_dropoffs(
        funnel
    )

    assert "drop_off_flag" in result.columns

    assert set(
        result["drop_off_flag"]
    ).issubset(
        {"low", "moderate", "high"}
    )


def test_empty_dataframe_raises_error():
    df = pd.DataFrame()

    with pytest.raises(ValueError):
        calculate_funnel_analysis(df)


def test_pipeline_can_save_results(
    funnel_dataframe,
    tmp_path,
):
    input_path = (
        tmp_path / "employee_analytics.csv"
    )

    output_directory = (
        tmp_path / "funnel_results"
    )

    funnel_dataframe.to_csv(
        input_path,
        index=False,
    )

    results = run_funnel_pipeline(
        input_path,
        output_directory,
    )

    assert "funnel_analysis" in results
    assert "funnel_dropoffs" in results

    assert (
        output_directory
        / "funnel_analysis.csv"
    ).exists()

    assert (
        output_directory
        / "funnel_dropoffs.csv"
    ).exists()