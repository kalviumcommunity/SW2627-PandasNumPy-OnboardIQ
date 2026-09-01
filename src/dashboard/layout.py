"""Reusable Streamlit layout components."""

from __future__ import annotations

import streamlit as st

from src.config.settings import APP_NAME, VERSION
from src.dashboard.session import reset_dashboard_session


def configure_page() -> None:
    """Configure the Streamlit page."""
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_header(
    title: str,
    subtitle: str | None = None,
) -> None:
    """Render a reusable page header."""
    st.title(title)

    if subtitle:
        st.caption(subtitle)


def render_page_header(
    title: str,
    description: str | None = None,
) -> None:
    """Render a consistent dashboard page header."""
    st.title(title)

    if description:
        st.write(description)


def render_sidebar_footer() -> None:
    """Render application information and session controls."""
    st.sidebar.divider()

    st.sidebar.caption(APP_NAME)
    st.sidebar.caption(f"Version {VERSION}")

    st.sidebar.divider()

    if st.sidebar.button(
        "Reset Dashboard Session",
        use_container_width=True,
    ):
        reset_dashboard_session()
        st.rerun()


def render_metric_cards(
    metrics: list[dict[str, str]],
) -> None:
    """
    Render reusable metric cards.

    Each metric dictionary should contain:
    - label
    - value
    - optional help
    """
    columns = st.columns(len(metrics))

    for column, metric in zip(columns, metrics):
        with column:
            help_text = metric.get("help")

            st.metric(
                label=metric["label"],
                value=metric["value"],
                help=help_text,
            )


def render_active_filters(
    filters: dict[str, str],
) -> None:
    """Render the currently active dashboard filters."""

    active_filters = {
        key: value
        for key, value in filters.items()
        if value and value != "All"
    }

    if not active_filters:
        return

    st.caption("Active Filters")

    columns = st.columns(len(active_filters))

    for column, (key, value) in zip(
        columns,
        active_filters.items(),
    ):
        display_key = key.replace("_", " ").title()

        with column:
            st.info(
                f"**{display_key}:** {value}"
            )


def _get_health_emoji(health_status: str | None) -> str:
    """Return an emoji based on the KPI health status."""
    if health_status == "healthy":
        return "🟢"

    if health_status == "attention":
        return "🟡"

    if health_status == "critical":
        return "🔴"

    return "⚪"


def render_kpi_cards(
    kpis: dict,
    health: dict | None = None,
) -> None:
    """Render KPI values as Streamlit metric cards with health indicators."""

    if health is None:
        health = {}

    cards = [
        (
            "Total Employees",
            kpis.get("employee_count"),
            "number",
            None,
        ),
        (
            "Onboarding Completion",
            kpis.get("onboarding_completion_rate"),
            "percentage",
            health.get("onboarding_health"),
        ),
        (
            "Learning Completion",
            kpis.get("learning_completion_rate"),
            "percentage",
            health.get("learning_health"),
        ),
        (
            "Tool Adoption",
            kpis.get("tool_adoption_rate"),
            "percentage",
            health.get("tool_adoption_health"),
        ),
        (
            "Avg. Support Tickets",
            kpis.get("average_support_tickets"),
            "decimal",
            health.get("support_health"),
        ),
        (
            "Assessment Score",
            kpis.get("average_assessment_score"),
            "decimal",
            None,
        ),
        (
            "Productivity Readiness",
            kpis.get("productivity_readiness_score"),
            "decimal",
            None,
        ),
    ]

    columns = st.columns(4)

    for index, (
        label,
        value,
        value_type,
        health_status,
    ) in enumerate(cards):
        column = columns[index % 4]

        with column:
            emoji = _get_health_emoji(health_status)
            display_label = f"{emoji} {label}"

            if value is None:
                display_value = "N/A"

            elif value_type == "number":
                display_value = f"{int(value):,}"

            elif value_type == "percentage":
                display_value = f"{float(value):.1f}%"

            else:
                display_value = f"{float(value):.2f}"

            st.metric(
                label=display_label,
                value=display_value,
            )


def render_insight_narratives(
    kpis: dict,
    health: dict | None = None,
) -> None:
    """Render data storytelling and executive insight narratives."""

    if health is None:
        health = {}

    st.subheader("📊 Executive Insights")

    insights: list[str] = []

    # 1. Onboarding Insight
    onboard_health = health.get("onboarding_health")
    onboard_val = kpis.get(
        "onboarding_completion_rate",
        0,
    )

    if onboard_health == "healthy":
        insights.append(
            f"✅ **Onboarding is strong:** "
            f"Completion rate is at a healthy "
            f"{float(onboard_val):.1f}%."
        )

    elif onboard_health == "attention":
        insights.append(
            f"🟡 **Onboarding needs attention:** "
            f"Completion rate is "
            f"{float(onboard_val):.1f}%."
        )

    elif onboard_health == "critical":
        insights.append(
            f"🔴 **Onboarding is below target:** "
            f"Completion rate is only "
            f"{float(onboard_val):.1f}%."
        )

    # 2. Learning Insight
    learning_health = health.get("learning_health")
    learning_val = kpis.get(
        "learning_completion_rate",
        0,
    )

    if learning_health == "healthy":
        insights.append(
            f"✅ **Learning progress is healthy:** "
            f"Course completion is "
            f"{float(learning_val):.1f}%."
        )

    elif learning_health == "attention":
        insights.append(
            f"🟡 **Learning progress needs attention:** "
            f"Course completion is "
            f"{float(learning_val):.1f}%."
        )

    elif learning_health == "critical":
        insights.append(
            f"🔴 **Learning completion is low:** "
            f"Course completion is "
            f"{float(learning_val):.1f}%."
        )

    # 3. Tool Adoption Insight
    tool_health = health.get("tool_adoption_health")
    tool_val = kpis.get(
        "tool_adoption_rate",
        0,
    )

    if tool_health == "healthy":
        insights.append(
            f"✅ **Tool adoption is strong:** "
            f"Adoption rate is "
            f"{float(tool_val):.1f}%."
        )

    elif tool_health == "attention":
        insights.append(
            f"🟡 **Tool adoption needs attention:** "
            f"Adoption rate is "
            f"{float(tool_val):.1f}%."
        )

    elif tool_health == "critical":
        insights.append(
            f"🔴 **Tool adoption is low:** "
            f"Adoption rate is "
            f"{float(tool_val):.1f}%."
        )

    # 4. Support Insight
    support_health = health.get("support_health")
    support_val = kpis.get(
        "average_support_tickets",
        0,
    )

    if support_health == "healthy":
        insights.append(
            f"✅ **Support demand is manageable:** "
            f"Employees average "
            f"{float(support_val):.2f} support tickets."
        )

    elif support_health == "attention":
        insights.append(
            f"🟡 **Support demand requires attention:** "
            f"Employees average "
            f"{float(support_val):.2f} support tickets."
        )

    elif support_health == "critical":
        insights.append(
            f"🔴 **Support demand is high:** "
            f"Employees average "
            f"{float(support_val):.2f} support tickets."
        )

    # 5. Productivity Insight
    productivity_val = kpis.get(
        "productivity_readiness_score",
    )

    if productivity_val is not None:
        insights.append(
            f"📈 **Productivity readiness:** "
            f"The current readiness score is "
            f"{float(productivity_val):.2f}."
        )

    # Render insights
    if insights:
        for insight in insights:
            st.markdown(insight)
    else:
        st.info(
            "No executive insights are available "
            "for the current dataset."
        )


def render_empty_state(
    title: str = "No data available",
    message: str | None = None,
) -> None:
    """Render a simple empty-state panel used by dashboard pages."""
    st.subheader(title)
    if message:
        st.info(message)
    else:
        st.info("There is no data to display for the current selection.")