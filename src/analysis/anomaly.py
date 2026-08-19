"""Anomaly detection and root-cause analysis for employee onboarding."""

from pathlib import Path

import numpy as np
import pandas as pd


ANOMALY_COLUMNS = {
    "onboarding_completion_rate": "low",
    "late_onboarding_tasks": "high",
    "total_support_tickets": "high",
    "open_support_tickets": "high",
    "average_resolution_time_hours": "high",
}


def _iqr_bounds(series: pd.Series) -> tuple[float, float]:
    """Return lower and upper IQR bounds for a numeric series."""
    numeric = pd.to_numeric(series, errors="coerce").dropna()

    if numeric.empty:
        return np.nan, np.nan

    q1 = numeric.quantile(0.25)
    q3 = numeric.quantile(0.75)
    iqr = q3 - q1

    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """Detect employee-level onboarding anomalies using the IQR method."""
    if df.empty:
        return pd.DataFrame()

    result = df.copy()

    if "employee_id" not in result.columns:
        raise ValueError("Input data must contain 'employee_id'.")

    anomaly_flags = []

    for column, direction in ANOMALY_COLUMNS.items():
        if column not in result.columns:
            continue

        values = pd.to_numeric(result[column], errors="coerce")
        lower, upper = _iqr_bounds(values)

        flag_column = f"{column}_anomaly"

        if pd.isna(lower) or pd.isna(upper):
            result[flag_column] = False
        elif direction == "low":
            result[flag_column] = values < lower
        else:
            result[flag_column] = values > upper

        anomaly_flags.append(flag_column)

    if not anomaly_flags:
        raise ValueError("No supported anomaly columns were found.")

    result["anomaly_count"] = result[anomaly_flags].sum(axis=1)

    # Risk score represents the proportion of available anomaly indicators.
    result["risk_score"] = (
        result["anomaly_count"] / len(anomaly_flags)
    ).round(2)

    # Risk is based on the number of simultaneous anomaly indicators.
    # 0 anomalies = Low, 1 anomaly = Medium, 2+ anomalies = High.
    result["risk_category"] = np.select(
        [
            result["anomaly_count"] == 0,
            result["anomaly_count"] == 1,
            result["anomaly_count"] >= 2,
        ],
        [
            "Low",
            "Medium",
            "High",
        ],
        default="Low",
    )

    return result


def summarize_anomalies(anomaly_df: pd.DataFrame) -> pd.DataFrame:
    """Create a summary of detected anomalies."""
    if anomaly_df.empty:
        return pd.DataFrame(
            columns=[
                "metric",
                "anomaly_count",
                "anomaly_percentage",
            ]
        )

    rows = []

    for column in ANOMALY_COLUMNS:
        flag_column = f"{column}_anomaly"

        if flag_column not in anomaly_df.columns:
            continue

        count = int(anomaly_df[flag_column].sum())
        percentage = round(
            count / len(anomaly_df) * 100,
            2,
        )

        rows.append(
            {
                "metric": column,
                "anomaly_count": count,
                "anomaly_percentage": percentage,
            }
        )

    return pd.DataFrame(rows)


def investigate_root_causes(
    anomaly_df: pd.DataFrame,
) -> pd.DataFrame:
    """Compare high-risk employees with other employees."""
    if anomaly_df.empty:
        return pd.DataFrame(
            columns=[
                "factor",
                "high_risk_mean",
                "other_mean",
                "difference",
            ]
        )

    numeric_factors = [
        "onboarding_completion_rate",
        "late_onboarding_tasks",
        "total_support_tickets",
        "open_support_tickets",
        "average_resolution_time_hours",
        "learning_completion_rate",
        "total_tool_usage",
    ]

    available_factors = [
        column
        for column in numeric_factors
        if column in anomaly_df.columns
    ]

    high_risk = anomaly_df["risk_category"].eq("High")

    rows = []

    for column in available_factors:
        values = pd.to_numeric(
            anomaly_df[column],
            errors="coerce",
        )

        high_mean = values[high_risk].mean()
        other_mean = values[~high_risk].mean()

        if pd.isna(high_mean) or pd.isna(other_mean):
            continue

        rows.append(
            {
                "factor": column,
                "high_risk_mean": round(high_mean, 2),
                "other_mean": round(other_mean, 2),
                "difference": round(
                    high_mean - other_mean,
                    2,
                ),
            }
        )

    result = pd.DataFrame(rows)

    if not result.empty:
        result["absolute_difference"] = result["difference"].abs()

        result = (
            result.sort_values(
                "absolute_difference",
                ascending=False,
            )
            .drop(columns="absolute_difference")
            .reset_index(drop=True)
        )

    return result


def department_risk_summary(
    anomaly_df: pd.DataFrame,
) -> pd.DataFrame:
    """Summarize risk categories by department."""
    if (
        anomaly_df.empty
        or "Department" not in anomaly_df.columns
    ):
        return pd.DataFrame()

    return (
        anomaly_df.groupby(
            ["Department", "risk_category"],
            observed=True,
        )
        .size()
        .reset_index(name="employee_count")
        .sort_values(
            ["Department", "employee_count"],
            ascending=[True, False],
        )
    )


def run_anomaly_pipeline(
    input_path: str | Path,
    output_directory: str | Path | None = None,
) -> dict[str, pd.DataFrame]:
    """Run anomaly detection and root-cause analysis."""
    input_path = Path(input_path)

    df = pd.read_csv(input_path)

    anomaly_results = detect_anomalies(df)
    anomaly_summary = summarize_anomalies(anomaly_results)
    root_causes = investigate_root_causes(anomaly_results)
    department_summary = department_risk_summary(
        anomaly_results
    )

    outputs = {
        "employee_anomaly_risk": anomaly_results,
        "anomaly_summary": anomaly_summary,
        "root_cause_factors": root_causes,
        "department_risk_summary": department_summary,
    }

    if output_directory is not None:
        output_directory = Path(output_directory)
        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        for name, output_df in outputs.items():
            output_df.to_csv(
                output_directory / f"{name}.csv",
                index=False,
            )

    return outputs