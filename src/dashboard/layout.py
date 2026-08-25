import streamlit as st


def render_page_header(
    title: str,
    description: str | None = None,
) -> None:
    """Render a consistent dashboard page header."""
    st.title(title)

    if description:
        st.write(description)


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

    for index, (label, value, value_type, health_status) in enumerate(cards):
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

            st.metric(label=display_label, value=display_value)


def render_insight_narratives(
    kpis: dict,
    health: dict | None = None,
) -> None:
    """Render data storytelling and executive insight narratives."""

    if health is None:
        health = {}

    st.subheader("📊 Executive Insights")

    insights = []

    # 1. Onboarding Insight
    onboard_health = health.get("onboarding_health")
    onboard_val = kpis.get("onboarding_completion_rate", 0)
    if onboard_health == "healthy":
        insights.append(
            f"✅ **Onboarding is strong:** Completion rate is at a healthy {onboard_val:.1f}%."
        )
    elif onboard_health == "attention":
        insights.append(
            f"⚠️ **Onboarding needs attention:** Completion rate is at {onboard_val:.1f}%, below the ideal target."
        )
    elif onboard_health == "critical":
        insights.append(
            f"🚨 **Critical onboarding drop:** Completion rate is critically low at {onboard_val:.1f}%."
        )

    # 2. Learning Insight
    learn_health = health.get("learning_health")
    learn_val = kpis.get("learning_completion_rate", 0)
    if learn_health == "healthy":
        insights.append(
            f"✅ **Learning progress is on track** with a {learn_val:.1f}% completion rate."
        )
    else:
        insights.append(
            f"⚠️ **Learning completion ({learn_val:.1f}%)** requires more focus to ensure employee readiness."
        )

    # 3. Tool Adoption Insight
    adopt_health = health.get("tool_adoption_health")
    adopt_val = kpis.get("tool_adoption_rate", 0)
    if adopt_health == "healthy":
        insights.append(
            f"✅ **Tool adoption is excellent** at {adopt_val:.1f}%, showing great digital readiness."
        )
    else:
        insights.append(
            f"⚠️ **Tool adoption is at {adopt_val:.1f}**. Some employees may need additional training."
        )

    # 4. Support Insight
    support_health = health.get("support_health")
    support_val = kpis.get("open_ticket_rate", 0)
    if support_health == "healthy":
        insights.append(
            f"✅ **Support burden is low**, with only {support_val:.1f}% of employees having open tickets."
        )
    else:
        insights.append(
            f"⚠️ **Support demand is elevated**, with {support_val:.1f}% of employees having open tickets."
        )

    # Render the insights as a clean bulleted list
    for insight in insights:
        st.markdown(f"- {insight}")