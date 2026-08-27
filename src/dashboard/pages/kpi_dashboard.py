from __future__ import annotations

import pandas as pd
import streamlit as st

from src.analysis.kpis import classify_kpi_health
from src.dashboard.data import load_dashboard_dataset
from src.dashboard.kpis import calculate_dashboard_kpis
from src.dashboard.layout import (
    render_department_overview,
    render_insight_narratives,
    render_kpi_cards,
    render_onboarding_trend,
    render_page_header,
)


def render_kpi_dashboard(
    dataframe: pd.DataFrame | None = None,
) -> None:
    """Render the OnboardIQ KPI dashboard."""

    render_page_header(
        "OnboardIQ KPI Dashboard",
        (
            "Monitor employee onboarding, learning, tool adoption, "
            "support, assessment, and productivity readiness."
        ),
    )

    # ------------------------------------------------------------------
    # Load dashboard data
    # ------------------------------------------------------------------
    if dataframe is None:
        dataframe = load_dashboard_dataset()

    if dataframe is None or dataframe.empty:
        st.warning(
            "No employee data is available for the dashboard."
        )
        return

    # ------------------------------------------------------------------
    # Calculate KPIs
    # ------------------------------------------------------------------
    try:
        kpis = calculate_dashboard_kpis(dataframe)
    except (KeyError, ValueError, TypeError) as exc:
        st.error(
            "Unable to calculate dashboard KPIs from the available data."
        )
        st.caption(f"Details: {exc}")
        return

    if not kpis:
        st.warning(
            "No KPI results are available for the dashboard."
        )
        return

    # ------------------------------------------------------------------
    # Calculate KPI health
    # ------------------------------------------------------------------
    health_dict: dict[str, object] = {}

    try:
        health_df = classify_kpi_health(
            pd.DataFrame([kpis])
        )

        if not health_df.empty:
            health_dict = health_df.iloc[0].to_dict()

    except (KeyError, ValueError, TypeError) as exc:
        # KPI cards can still be displayed even when health
        # classification is unavailable.
        st.warning(
            "KPI health indicators could not be calculated."
        )
        st.caption(f"Details: {exc}")

    # ------------------------------------------------------------------
    # KPI cards
    # ------------------------------------------------------------------
    render_kpi_cards(
        kpis,
        health=health_dict,
    )

    st.divider()

    # ------------------------------------------------------------------
    # Executive insights
    # ------------------------------------------------------------------
    render_insight_narratives(
        kpis,
        health=health_dict,
    )

    st.divider()

    # ------------------------------------------------------------------
    # Onboarding trend
    # ------------------------------------------------------------------
    try:
        render_onboarding_trend(dataframe)
    except (KeyError, ValueError, TypeError) as exc:
        st.warning(
            "The onboarding trend could not be displayed "
            "using the available data."
        )
        st.caption(f"Details: {exc}")

    st.divider()

    # ------------------------------------------------------------------
    # Department overview
    # ------------------------------------------------------------------
    try:
        render_department_overview(dataframe)
    except (KeyError, ValueError, TypeError) as exc:
        st.warning(
            "The department overview could not be displayed "
            "using the available data."
        )
        st.caption(f"Details: {exc}")

    st.divider()

    # ------------------------------------------------------------------
    # KPI summary
    # ------------------------------------------------------------------
    render_kpi_summary(kpis)


def render_kpi_summary(
    kpis: dict[str, object],
) -> None:
    """Render a tabular summary of the dashboard KPIs."""

    st.subheader("KPI Summary")

    summary = pd.DataFrame(
        [
            {
                "KPI": "Total Employees",
                "Value": kpis.get(
                    "employee_count",
                    0,
                ),
            },
            {
                "KPI": "Onboarding Completion",
                "Value": kpis.get(
                    "onboarding_completion_rate",
                    0.0,
                ),
                "Unit": "%",
            },
            {
                "KPI": "Learning Completion",
                "Value": kpis.get(
                    "learning_completion_rate",
                    0.0,
                ),
                "Unit": "%",
            },
            {
                "KPI": "Tool Adoption",
                "Value": kpis.get(
                    "tool_adoption_rate",
                    0.0,
                ),
                "Unit": "%",
            },
            {
                "KPI": "Average Support Tickets",
                "Value": kpis.get(
                    "average_support_tickets",
                    0.0,
                ),
                "Unit": "",
            },
            {
                "KPI": "Assessment Score",
                "Value": kpis.get(
                    "average_assessment_score",
                    0.0,
                ),
                "Unit": "",
            },
            {
                "KPI": "Productivity Readiness",
                "Value": kpis.get(
                    "productivity_readiness_score",
                    0.0,
                ),
                "Unit": "",
            },
        ]
    )

    # ------------------------------------------------------------------
    # Format values for display only.
    # ------------------------------------------------------------------
    def format_value(row: pd.Series) -> str:
        """Format a KPI value according to its unit."""

        value = row["Value"]
        unit = row.get("Unit", "")

        if pd.isna(value):
            return "N/A"

        if isinstance(value, (int, float)) or pd.api.types.is_number(value):
            if unit == "%":
                return f"{float(value):.2f}%"

            return f"{float(value):.2f}"

        return str(value)

    summary["Value"] = summary.apply(
        format_value,
        axis=1,
    )

    if "Unit" in summary.columns:
        summary = summary.drop(columns=["Unit"])

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True,
    )