from pathlib import Path

import numpy as np
import pandas as pd


TREND_COLUMNS = [
    "onboarding_completion_rate",
    "learning_completion_rate",
    "average_assessment_score",
    "total_usage_records",
    "total_support_tickets",
    "open_support_tickets",
]


SEGMENT_SCORE_COLUMNS = [
    "onboarding_completion_rate",
    "learning_completion_rate",
    "average_assessment_score",
    "total_usage_records",
]


def _numeric_series(
    df: pd.DataFrame,
    column: str,
) -> pd.Series:
    """
    Return a numeric version of a dataframe column.

    Missing or non-numeric values are converted to NaN.
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' does not exist.")

    return pd.to_numeric(df[column], errors="coerce")


def prepare_hire_date(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert DateofHire into a datetime column.

    Returns a copy so the original dataframe is not modified.
    """
    if "DateofHire" not in df.columns:
        raise KeyError("Column 'DateofHire' does not exist.")

    result = df.copy()

    result["DateofHire"] = pd.to_datetime(
        result["DateofHire"],
        errors="coerce",
    )

    return result


def calculate_monthly_onboarding_trend(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate monthly onboarding trends based on employee hire date.

    The result contains:
    - hire_month
    - employee_count
    - average_onboarding_completion_rate
    - average_learning_completion_rate
    - average_assessment_score
    """
    required_columns = [
        "DateofHire",
        "onboarding_completion_rate",
        "learning_completion_rate",
        "average_assessment_score",
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise KeyError(
            f"Missing required columns: {', '.join(missing)}"
        )

    result = prepare_hire_date(df)

    result["hire_month"] = (
        result["DateofHire"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    result["onboarding_completion_rate"] = pd.to_numeric(
        result["onboarding_completion_rate"],
        errors="coerce",
    )

    result["learning_completion_rate"] = pd.to_numeric(
        result["learning_completion_rate"],
        errors="coerce",
    )

    result["average_assessment_score"] = pd.to_numeric(
        result["average_assessment_score"],
        errors="coerce",
    )

    trend = (
        result.dropna(subset=["hire_month"])
        .groupby("hire_month")
        .agg(
            employee_count=("EmpID", "nunique"),
            average_onboarding_completion_rate=(
                "onboarding_completion_rate",
                "mean",
            ),
            average_learning_completion_rate=(
                "learning_completion_rate",
                "mean",
            ),
            average_assessment_score=(
                "average_assessment_score",
                "mean",
            ),
        )
        .reset_index()
        .sort_values("hire_month")
    )

    return trend.reset_index(drop=True)


def add_rolling_metrics(
    trend_df: pd.DataFrame,
    window: int = 3,
) -> pd.DataFrame:
    """
    Add rolling averages to a monthly trend dataframe.

    A three-month rolling window is used by default.
    """
    if window < 1:
        raise ValueError("Rolling window must be at least 1.")

    required_columns = [
        "hire_month",
        "average_onboarding_completion_rate",
        "average_learning_completion_rate",
        "average_assessment_score",
    ]

    missing = [
        column
        for column in required_columns
        if column not in trend_df.columns
    ]

    if missing:
        raise KeyError(
            f"Missing required columns: {', '.join(missing)}"
        )

    result = trend_df.copy()

    result = result.sort_values("hire_month").reset_index(drop=True)

    result["rolling_onboarding_completion_rate"] = (
        result["average_onboarding_completion_rate"]
        .rolling(window=window, min_periods=1)
        .mean()
    )

    result["rolling_learning_completion_rate"] = (
        result["average_learning_completion_rate"]
        .rolling(window=window, min_periods=1)
        .mean()
    )

    result["rolling_assessment_score"] = (
        result["average_assessment_score"]
        .rolling(window=window, min_periods=1)
        .mean()
    )

    return result


def calculate_trend_change(
    trend_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate month-to-month change in onboarding completion.

    The first month has no previous month, so its change is NaN.
    """
    if "average_onboarding_completion_rate" not in trend_df.columns:
        raise KeyError(
            "Column 'average_onboarding_completion_rate' does not exist."
        )

    result = trend_df.copy()

    result["onboarding_completion_change"] = (
        result["average_onboarding_completion_rate"]
        .diff()
    )

    return result


def calculate_employee_productivity_scores(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create a normalized productivity score for each employee.

    The score combines:
    - onboarding completion
    - learning completion
    - assessment score
    - tool usage

    Each metric is normalized using min-max normalization.

    The final productivity score ranges from 0 to 100.
    """
    required_columns = [
        "EmpID",
        *SEGMENT_SCORE_COLUMNS,
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise KeyError(
            f"Missing required columns: {', '.join(missing)}"
        )

    result = df[
        required_columns
    ].copy()

    for column in SEGMENT_SCORE_COLUMNS:
        result[column] = pd.to_numeric(
            result[column],
            errors="coerce",
        )

    normalized_columns = []

    for column in SEGMENT_SCORE_COLUMNS:
        minimum = result[column].min()
        maximum = result[column].max()

        normalized_column = f"{column}_normalized"

        if pd.isna(minimum) or pd.isna(maximum):
            result[normalized_column] = np.nan

        elif maximum == minimum:
            result[normalized_column] = 1.0

        else:
            result[normalized_column] = (
                result[column] - minimum
            ) / (maximum - minimum)

        normalized_columns.append(normalized_column)

    result["productivity_score"] = (
        result[normalized_columns]
        .mean(axis=1, skipna=True)
        * 100
    )

    return result[
        [
            "EmpID",
            *SEGMENT_SCORE_COLUMNS,
            "productivity_score",
        ]
    ]


def assign_productivity_segments(
    scored_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Assign employees to productivity segments.

    Segments:
    - High Productivity: score >= 75
    - Medium Productivity: score >= 50 and < 75
    - Low Productivity: score < 50
    """
    if "productivity_score" not in scored_df.columns:
        raise KeyError(
            "Column 'productivity_score' does not exist."
        )

    result = scored_df.copy()

    result["productivity_segment"] = pd.cut(
        result["productivity_score"],
        bins=[-np.inf, 50, 75, np.inf],
        labels=[
            "Low Productivity",
            "Medium Productivity",
            "High Productivity",
        ],
        right=False,
    )

    return result


def calculate_segment_summary(
    segmented_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Summarize employee productivity segments.
    """
    required_columns = [
        "productivity_segment",
        "productivity_score",
    ]

    missing = [
        column
        for column in required_columns
        if column not in segmented_df.columns
    ]

    if missing:
        raise KeyError(
            f"Missing required columns: {', '.join(missing)}"
        )

    result = (
        segmented_df
        .groupby(
            "productivity_segment",
            observed=False,
        )
        .agg(
            employee_count=("productivity_score", "count"),
            average_productivity_score=(
                "productivity_score",
                "mean",
            ),
        )
        .reset_index()
    )

    total_employees = result["employee_count"].sum()

    if total_employees:
        result["employee_percentage"] = (
            result["employee_count"]
            / total_employees
            * 100
        )
    else:
        result["employee_percentage"] = np.nan

    return result


def calculate_department_productivity(
    segmented_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate productivity metrics by department.
    """
    required_columns = [
        "Department",
        "productivity_score",
    ]

    missing = [
        column
        for column in required_columns
        if column not in segmented_df.columns
    ]

    if missing:
        raise KeyError(
            f"Missing required columns: {', '.join(missing)}"
        )

    result = (
        segmented_df
        .groupby("Department")
        .agg(
            employee_count=(
                "productivity_score",
                "count",
            ),
            average_productivity_score=(
                "productivity_score",
                "mean",
            ),
        )
        .reset_index()
        .sort_values(
            "average_productivity_score",
            ascending=False,
        )
    )

    return result.reset_index(drop=True)


def run_trend_segmentation_pipeline(
    input_path: str | Path,
    output_directory: str | Path | None = None,
) -> dict[str, pd.DataFrame]:
    """
    Run the complete trend-analysis and segmentation pipeline.

    Returns:
        Dictionary containing:
        - monthly_trends
        - productivity_scores
        - productivity_segments
        - segment_summary
        - department_productivity
    """
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file does not exist: {input_path}"
        )

    df = pd.read_csv(input_path)

    monthly_trends = calculate_monthly_onboarding_trend(df)

    monthly_trends = add_rolling_metrics(
        monthly_trends,
        window=3,
    )

    monthly_trends = calculate_trend_change(
        monthly_trends,
    )

    productivity_scores = calculate_employee_productivity_scores(
        df
    )

    productivity_segments = assign_productivity_segments(
        productivity_scores
    )

    if "Department" in df.columns:
        productivity_segments = productivity_segments.merge(
            df[["EmpID", "Department"]],
            on="EmpID",
            how="left",
        )

    segment_summary = calculate_segment_summary(
        productivity_segments
    )

    if "Department" in productivity_segments.columns:
        department_productivity = calculate_department_productivity(
            productivity_segments
        )
    else:
        department_productivity = pd.DataFrame()

    results = {
        "monthly_trends": monthly_trends,
        "productivity_scores": productivity_scores,
        "productivity_segments": productivity_segments,
        "segment_summary": segment_summary,
        "department_productivity": department_productivity,
    }

    if output_directory is not None:
        output_directory = Path(output_directory)
        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        for name, result in results.items():
            result.to_csv(
                output_directory / f"{name}.csv",
                index=False,
            )

    return results