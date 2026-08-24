import streamlit as st


def render_page_header(
    title: str,
    description: str | None = None,
) -> None:
    """Render a consistent dashboard page header."""
    st.title(title)

    if description:
        st.write(description)


def render_kpi_cards(kpis: dict) -> None:
    """Render KPI values as Streamlit metric cards."""

    cards = [
        ("Total Employees", kpis.get("employee_count"), "number"),
        (
            "Onboarding Completion",
            kpis.get("onboarding_completion_rate"),
            "percentage",
        ),
        (
            "Learning Completion",
            kpis.get("learning_completion_rate"),
            "percentage",
        ),
        (
            "Tool Adoption",
            kpis.get("tool_adoption_rate"),
            "percentage",
        ),
        (
            "Avg. Support Tickets",
            kpis.get("average_support_tickets"),
            "decimal",
        ),
        (
            "Assessment Score",
            kpis.get("average_assessment_score"),
            "decimal",
        ),
        (
            "Productivity Readiness",
            kpis.get("productivity_readiness_score"),
            "decimal",
        ),
    ]

    columns = st.columns(4)

    for index, (label, value, value_type) in enumerate(cards):
        column = columns[index % 4]

        if value is None:
            display_value = "N/A"
        elif value_type == "number":
            display_value = f"{int(value):,}"
        elif value_type == "percentage":
            display_value = f"{float(value):.1f}%"
        else:
            display_value = f"{float(value):.2f}"

        column.metric(label, display_value)