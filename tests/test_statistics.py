import numpy as np
import pandas as pd
import pytest

from src.analysis.statistics import (
    calculate_descriptive_statistics,
    calculate_distribution_statistics,
    calculate_performance_metrics,
    run_statistical_pipeline,
)


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Create a small employee analytics dataset for testing."""
    return pd.DataFrame(
        {
            "Salary": [50000, 60000, 70000, 80000],
            "Absences": [2, 4, 6, 8],
            "DaysLateLast30": [0, 1, 2, 3],
            "onboarding_completion_rate": [
                50.0,
                75.0,
                80.0,
                95.0,
            ],
            "total_usage_records": [
                40,
                45,
                50,
                55,
            ],
            "total_support_tickets": [
                2,
                3,
                4,
                5,
            ],
            "open_support_tickets": [
                1,
                1,
                2,
                2,
            ],
            "learning_completion_rate": [
                60.0,
                70.0,
                80.0,
                90.0,
            ],
            "average_assessment_score": [
                70.0,
                80.0,
                85.0,
                90.0,
            ],
            "average_resolution_time_hours": [
                10.0,
                15.0,
                20.0,
                25.0,
            ],
        }
    )


def test_calculate_descriptive_statistics(sample_dataframe):
    """Descriptive statistics should use the expected NumPy calculations."""
    result = calculate_descriptive_statistics(
        sample_dataframe,
        columns=["Salary"],
    )

    row = result.iloc[0]

    assert row["metric"] == "Salary"
    assert row["count"] == 4
    assert row["mean"] == pytest.approx(65000.0)
    assert row["median"] == pytest.approx(65000.0)
    assert row["min"] == pytest.approx(50000.0)
    assert row["q25"] == pytest.approx(57500.0)
    assert row["q50"] == pytest.approx(65000.0)
    assert row["q75"] == pytest.approx(72500.0)
    assert row["max"] == pytest.approx(80000.0)


def test_descriptive_statistics_standard_deviation(sample_dataframe):
    """Standard deviation should match NumPy sample standard deviation."""
    result = calculate_descriptive_statistics(
        sample_dataframe,
        columns=["Absences"],
    )

    expected = np.std(
        sample_dataframe["Absences"].to_numpy(),
        ddof=1,
    )

    assert result.iloc[0]["std"] == pytest.approx(expected)


def test_distribution_statistics(sample_dataframe):
    """Distribution analysis should calculate IQR and range."""
    result = calculate_distribution_statistics(
        sample_dataframe,
        columns=["Salary"],
    )

    row = result.iloc[0]

    assert row["q25"] == pytest.approx(57500.0)
    assert row["median"] == pytest.approx(65000.0)
    assert row["q75"] == pytest.approx(72500.0)
    assert row["iqr"] == pytest.approx(15000.0)
    assert row["range"] == pytest.approx(30000.0)


def test_distribution_statistics_identifies_spread(sample_dataframe):
    """Distribution statistics should include standard deviation."""
    result = calculate_distribution_statistics(
        sample_dataframe,
        columns=["Absences"],
    )

    expected = np.std(
        sample_dataframe["Absences"].to_numpy(),
        ddof=1,
    )

    assert result.iloc[0]["std"] == pytest.approx(expected)


def test_performance_metrics(sample_dataframe):
    """Performance metrics should calculate project-level averages."""
    result = calculate_performance_metrics(
        sample_dataframe,
    )

    row = result.iloc[0]

    assert row["average_onboarding_completion_rate"] == pytest.approx(
        75.0
    )

    assert row["average_tool_usage_records"] == pytest.approx(
        47.5
    )

    assert row["average_support_tickets"] == pytest.approx(
        3.5
    )

    assert row["average_open_support_tickets"] == pytest.approx(
        1.5
    )

    assert row["average_learning_completion_rate"] == pytest.approx(
        75.0
    )


def test_missing_values_are_ignored(sample_dataframe):
    """Missing statistical values should not become zeros."""
    df = sample_dataframe.copy()

    df.loc[1, "Salary"] = np.nan

    result = calculate_descriptive_statistics(
        df,
        columns=["Salary"],
    )

    row = result.iloc[0]

    assert row["count"] == 3
    assert row["mean"] == pytest.approx(66666.66666666667)
    assert row["min"] == pytest.approx(50000.0)
    assert row["max"] == pytest.approx(80000.0)


def test_missing_performance_values_are_ignored(sample_dataframe):
    """Performance calculations should ignore missing values."""
    df = sample_dataframe.copy()

    df.loc[0, "onboarding_completion_rate"] = np.nan

    result = calculate_performance_metrics(df)

    expected = np.mean(
        [75.0, 80.0, 95.0]
    )

    assert result.iloc[0][
        "average_onboarding_completion_rate"
    ] == pytest.approx(expected)


def test_invalid_column_raises_error(sample_dataframe):
    """An unknown column should raise a clear error."""
    with pytest.raises(KeyError):
        calculate_descriptive_statistics(
            sample_dataframe,
            columns=["does_not_exist"],
        )


def test_empty_dataframe_raises_error():
    """Statistical analysis should reject an empty dataframe."""
    df = pd.DataFrame()

    with pytest.raises(ValueError):
        calculate_descriptive_statistics(df)


def test_pipeline_reads_dataset_and_returns_results(
    sample_dataframe,
    tmp_path,
):
    """The complete pipeline should load data and return all analysis outputs."""
    input_path = tmp_path / "employee_analytics.csv"

    sample_dataframe.to_csv(
        input_path,
        index=False,
    )

    results = run_statistical_pipeline(input_path)

    assert "descriptive_statistics" in results
    assert "distribution_statistics" in results
    assert "performance_metrics" in results

    assert not results["descriptive_statistics"].empty
    assert not results["distribution_statistics"].empty
    assert not results["performance_metrics"].empty


def test_pipeline_can_save_results(
    sample_dataframe,
    tmp_path,
):
    """The pipeline should optionally save analysis results as CSV files."""
    input_path = tmp_path / "employee_analytics.csv"
    output_directory = tmp_path / "analysis_results"

    sample_dataframe.to_csv(
        input_path,
        index=False,
    )

    run_statistical_pipeline(
        input_path,
        output_directory,
    )

    assert (
        output_directory
        / "descriptive_statistics.csv"
    ).exists()

    assert (
        output_directory
        / "distribution_statistics.csv"
    ).exists()

    assert (
        output_directory
        / "performance_metrics.csv"
    ).exists()