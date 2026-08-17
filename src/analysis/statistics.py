from pathlib import Path

import numpy as np
import pandas as pd


# Columns from the employee-level analytics dataset that are
# appropriate for statistical analysis.
STATISTICAL_COLUMNS = [
    "Salary",
    "Absences",
    "DaysLateLast30",
    "SpecialProjectsCount",
    "completion_percentage",
    "total_onboarding_tasks",
    "completed_onboarding_tasks",
    "late_onboarding_tasks",
    "onboarding_completion_rate",
    "total_usage_records",
    "total_slack_activity",
    "total_jira_activity",
    "total_github_activity",
    "total_teams_activity",
    "total_workspace_activity",
    "total_support_tickets",
    "average_resolution_time_hours",
    "open_support_tickets",
    "total_learning_records",
    "average_assessment_score",
    "average_completion_time_hours",
    "learning_completion_rate",
]


def _numeric_values(
    df: pd.DataFrame,
    column: str,
) -> np.ndarray:
    """
    Return a column as a NumPy numeric array with missing values removed.

    Raises:
        KeyError: If the requested column does not exist.
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' does not exist.")

    values = pd.to_numeric(df[column], errors="coerce").dropna()

    return values.to_numpy(dtype=float)


def calculate_descriptive_statistics(
    df: pd.DataFrame,
    columns: list[str] | None = None,
) -> pd.DataFrame:
    """
    Calculate descriptive statistics using NumPy vectorized operations.

    Statistics returned:
    - count
    - mean
    - median
    - standard deviation
    - minimum
    - 25th percentile
    - 50th percentile
    - 75th percentile
    - maximum

    Missing values are excluded from the calculations.

    Returns:
        DataFrame containing one row per analyzed column.
    """
    if columns is None:
        columns = [
            column
            for column in STATISTICAL_COLUMNS
            if column in df.columns
        ]

    if not columns:
        raise ValueError("No valid statistical columns were found.")

    results = []

    for column in columns:
        values = _numeric_values(df, column)

        if values.size == 0:
            results.append(
                {
                    "metric": column,
                    "count": 0,
                    "mean": np.nan,
                    "median": np.nan,
                    "std": np.nan,
                    "min": np.nan,
                    "q25": np.nan,
                    "q50": np.nan,
                    "q75": np.nan,
                    "max": np.nan,
                }
            )
            continue

        quartiles = np.percentile(
            values,
            [25, 50, 75],
        )

        results.append(
            {
                "metric": column,
                "count": int(values.size),
                "mean": float(np.mean(values)),
                "median": float(np.median(values)),
                "std": float(np.std(values, ddof=1))
                if values.size > 1
                else 0.0,
                "min": float(np.min(values)),
                "q25": float(quartiles[0]),
                "q50": float(quartiles[1]),
                "q75": float(quartiles[2]),
                "max": float(np.max(values)),
            }
        )

    return pd.DataFrame(results)


def calculate_distribution_statistics(
    df: pd.DataFrame,
    columns: list[str] | None = None,
) -> pd.DataFrame:
    """
    Calculate distribution-focused statistics using NumPy.

    The output focuses on:
    - minimum
    - lower quartile
    - median
    - upper quartile
    - maximum
    - interquartile range
    - range
    - standard deviation

    These statistics help identify the spread and distribution
    of onboarding, productivity, support, and learning metrics.
    """
    if columns is None:
        columns = [
            column
            for column in STATISTICAL_COLUMNS
            if column in df.columns
        ]

    if not columns:
        raise ValueError("No valid distribution columns were found.")

    results = []

    for column in columns:
        values = _numeric_values(df, column)

        if values.size == 0:
            results.append(
                {
                    "metric": column,
                    "min": np.nan,
                    "q25": np.nan,
                    "median": np.nan,
                    "q75": np.nan,
                    "max": np.nan,
                    "iqr": np.nan,
                    "range": np.nan,
                    "std": np.nan,
                }
            )
            continue

        q25, median, q75 = np.percentile(
            values,
            [25, 50, 75],
        )

        results.append(
            {
                "metric": column,
                "min": float(np.min(values)),
                "q25": float(q25),
                "median": float(median),
                "q75": float(q75),
                "max": float(np.max(values)),
                "iqr": float(q75 - q25),
                "range": float(np.max(values) - np.min(values)),
                "std": float(np.std(values, ddof=1))
                if values.size > 1
                else 0.0,
            }
        )

    return pd.DataFrame(results)


def calculate_performance_metrics(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate employee onboarding performance metrics.

    The calculations use NumPy vectorized operations rather than
    row-by-row Python loops.

    Returns:
        One-row DataFrame containing overall performance metrics.
    """
    metrics = {}

    if "onboarding_completion_rate" in df.columns:
        values = _numeric_values(
            df,
            "onboarding_completion_rate",
        )
        if values.size:
            metrics["average_onboarding_completion_rate"] = float(
                np.mean(values)
            )
            metrics["median_onboarding_completion_rate"] = float(
                np.median(values)
            )

    if "total_usage_records" in df.columns:
        values = _numeric_values(
            df,
            "total_usage_records",
        )
        if values.size:
            metrics["average_tool_usage_records"] = float(
                np.mean(values)
            )

    if "total_support_tickets" in df.columns:
        values = _numeric_values(
            df,
            "total_support_tickets",
        )
        if values.size:
            metrics["average_support_tickets"] = float(
                np.mean(values)
            )

    if "open_support_tickets" in df.columns:
        values = _numeric_values(
            df,
            "open_support_tickets",
        )
        if values.size:
            metrics["average_open_support_tickets"] = float(
                np.mean(values)
            )

    if "learning_completion_rate" in df.columns:
        values = _numeric_values(
            df,
            "learning_completion_rate",
        )
        if values.size:
            metrics["average_learning_completion_rate"] = float(
                np.mean(values)
            )

    if "average_assessment_score" in df.columns:
        values = _numeric_values(
            df,
            "average_assessment_score",
        )
        if values.size:
            metrics["average_assessment_score"] = float(
                np.mean(values)
            )

    if "average_resolution_time_hours" in df.columns:
        values = _numeric_values(
            df,
            "average_resolution_time_hours",
        )
        if values.size:
            metrics["average_resolution_time_hours"] = float(
                np.mean(values)
            )

    if "Absences" in df.columns:
        values = _numeric_values(df, "Absences")
        if values.size:
            metrics["average_absences"] = float(
                np.mean(values)
            )

    if "DaysLateLast30" in df.columns:
        values = _numeric_values(
            df,
            "DaysLateLast30",
        )
        if values.size:
            metrics["average_days_late_last_30"] = float(
                np.mean(values)
            )

    if not metrics:
        raise ValueError(
            "No supported performance columns were found."
        )

    return pd.DataFrame([metrics])


def run_statistical_pipeline(
    input_path: str | Path,
    output_directory: str | Path | None = None,
) -> dict[str, pd.DataFrame]:
    """
    Run the complete NumPy-based statistical analysis pipeline.

    Steps:
    1. Load the employee-level analytics dataset.
    2. Calculate descriptive statistics.
    3. Calculate distribution statistics.
    4. Calculate onboarding/performance metrics.
    5. Optionally save the results as CSV files.

    Args:
        input_path: Path to the merged employee analytics CSV.
        output_directory: Optional directory for generated reports.

    Returns:
        Dictionary containing:
        - descriptive_statistics
        - distribution_statistics
        - performance_metrics
    """
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {input_path}"
        )

    df = pd.read_csv(input_path)

    if df.empty:
        raise ValueError("Input dataset contains no rows.")

    descriptive_statistics = calculate_descriptive_statistics(df)

    distribution_statistics = calculate_distribution_statistics(df)

    performance_metrics = calculate_performance_metrics(df)

    results = {
        "descriptive_statistics": descriptive_statistics,
        "distribution_statistics": distribution_statistics,
        "performance_metrics": performance_metrics,
    }

    if output_directory is not None:
        output_directory = Path(output_directory)
        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        descriptive_statistics.to_csv(
            output_directory / "descriptive_statistics.csv",
            index=False,
        )

        distribution_statistics.to_csv(
            output_directory / "distribution_statistics.csv",
            index=False,
        )

        performance_metrics.to_csv(
            output_directory / "performance_metrics.csv",
            index=False,
        )

    return results