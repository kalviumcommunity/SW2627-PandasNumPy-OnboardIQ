"""Utilities for exporting dashboard data and executive reports."""

from __future__ import annotations

from collections.abc import Mapping

import pandas as pd


def export_dataframe_to_csv(
    dataframe: pd.DataFrame,
) -> bytes:
    """Export a non-empty DataFrame to CSV bytes.

    Args:
        dataframe: DataFrame to export.

    Returns:
        CSV representation of the DataFrame as UTF-8 bytes.

    Raises:
        ValueError: If the DataFrame is empty.
        TypeError: If the supplied object is not a DataFrame.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")

    if dataframe.empty:
        raise ValueError("Cannot export an empty dataframe.")

    return dataframe.to_csv(
        index=False,
    ).encode("utf-8")


def generate_executive_report(
    kpis: Mapping[str, object],
    health: Mapping[str, object] | None = None,
) -> str:
    """Generate a Markdown executive summary report.

    Args:
        kpis: Dictionary-like collection containing calculated KPIs.
        health: Optional dictionary-like collection containing KPI
            health classifications.

    Returns:
        A Markdown-formatted executive summary.
    """
    if not isinstance(kpis, Mapping):
        raise TypeError("kpis must be a mapping.")

    if health is None:
        health = {}

    if not isinstance(health, Mapping):
        raise TypeError("health must be a mapping.")

    employee_count = kpis.get(
        "employee_count",
        0,
    )

    onboarding_rate = kpis.get(
        "onboarding_completion_rate",
        0.0,
    )

    learning_rate = kpis.get(
        "learning_completion_rate",
        0.0,
    )

    tool_adoption_rate = kpis.get(
        "tool_adoption_rate",
        0.0,
    )

    support_tickets = kpis.get(
        "average_support_tickets",
        0.0,
    )

    productivity_score = kpis.get(
        "productivity_readiness_score",
        0.0,
    )

    onboarding_health = str(
        health.get(
            "onboarding_health",
            "",
        )
    ).lower()

    learning_health = str(
        health.get(
            "learning_health",
            "",
        )
    ).lower()

    tool_adoption_health = str(
        health.get(
            "tool_adoption_health",
            "",
        )
    ).lower()

    support_health = str(
        health.get(
            "support_health",
            "",
        )
    ).lower()

    attention_required = any(
        status in {"attention", "critical"}
        for status in (
            onboarding_health,
            learning_health,
            tool_adoption_health,
            support_health,
        )
    )

    lines = [
        "# OnboardIQ Executive Summary Report",
        "",
        "## Executive Overview",
        "",
        f"**Total Employees:** {employee_count}",
        "",
        "## Key Performance Indicators",
        "",
        (
            f"- **Onboarding Completion:** "
            f"{_format_number(onboarding_rate)}%"
        ),
        (
            f"- **Learning Completion:** "
            f"{_format_number(learning_rate)}%"
        ),
        (
            f"- **Tool Adoption:** "
            f"{_format_number(tool_adoption_rate)}%"
        ),
        (
            f"- **Average Support Tickets:** "
            f"{_format_number(support_tickets)}"
        ),
        (
            f"- **Productivity Readiness:** "
            f"{_format_number(productivity_score)}"
        ),
        "",
    ]

    if attention_required:
        lines.extend(
            [
                "## Action Required",
                "",
            ]
        )

        if onboarding_health in {"attention", "critical"}:
            lines.append(
                "- Review onboarding workflows and identify "
                "completion barriers."
            )

        if learning_health in {"attention", "critical"}:
            lines.append(
                "- Review learning completion gaps and "
                "target employees requiring additional support."
            )

        if tool_adoption_health in {"attention", "critical"}:
            lines.append(
                "- Investigate barriers to internal tool adoption "
                "and provide targeted enablement."
            )

        if support_health in {"attention", "critical"}:
            lines.append(
                "- Review support demand and identify recurring "
                "onboarding issues."
            )

        lines.append("")

    else:
        lines.extend(
            [
                "## Recommendations",
                "",
                "- Maintain current onboarding protocols.",
                "- Continue monitoring learning and tool adoption.",
                "- Maintain current employee support processes.",
                "- Continue tracking productivity readiness.",
                "",
            ]
        )

    lines.extend(
        [
            "## KPI Health",
            "",
            (
                f"- **Onboarding:** "
                f"{_format_health(onboarding_health)}"
            ),
            (
                f"- **Learning:** "
                f"{_format_health(learning_health)}"
            ),
            (
                f"- **Tool Adoption:** "
                f"{_format_health(tool_adoption_health)}"
            ),
            (
                f"- **Support:** "
                f"{_format_health(support_health)}"
            ),
            "",
        ]
    )

    return "\n".join(lines)


def _format_number(value: object) -> str:
    """Format a numeric value for executive reporting."""

    if value is None:
        return "N/A"

    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return str(value)


def _format_health(value: str) -> str:
    """Format a KPI health status for display."""

    if not value:
        return "Not available"

    return value.capitalize()