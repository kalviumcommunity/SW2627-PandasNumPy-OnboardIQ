from pathlib import Path

import numpy as np
import pandas as pd


def _numeric_series(
    df: pd.DataFrame,
    column: str,
) -> pd.Series:
    """Return a numeric dataframe column."""

    if column not in df.columns:
        raise KeyError(f"Column '{column}' does not exist.")

    return pd.to_numeric(
        df[column],
        errors="coerce",
    )


def calculate_kpis(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate business KPIs for employee onboarding.

    The KPIs cover:
    - onboarding completion
    - learning completion
    - tool adoption
    - support burden
    - open support tickets
    - assessment performance
    - support resolution time
    - productivity readiness

    Returns:
        One-row DataFrame containing the calculated KPIs.
    """

    if df.empty:
        raise ValueError(
            "Cannot calculate KPIs on an empty dataframe."
        )

    required_columns = [
        "onboarding_completion_rate",
        "learning_completion_rate",
        "total_usage_records",
        "total_support_tickets",
        "open_support_tickets",
        "average_assessment_score",
        "average_resolution_time_hours",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise KeyError(
            "Missing required KPI columns: "
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

    support = _numeric_series(
        df,
        "total_support_tickets",
    )

    open_support = _numeric_series(
        df,
        "open_support_tickets",
    )

    assessment = _numeric_series(
        df,
        "average_assessment_score",
    )

    resolution = _numeric_series(
        df,
        "average_resolution_time_hours",
    )

    employee_count = len(df)

    onboarding_completion_rate = onboarding.mean()

    learning_completion_rate = learning.mean()

    tool_adoption_rate = (
        usage.gt(0).mean() * 100
    )

    average_support_tickets = support.mean()

    average_open_support_tickets = (
        open_support.mean()
    )

    open_ticket_rate = (
        open_support.gt(0).mean() * 100
    )

    average_assessment_score = (
        assessment.mean()
    )

    average_resolution_time_hours = (
        resolution.mean()
    )

    productivity_readiness_score = (
        onboarding_completion_rate * 0.4
        + learning_completion_rate * 0.3
        + tool_adoption_rate * 0.3
    )

    return pd.DataFrame(
        [
            {
                "employee_count": employee_count,
                "onboarding_completion_rate": (
                    onboarding_completion_rate
                ),
                "learning_completion_rate": (
                    learning_completion_rate
                ),
                "tool_adoption_rate": (
                    tool_adoption_rate
                ),
                "average_support_tickets": (
                    average_support_tickets
                ),
                "average_open_support_tickets": (
                    average_open_support_tickets
                ),
                "open_ticket_rate": (
                    open_ticket_rate
                ),
                "average_assessment_score": (
                    average_assessment_score
                ),
                "average_resolution_time_hours": (
                    average_resolution_time_hours
                ),
                "productivity_readiness_score": (
                    productivity_readiness_score
                ),
            }
        ]
    )


def classify_kpi_health(
    kpis: pd.DataFrame,
) -> pd.DataFrame:
    """
    Classify KPI values into business health categories.

    Health levels:
    - healthy
    - attention
    - critical
    """

    required_columns = {
        "onboarding_completion_rate",
        "learning_completion_rate",
        "tool_adoption_rate",
        "open_ticket_rate",
    }

    missing_columns = required_columns.difference(
        kpis.columns
    )

    if missing_columns:
        raise KeyError(
            "Missing KPI columns: "
            + ", ".join(sorted(missing_columns))
        )

    result = kpis.copy()

    def completion_health(value):
        if pd.isna(value):
            return "unknown"

        if value >= 80:
            return "healthy"

        if value >= 60:
            return "attention"

        return "critical"

    def adoption_health(value):
        if pd.isna(value):
            return "unknown"

        if value >= 80:
            return "healthy"

        if value >= 50:
            return "attention"

        return "critical"

    def ticket_health(value):
        if pd.isna(value):
            return "unknown"

        if value <= 20:
            return "healthy"

        if value <= 40:
            return "attention"

        return "critical"

    result["onboarding_health"] = (
        result[
            "onboarding_completion_rate"
        ].apply(completion_health)
    )

    result["learning_health"] = (
        result[
            "learning_completion_rate"
        ].apply(completion_health)
    )

    result["tool_adoption_health"] = (
        result[
            "tool_adoption_rate"
        ].apply(adoption_health)
    )

    result["support_health"] = (
        result[
            "open_ticket_rate"
        ].apply(ticket_health)
    )

    return result


def run_kpi_pipeline(
    input_path: str | Path,
    output_directory: str | Path | None = None,
) -> dict[str, pd.DataFrame]:
    """
    Load the employee analytics dataset and calculate KPIs.

    Optionally saves KPI outputs as CSV files.
    """

    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {input_path}"
        )

    df = pd.read_csv(input_path)

    kpis = calculate_kpis(df)

    kpi_health = classify_kpi_health(kpis)

    results = {
        "kpis": kpis,
        "kpi_health": kpi_health,
    }

    if output_directory is not None:
        output_directory = Path(
            output_directory
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        kpis.to_csv(
            output_directory / "kpis.csv",
            index=False,
        )

        kpi_health.to_csv(
            output_directory / "kpi_health.csv",
            index=False,
        )

    return results