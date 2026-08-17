import numpy as np
import pandas as pd
import pytest

from src.analysis.statistics import (
    calculate_correlation_matrix,
    calculate_correlation_pairs,
    calculate_department_insights,
    calculate_department_rankings,
    calculate_descriptive_statistics,
    calculate_distribution_statistics,
    calculate_performance_metrics,
    run_correlation_department_pipeline,
)


def test_calculate_descriptive_statistics():
    df = pd.DataFrame(
        {
            "Salary": [50000, 60000, 70000, 80000],
        }
    )

    result = calculate_descriptive_statistics(
        df,
        columns=["Salary"],
    )

    assert len(result) == 1
    assert result.loc[0, "count"] == 4
    assert result.loc[0, "mean"] == 65000
    assert result.loc[0, "median"] == 65000


def test_calculate_distribution_statistics():
    df = pd.DataFrame(
        {
            "Salary": [50000, 60000, 70000, 80000],
        }
    )

    result = calculate_distribution_statistics(
        df,
        columns=["Salary"],
    )

    assert len(result) == 1
    assert result.loc[0, "min"] == 50000
    assert result.loc[0, "max"] == 80000
    assert result.loc[0, "iqr"] == 15000
    assert result.loc[0, "range"] == 30000


def test_performance_metrics():
    df = pd.DataFrame(
        {
            "onboarding_completion_rate": [
                60,
                80,
                100,
            ],
            "total_usage_records": [
                10,
                20,
                30,
            ],
            "total_support_tickets": [
                2,
                4,
                6,
            ],
            "learning_completion_rate": [
                50,
                75,
                100,
            ],
        }
    )

    result = calculate_performance_metrics(df)

    assert result.loc[
        0,
        "average_onboarding_completion_rate",
    ] == 80

    assert result.loc[
        0,
        "average_tool_usage_records",
    ] == 20

    assert result.loc[
        0,
        "average_support_tickets",
    ] == 4

    assert result.loc[
        0,
        "average_learning_completion_rate",
    ] == 75


def test_correlation_matrix_calculates_relationships():
    df = pd.DataFrame(
        {
            "onboarding_completion_rate": [
                50,
                60,
                70,
                80,
                90,
            ],
            "total_usage_records": [
                10,
                20,
                30,
                40,
                50,
            ],
            "total_support_tickets": [
                5,
                4,
                3,
                2,
                1,
            ],
        }
    )

    result = calculate_correlation_matrix(
        df,
        columns=[
            "onboarding_completion_rate",
            "total_usage_records",
            "total_support_tickets",
        ],
    )

    assert list(result.columns) == [
        "onboarding_completion_rate",
        "total_usage_records",
        "total_support_tickets",
    ]

    assert result.shape == (3, 3)

    assert result.loc[
        "onboarding_completion_rate",
        "total_usage_records",
    ] == pytest.approx(1.0)

    assert result.loc[
        "onboarding_completion_rate",
        "total_support_tickets",
    ] == pytest.approx(-1.0)


def test_correlation_matrix_handles_missing_values():
    df = pd.DataFrame(
        {
            "onboarding_completion_rate": [
                50,
                60,
                np.nan,
                80,
            ],
            "total_usage_records": [
                10,
                20,
                30,
                np.nan,
            ],
        }
    )

    result = calculate_correlation_matrix(
        df,
        columns=[
            "onboarding_completion_rate",
            "total_usage_records",
        ],
    )

    assert result.shape == (2, 2)
    assert not pd.isna(
        result.loc[
            "onboarding_completion_rate",
            "total_usage_records",
        ]
    )


def test_correlation_requires_at_least_two_columns():
    df = pd.DataFrame(
        {
            "onboarding_completion_rate": [
                50,
                60,
                70,
            ]
        }
    )

    with pytest.raises(ValueError):
        calculate_correlation_matrix(
            df,
            columns=["onboarding_completion_rate"],
        )


def test_correlation_pairs_returns_unique_relationships():
    df = pd.DataFrame(
        {
            "onboarding_completion_rate": [
                50,
                60,
                70,
                80,
            ],
            "total_usage_records": [
                10,
                20,
                30,
                40,
            ],
            "total_support_tickets": [
                4,
                3,
                2,
                1,
            ],
        }
    )

    result = calculate_correlation_pairs(
        df,
        columns=[
            "onboarding_completion_rate",
            "total_usage_records",
            "total_support_tickets",
        ],
    )

    assert len(result) == 3

    assert set(result.columns) == {
        "metric_1",
        "metric_2",
        "correlation",
        "relationship",
    }

    assert (
        result["correlation"]
        .between(-1, 1)
        .all()
    )


def test_department_insights_groups_employees():
    df = pd.DataFrame(
        {
            "EmpID": [
                1,
                2,
                3,
                4,
                5,
                6,
            ],
            "Department": [
                "IT/IS",
                "IT/IS",
                "IT/IS",
                "Production",
                "Production",
                "Production",
            ],
            "onboarding_completion_rate": [
                80,
                90,
                70,
                60,
                70,
                80,
            ],
            "total_usage_records": [
                40,
                50,
                60,
                20,
                30,
                40,
            ],
            "total_support_tickets": [
                2,
                3,
                1,
                5,
                4,
                3,
            ],
            "learning_completion_rate": [
                80,
                90,
                70,
                60,
                70,
                80,
            ],
        }
    )

    result = calculate_department_insights(df)

    assert len(result) == 2

    assert set(result["Department"]) == {
        "IT/IS",
        "Production",
    }

    it_row = result[
        result["Department"] == "IT/IS"
    ].iloc[0]

    assert it_row["employee_count"] == 3

    assert it_row[
        "average_onboarding_completion_rate"
    ] == pytest.approx(80)

    assert it_row[
        "average_total_usage_records"
    ] == pytest.approx(50)

    assert it_row[
        "average_total_support_tickets"
    ] == pytest.approx(2)


def test_department_insights_marks_small_departments_low_confidence():
    df = pd.DataFrame(
        {
            "EmpID": [
                1,
                2,
                3,
                4,
                5,
                6,
            ],
            "Department": [
                "Production",
                "Production",
                "Production",
                "Production",
                "Production",
                "Executive Office",
            ],
            "onboarding_completion_rate": [
                70,
                75,
                80,
                85,
                90,
                60,
            ],
        }
    )

    result = calculate_department_insights(df)

    executive_row = result[
        result["Department"] == "Executive Office"
    ].iloc[0]

    production_row = result[
        result["Department"] == "Production"
    ].iloc[0]

    assert executive_row["employee_count"] == 1
    assert executive_row["benchmark_confidence"] == "low"

    assert production_row["employee_count"] == 5
    assert production_row["benchmark_confidence"] == "standard"


def test_department_insights_handles_missing_metrics():
    df = pd.DataFrame(
        {
            "EmpID": [1, 2, 3],
            "Department": [
                "IT/IS",
                "IT/IS",
                "Production",
            ],
            "onboarding_completion_rate": [
                80,
                90,
                70,
            ],
        }
    )

    result = calculate_department_insights(df)

    assert "average_onboarding_completion_rate" in result.columns
    assert "employee_count" in result.columns
    assert len(result) == 2


def test_department_rankings_adds_ranks():
    department_data = pd.DataFrame(
        {
            "Department": [
                "IT/IS",
                "Production",
                "Sales",
            ],
            "employee_count": [
                50,
                209,
                31,
            ],
            "average_onboarding_completion_rate": [
                90,
                70,
                80,
            ],
            "average_learning_completion_rate": [
                95,
                75,
                85,
            ],
            "average_total_support_tickets": [
                2,
                5,
                3,
            ],
            "average_open_support_tickets": [
                1,
                4,
                2,
            ],
        }
    )

    result = calculate_department_rankings(
        department_data
    )

    assert "onboarding_rank" in result.columns
    assert "learning_rank" in result.columns
    assert "support_ticket_rank" in result.columns
    assert "open_ticket_rank" in result.columns

    it_row = result[
        result["Department"] == "IT/IS"
    ].iloc[0]

    assert it_row["onboarding_rank"] == 1
    assert it_row["learning_rank"] == 1
    assert it_row["support_ticket_rank"] == 1
    assert it_row["open_ticket_rank"] == 1


def test_pipeline_reads_dataset_and_returns_results(tmp_path):
    df = pd.DataFrame(
        {
            "EmpID": [1, 2, 3, 4, 5],
            "Department": [
                "IT/IS",
                "IT/IS",
                "Production",
                "Production",
                "Sales",
            ],
            "Salary": [
                50000,
                60000,
                55000,
                65000,
                70000,
            ],
            "onboarding_completion_rate": [
                70,
                80,
                60,
                75,
                90,
            ],
            "total_usage_records": [
                20,
                30,
                15,
                25,
                40,
            ],
            "total_support_tickets": [
                3,
                2,
                5,
                4,
                1,
            ],
            "learning_completion_rate": [
                70,
                80,
                60,
                75,
                90,
            ],
        }
    )

    input_path = tmp_path / "employee_analytics.csv"

    df.to_csv(
        input_path,
        index=False,
    )

    results = run_correlation_department_pipeline(
        input_path
    )

    assert set(results.keys()) == {
        "correlation_matrix",
        "correlation_pairs",
        "department_insights",
        "department_rankings",
    }

    assert not results[
        "correlation_matrix"
    ].empty

    assert not results[
        "correlation_pairs"
    ].empty

    assert not results[
        "department_insights"
    ].empty

    assert not results[
        "department_rankings"
    ].empty


def test_pipeline_can_save_results(tmp_path):
    df = pd.DataFrame(
        {
            "EmpID": [1, 2, 3, 4],
            "Department": [
                "IT/IS",
                "IT/IS",
                "Production",
                "Production",
            ],
            "onboarding_completion_rate": [
                70,
                80,
                60,
                90,
            ],
            "total_usage_records": [
                20,
                30,
                15,
                40,
            ],
            "total_support_tickets": [
                3,
                2,
                5,
                1,
            ],
            "learning_completion_rate": [
                70,
                80,
                60,
                90,
            ],
        }
    )

    input_path = tmp_path / "employee_analytics.csv"
    output_directory = tmp_path / "reports"

    df.to_csv(
        input_path,
        index=False,
    )

    run_correlation_department_pipeline(
        input_path,
        output_directory,
    )

    assert (
        output_directory
        / "correlation_matrix.csv"
    ).exists()

    assert (
        output_directory
        / "correlation_pairs.csv"
    ).exists()

    assert (
        output_directory
        / "department_insights.csv"
    ).exists()

    assert (
        output_directory
        / "department_rankings.csv"
    ).exists()