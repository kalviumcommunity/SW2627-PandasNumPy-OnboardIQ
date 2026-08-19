from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_FUNNEL_STAGES = [
    "employees",
    "onboarding_started",
    "onboarding_50_percent",
    "onboarding_75_percent",
    "onboarding_completed",
    "learning_completed",
    "tool_adopted",
]


def _numeric_series(
    df: pd.DataFrame,
    column: str,
) -> pd.Series:
    """Return a numeric series with invalid values converted to NaN."""

    if column not in df.columns:
        raise KeyError(f"Column '{column}' does not exist.")

    return pd.to_numeric(
        df[column],
        errors="coerce",
    )


def calculate_funnel_analysis(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate employee onboarding funnel stages.

    Funnel stages:

    1. Employees
    2. Onboarding started
    3. At least 50% onboarding completion
    4. At least 75% onboarding completion
    5. Onboarding completed
    6. Learning completed
    7. Tool adopted

    Returns:
        DataFrame containing stage counts, conversion rates,
        and drop-off rates.
    """

    if df.empty:
        raise ValueError("Cannot calculate funnel analysis on empty data.")

    required_columns = [
        "onboarding_completion_rate",
        "learning_completion_rate",
        "total_usage_records",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise KeyError(
            "Missing required funnel columns: "
            + ", ".join(missing_columns)
        )

    onboarding = _numeric_series(
        df,
        "onboarding_completion_rate",
    )

    learning = _numeric_series(
        df,
        "learning_completion_rate",
    )

    usage = _numeric_series(
        df,
        "total_usage_records",
    )

    total_employees = len(df)

    onboarding_started = onboarding.notna().sum()

    onboarding_50 = (
        onboarding.ge(50)
        .fillna(False)
        .sum()
    )

    onboarding_75 = (
        onboarding.ge(75)
        .fillna(False)
        .sum()
    )

    onboarding_completed = (
        onboarding.ge(100)
        .fillna(False)
        .sum()
    )

    learning_completed = (
        learning.ge(100)
        .fillna(False)
        .sum()
    )

    tool_adopted = (
        usage.gt(0)
        .fillna(False)
        .sum()
    )

    stage_counts = [
        total_employees,
        onboarding_started,
        onboarding_50,
        onboarding_75,
        onboarding_completed,
        learning_completed,
        tool_adopted,
    ]

    stage_names = [
        "employees",
        "onboarding_started",
        "onboarding_50_percent",
        "onboarding_75_percent",
        "onboarding_completed",
        "learning_completed",
        "tool_adopted",
    ]

    results = []

    previous_count = None

    for stage, count in zip(
        stage_names,
        stage_counts,
    ):
        count = int(count)

        if total_employees:
            overall_conversion = (
                count / total_employees
            ) * 100
        else:
            overall_conversion = np.nan

        if previous_count is None:
            stage_conversion = 100.0
            drop_off = 0.0
        elif previous_count > 0:
            stage_conversion = (
                count / previous_count
            ) * 100

            drop_off = (
                (previous_count - count)
                / previous_count
            ) * 100
        else:
            stage_conversion = np.nan
            drop_off = np.nan

        results.append(
            {
                "stage": stage,
                "employee_count": count,
                "overall_conversion_rate": overall_conversion,
                "stage_conversion_rate": stage_conversion,
                "drop_off_rate": drop_off,
            }
        )

        previous_count = count

    return pd.DataFrame(results)


def identify_funnel_dropoffs(
    funnel_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Identify funnel stages with meaningful employee drop-off.

    Args:
        funnel_data: Output from calculate_funnel_analysis().

    Returns:
        Funnel rows sorted by drop-off rate descending.
    """

    required_columns = {
        "stage",
        "employee_count",
        "drop_off_rate",
    }

    missing = required_columns.difference(
        funnel_data.columns
    )

    if missing:
        raise KeyError(
            "Missing funnel columns: "
            + ", ".join(sorted(missing))
        )

    result = funnel_data.copy()

    result["drop_off_rate"] = pd.to_numeric(
        result["drop_off_rate"],
        errors="coerce",
    )

    result["drop_off_flag"] = np.where(
        result["drop_off_rate"] >= 20,
        "high",
        np.where(
            result["drop_off_rate"] >= 10,
            "moderate",
            "low",
        ),
    )

    return result.sort_values(
        "drop_off_rate",
        ascending=False,
    ).reset_index(drop=True)


def run_funnel_pipeline(
    input_path: str | Path,
    output_directory: str | Path | None = None,
) -> dict[str, pd.DataFrame]:
    """
    Load the employee analytics dataset and run funnel analysis.

    Optionally saves funnel results as CSV files.
    """

    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {input_path}"
        )

    df = pd.read_csv(input_path)

    funnel = calculate_funnel_analysis(df)

    dropoffs = identify_funnel_dropoffs(funnel)

    results = {
        "funnel_analysis": funnel,
        "funnel_dropoffs": dropoffs,
    }

    if output_directory is not None:
        output_directory = Path(output_directory)
        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        funnel.to_csv(
            output_directory / "funnel_analysis.csv",
            index=False,
        )

        dropoffs.to_csv(
            output_directory / "funnel_dropoffs.csv",
            index=False,
        )

    return results