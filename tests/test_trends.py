import numpy as np
import pandas as pd
import pytest

from src.analysis.trends import (
    add_rolling_metrics,
    assign_productivity_segments,
    calculate_department_productivity,
    calculate_employee_productivity_scores,
    calculate_monthly_onboarding_trend,
    calculate_segment_summary,
    calculate_trend_change,
    prepare_hire_date,
    run_trend_segmentation_pipeline,
)


@pytest.fixture
def sample_employee_data():
    return pd.DataFrame(
        {
            "EmpID": [
                1,
                2,
                3,
                4,
                5,
                6,
            ],
            "DateofHire": [
                "2024-01-10",
                "2024-01-15",
                "2024-02-10",
                "2024-02-20",
                "2024-03-05",
                "2024-03-15",
            ],
            "Department": [
                "IT/IS",
                "IT/IS",
                "Production",
                "Production",
                "Sales",
                "Sales",
            ],
            "onboarding_completion_rate": [
                60,
                70,
                80,
                90,
                50,
                100,
            ],
            "learning_completion_rate": [
                50,
                60,
                70,
                80,
                40,
                90,
            ],
            "average_assessment_score": [
                60,
                70,
                80,
                90,
                50,
                100,
            ],
            "total_usage_records": [
                10,
                20,
                30,
                40,
                5,
                50,
            ],
            "total_support_tickets": [
                3,
                2,
                4,
                3,
                6,
                1,
            ],
            "open_support_tickets": [
                1,
                1,
                2,
                1,
                4,
                0,
            ],
        }
    )


def test_prepare_hire_date_converts_dates(
    sample_employee_data,
):
    result = prepare_hire_date(sample_employee_data)

    assert pd.api.types.is_datetime64_any_dtype(
        result["DateofHire"]
    )


def test_monthly_trend_groups_by_month(
    sample_employee_data,
):
    result = calculate_monthly_onboarding_trend(
        sample_employee_data
    )

    assert len(result) == 3

    assert list(result["employee_count"]) == [
        2,
        2,
        2,
    ]

    assert result.loc[
        0,
        "average_onboarding_completion_rate",
    ] == pytest.approx(65)

    assert result.loc[
        1,
        "average_onboarding_completion_rate",
    ] == pytest.approx(85)

    assert result.loc[
        2,
        "average_onboarding_completion_rate",
    ] == pytest.approx(75)


def test_rolling_metrics_are_calculated(
    sample_employee_data,
):
    trend = calculate_monthly_onboarding_trend(
        sample_employee_data
    )

    result = add_rolling_metrics(
        trend,
        window=2,
    )

    assert (
        "rolling_onboarding_completion_rate"
        in result.columns
    )

    assert result.loc[
        0,
        "rolling_onboarding_completion_rate",
    ] == pytest.approx(65)

    assert result.loc[
        1,
        "rolling_onboarding_completion_rate",
    ] == pytest.approx(75)

    assert result.loc[
        2,
        "rolling_onboarding_completion_rate",
    ] == pytest.approx(80)


def test_trend_change_calculates_difference(
    sample_employee_data,
):
    trend = calculate_monthly_onboarding_trend(
        sample_employee_data
    )

    result = calculate_trend_change(trend)

    assert pd.isna(
        result.loc[
            0,
            "onboarding_completion_change",
        ]
    )

    assert result.loc[
        1,
        "onboarding_completion_change",
    ] == pytest.approx(20)

    assert result.loc[
        2,
        "onboarding_completion_change",
    ] == pytest.approx(-10)


def test_productivity_scores_are_between_zero_and_100(
    sample_employee_data,
):
    result = calculate_employee_productivity_scores(
        sample_employee_data
    )

    assert len(result) == 6

    assert (
        result["productivity_score"]
        .between(0, 100)
        .all()
    )


def test_highest_employee_has_high_productivity_score(
    sample_employee_data,
):
    result = calculate_employee_productivity_scores(
        sample_employee_data
    )

    highest_score = result.loc[
        result["EmpID"] == 6,
        "productivity_score",
    ].iloc[0]

    lowest_score = result.loc[
        result["EmpID"] == 5,
        "productivity_score",
    ].iloc[0]

    assert highest_score > lowest_score


def test_productivity_segments_are_assigned(
    sample_employee_data,
):
    scores = calculate_employee_productivity_scores(
        sample_employee_data
    )

    result = assign_productivity_segments(scores)

    assert "productivity_segment" in result.columns

    valid_segments = {
        "Low Productivity",
        "Medium Productivity",
        "High Productivity",
    }

    actual_segments = set(
        result["productivity_segment"]
        .dropna()
        .astype(str)
    )

    assert actual_segments.issubset(valid_segments)


def test_segment_summary_counts_employees(
    sample_employee_data,
):
    scores = calculate_employee_productivity_scores(
        sample_employee_data
    )

    segmented = assign_productivity_segments(
        scores
    )

    result = calculate_segment_summary(segmented)

    assert "employee_count" in result.columns

    assert (
        result["employee_count"].sum()
        == len(sample_employee_data)
    )


def test_department_productivity_groups_employees(
    sample_employee_data,
):
    scores = calculate_employee_productivity_scores(
        sample_employee_data
    )

    segmented = assign_productivity_segments(
        scores
    )

    segmented = segmented.merge(
        sample_employee_data[
            ["EmpID", "Department"]
        ],
        on="EmpID",
        how="left",
    )

    result = calculate_department_productivity(
        segmented
    )

    assert len(result) == 3

    assert set(result["Department"]) == {
        "IT/IS",
        "Production",
        "Sales",
    }

    assert (
        result["employee_count"].sum()
        == len(sample_employee_data)
    )


def test_pipeline_returns_all_results(
    sample_employee_data,
    tmp_path,
):
    input_path = (
        tmp_path / "employee_analytics.csv"
    )

    output_directory = (
        tmp_path / "trend_results"
    )

    sample_employee_data.to_csv(
        input_path,
        index=False,
    )

    results = run_trend_segmentation_pipeline(
        input_path,
        output_directory,
    )

    assert "monthly_trends" in results
    assert "productivity_scores" in results
    assert "productivity_segments" in results
    assert "segment_summary" in results
    assert "department_productivity" in results

    assert not results[
        "monthly_trends"
    ].empty

    assert not results[
        "productivity_scores"
    ].empty

    assert not results[
        "productivity_segments"
    ].empty

    assert not results[
        "segment_summary"
    ].empty

    assert not results[
        "department_productivity"
    ].empty

    assert (
        output_directory
        / "monthly_trends.csv"
    ).exists()

    assert (
        output_directory
        / "productivity_scores.csv"
    ).exists()

    assert (
        output_directory
        / "productivity_segments.csv"
    ).exists()

    assert (
        output_directory
        / "segment_summary.csv"
    ).exists()

    assert (
        output_directory
        / "department_productivity.csv"
    ).exists()


def test_missing_date_column_raises_error():
    df = pd.DataFrame(
        {
            "EmpID": [1, 2],
        }
    )

    with pytest.raises(KeyError):
        calculate_monthly_onboarding_trend(df)


def test_invalid_rolling_window_raises_error(
    sample_employee_data,
):
    trend = calculate_monthly_onboarding_trend(
        sample_employee_data
    )

    with pytest.raises(ValueError):
        add_rolling_metrics(
            trend,
            window=0,
        )