from __future__ import annotations

from typing import Any

import pandas as pd


# ============================================================
# DEFAULT KPI THRESHOLDS
# ============================================================

DEFAULT_THRESHOLDS: dict[str, dict[str, Any]] = {
    "onboarding_completion_rate": {
        "warning": 80.0,
        "critical": 60.0,
        "direction": "higher_is_better",
        "label": "Onboarding Completion",
    },
    "learning_completion_rate": {
        "warning": 75.0,
        "critical": 50.0,
        "direction": "higher_is_better",
        "label": "Learning Completion",
    },
    "tool_adoption_rate": {
        "warning": 75.0,
        "critical": 50.0,
        "direction": "higher_is_better",
        "label": "Tool Adoption",
    },
    "productivity_readiness_score": {
        "warning": 70.0,
        "critical": 50.0,
        "direction": "higher_is_better",
        "label": "Productivity Readiness",
    },
}


# ============================================================
# THRESHOLD DETECTION
# ============================================================


def detect_kpi_alerts(
    kpis: dict[str, Any],
    thresholds: dict[str, dict[str, Any]] | None = None,
) -> pd.DataFrame:
    """
    Detect KPI threshold violations.

    Parameters
    ----------
    kpis:
        Dictionary containing calculated KPI values.

    thresholds:
        Optional threshold configuration. When omitted,
        DEFAULT_THRESHOLDS is used.

    Returns
    -------
    pd.DataFrame
        One row per monitored KPI containing its value,
        threshold status, severity, and alert message.
    """

    if not isinstance(kpis, dict):
        raise ValueError("kpis must be a dictionary.")

    threshold_config = (
        DEFAULT_THRESHOLDS
        if thresholds is None
        else thresholds
    )

    alerts: list[dict[str, Any]] = []

    for metric, config in threshold_config.items():
        value = kpis.get(metric)

        if value is None or pd.isna(value):
            continue

        warning = float(config["warning"])
        critical = float(config["critical"])
        direction = config.get(
            "direction",
            "higher_is_better",
        )
        label = config.get(
            "label",
            metric.replace("_", " ").title(),
        )

        severity = "Normal"
        status = "Within Threshold"

        if direction == "higher_is_better":
            if value < critical:
                severity = "Critical"
                status = "Critical"
            elif value < warning:
                severity = "Warning"
                status = "Warning"

        elif direction == "lower_is_better":
            if value > critical:
                severity = "Critical"
                status = "Critical"
            elif value > warning:
                severity = "Warning"
                status = "Warning"

        else:
            raise ValueError(
                f"Unsupported threshold direction: {direction}"
            )

        alerts.append(
            {
                "metric": metric,
                "label": label,
                "value": float(value),
                "warning_threshold": warning,
                "critical_threshold": critical,
                "status": status,
                "severity": severity,
                "alert_message": _build_alert_message(
                    label,
                    float(value),
                    severity,
                ),
            }
        )

    return pd.DataFrame(alerts)


# ============================================================
# ALERT MESSAGE
# ============================================================


def _build_alert_message(
    label: str,
    value: float,
    severity: str,
) -> str:
    """Build a human-readable KPI alert message."""

    if severity == "Critical":
        return (
            f"{label} is critically low at "
            f"{value:.2f}%. Immediate attention required."
        )

    if severity == "Warning":
        return (
            f"{label} is below the target threshold "
            f"at {value:.2f}%."
        )

    return (
        f"{label} is within the expected threshold "
        f"at {value:.2f}%."
    )


# ============================================================
# ACTIVE ALERTS
# ============================================================


def get_active_alerts(
    alerts: pd.DataFrame,
) -> pd.DataFrame:
    """
    Return only Warning and Critical alerts.
    """

    if alerts.empty:
        return alerts.copy()

    return alerts[
        alerts["severity"].isin(
            ["Warning", "Critical"]
        )
    ].reset_index(drop=True)


# ============================================================
# ALERT SUMMARY
# ============================================================


def summarize_alerts(
    alerts: pd.DataFrame,
) -> dict[str, int]:
    """
    Return counts of alerts by severity.
    """

    if alerts.empty:
        return {
            "total_alerts": 0,
            "critical_alerts": 0,
            "warning_alerts": 0,
        }

    return {
        "total_alerts": int(
            len(get_active_alerts(alerts))
        ),
        "critical_alerts": int(
            (alerts["severity"] == "Critical").sum()
        ),
        "warning_alerts": int(
            (alerts["severity"] == "Warning").sum()
        ),
    }