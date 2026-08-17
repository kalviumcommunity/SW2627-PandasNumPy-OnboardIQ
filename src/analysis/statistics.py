from pathlib import Path

import numpy as np
import pandas as pd


# Numeric columns available in the employee-level analytics dataset.
STATISTICAL_COLUMNS = [
    "Salary",
    "Absences",
    "DaysLateLast30",
    "SpecialProjectsCount",
    "average_completion_percentage",
    "total_onboarding_tasks",
    "completed_onboarding_tasks",
    "late_onboarding_tasks",
    "onboarding_completion_rate",
    "total_usage_records",
    "average_daily_active_usage",
    "total_slack_activity",
    "total_jira_usage",
    "total_github_activity",
    "total_teams_activity",
    "total_workspace_activity",
    "total_support_tickets",
    "average_resolution_time_hours",
    "open_support_tickets",
    "total_learning_records",
    "completed_courses",
    "average_assessment_score",
    "average_completion_time_hours",
    "learning_completion_rate",
]


# Metrics specifically relevant to Issue #15 correlation analysis.
CORRELATION_COLUMNS = [
    "onboarding_completion_rate",
    "total_usage_records",
    "average_daily_active_usage",
    "total_slack_activity",
    "total_jira_usage",
    "total_github_activity",
    "total_teams_activity",
    "total_workspace_activity",
    "total_support_tickets",
    "average_resolution_time_hours",
    "open_support_tickets",
    "total_learning_records",
    "completed_courses",
    "average_assessment_score",
    "learning_completion_rate",
    "Absences",
    "DaysLateLast30",
]


# Metrics used for department-level benchmarking.
DEPARTMENT_METRICS = [
    "onboarding_completion_rate",
    "completed_onboarding_tasks",
    "total_usage_records",
    "average_daily_active_usage",
    "total_support_tickets",
    "open_support_tickets",
    "average_resolution_time_hours",
    "learning_completion_rate",
    "average_assessment_score",
    "Absences",
    "DaysLateLast30",
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

    Missing values are excluded from calculations.
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
                "std": (
                    float(np.std(values, ddof=1))
                    if values.size > 1
                    else 0.0
                ),
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

    Returns:
    - minimum
    - lower quartile
    - median
    - upper quartile
    - maximum
    - interquartile range
    - range
    - standard deviation
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
                "std": (
                    float(np.std(values, ddof=1))
                    if values.size > 1
                    else 0.0
                ),
            }
        )

    return pd.DataFrame(results)


def calculate_performance_metrics(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate overall employee onboarding performance metrics.

    Calculations use NumPy vectorized operations.
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


def calculate_correlation_matrix(
    df: pd.DataFrame,
    columns: list[str] | None = None,
) -> pd.DataFrame:
    """
    Calculate Pearson correlation coefficients between
    employee-level onboarding, tool-usage, support, and
    learning metrics.

    Missing values are handled using pairwise complete
    observations.

    Returns:
        A square DataFrame containing Pearson correlation
        coefficients.
    """
    if columns is None:
        columns = [
            column
            for column in CORRELATION_COLUMNS
            if column in df.columns
        ]

    if len(columns) < 2:
        raise ValueError(
            "At least two valid columns are required for correlation analysis."
        )

    numeric_df = pd.DataFrame(index=df.index)

    for column in columns:
        numeric_df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    correlation = numeric_df.corr(method="pearson")

    return correlation


def calculate_correlation_pairs(
    df: pd.DataFrame,
    columns: list[str] | None = None,
) -> pd.DataFrame:
    """
    Convert the correlation matrix into a long-form table.

    Only unique metric pairs are returned.

    Returns:
        DataFrame containing:
        - metric_1
        - metric_2
        - correlation
        - relationship
    """
    matrix = calculate_correlation_matrix(
        df,
        columns=columns,
    )

    results = []

    for index, metric_1 in enumerate(matrix.columns):
        for metric_2 in matrix.columns[index + 1:]:
            correlation = matrix.loc[
                metric_1,
                metric_2,
            ]

            if pd.isna(correlation):
                relationship = "undefined"
            elif correlation >= 0.7:
                relationship = "strong_positive"
            elif correlation >= 0.3:
                relationship = "moderate_positive"
            elif correlation > -0.3:
                relationship = "weak_or_none"
            elif correlation > -0.7:
                relationship = "moderate_negative"
            else:
                relationship = "strong_negative"

            results.append(
                {
                    "metric_1": metric_1,
                    "metric_2": metric_2,
                    "correlation": float(correlation)
                    if not pd.isna(correlation)
                    else np.nan,
                    "relationship": relationship,
                }
            )

    return pd.DataFrame(results)


def calculate_department_insights(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate department-level aggregated insights.

    Each department receives:
    - employee count
    - onboarding metrics
    - tool-usage metrics
    - support metrics
    - learning metrics
    - attendance indicators
    - benchmark confidence

    Departments with fewer than five employees are marked
    as low-confidence for benchmarking.
    """
    if "Department" not in df.columns:
        raise KeyError(
            "Column 'Department' does not exist."
        )

    if df.empty:
        raise ValueError(
            "Cannot calculate department insights from an empty DataFrame."
        )

    available_metrics = [
        column
        for column in DEPARTMENT_METRICS
        if column in df.columns
    ]

    if not available_metrics:
        raise ValueError(
            "No valid department metrics were found."
        )

    working_df = df.copy()

    for column in available_metrics:
        working_df[column] = pd.to_numeric(
            working_df[column],
            errors="coerce",
        )

    department_metrics = (
        working_df
        .groupby("Department", dropna=False)
        .agg(
            employee_count=("EmpID", "nunique")
            if "EmpID" in working_df.columns
            else ("Department", "size"),
            **{
                f"average_{column}": (column, "mean")
                for column in available_metrics
            },
        )
        .reset_index()
    )

    department_metrics["benchmark_confidence"] = np.where(
        department_metrics["employee_count"] < 5,
        "low",
        "standard",
    )

    return department_metrics


def calculate_department_rankings(
    department_insights: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add relative rankings for key department metrics.

    Higher onboarding and learning completion rates rank first.
    Lower support and absence metrics rank first.
    """
    required_columns = {
        "Department",
        "employee_count",
    }

    missing = required_columns - set(
        department_insights.columns
    )

    if missing:
        raise KeyError(
            f"Missing required department columns: {sorted(missing)}"
        )

    result = department_insights.copy()

    ranking_columns = {
        "average_onboarding_completion_rate": "onboarding_rank",
        "average_learning_completion_rate": "learning_rank",
        "average_total_support_tickets": "support_ticket_rank",
        "average_open_support_tickets": "open_ticket_rank",
    }

    for metric, rank_column in ranking_columns.items():
        if metric not in result.columns:
            continue

        ascending = metric in {
            "average_total_support_tickets",
            "average_open_support_tickets",
        }

        result[rank_column] = (
            result[metric]
            .rank(
                ascending=ascending,
                method="min",
            )
            .astype("Int64")
        )

    return result


def run_statistical_pipeline(
    input_path: str | Path,
    output_directory: str | Path | None = None,
) -> dict[str, pd.DataFrame]:
    """
    Run the complete Issue #14 statistical analysis pipeline.

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
        raise ValueError(
            "Input dataset contains no rows."
        )

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


def run_correlation_department_pipeline(
    input_path: str | Path,
    output_directory: str | Path | None = None,
) -> dict[str, pd.DataFrame]:
    """
    Run the Issue #15 correlation and department-level
    analysis pipeline.

    Steps:
    1. Load employee-level analytics data.
    2. Calculate correlation matrix.
    3. Calculate correlation-pair relationships.
    4. Calculate department-level aggregated insights.
    5. Calculate department rankings.
    6. Optionally save results as CSV files.

    Correlation indicates statistical association and must
    not be interpreted as causation.
    """
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {input_path}"
        )

    df = pd.read_csv(input_path)

    if df.empty:
        raise ValueError(
            "Input dataset contains no rows."
        )

    correlation_matrix = calculate_correlation_matrix(df)

    correlation_pairs = calculate_correlation_pairs(df)

    department_insights = calculate_department_insights(df)

    department_rankings = calculate_department_rankings(
        department_insights
    )

    results = {
        "correlation_matrix": correlation_matrix,
        "correlation_pairs": correlation_pairs,
        "department_insights": department_insights,
        "department_rankings": department_rankings,
    }

    if output_directory is not None:
        output_directory = Path(output_directory)
        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        correlation_matrix.to_csv(
            output_directory / "correlation_matrix.csv"
        )

        correlation_pairs.to_csv(
            output_directory / "correlation_pairs.csv",
            index=False,
        )

        department_insights.to_csv(
            output_directory / "department_insights.csv",
            index=False,
        )

        department_rankings.to_csv(
            output_directory / "department_rankings.csv",
            index=False,
        )

    return results