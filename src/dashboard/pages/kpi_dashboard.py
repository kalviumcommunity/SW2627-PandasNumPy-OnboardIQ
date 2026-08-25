def render_kpi_dashboard(
    dataframe: pd.DataFrame | None = None,
) -> None:
    """Render the OnboardIQ KPI dashboard."""

    render_page_header(
        "OnboardIQ KPI Dashboard",
        "Monitor employee onboarding, learning, tool adoption, "
        "support, assessment, and productivity readiness.",
    )

    if dataframe is None:
        dataframe = load_dashboard_dataset()

    if dataframe.empty:
        st.warning(
            "No employee data is available for the dashboard."
        )
        return

    kpis = calculate_dashboard_kpis(dataframe)

    # --- NEW: Calculate health status and render insights ---
    from src.analysis.kpis import classify_kpi_health
    from src.dashboard.layout import render_insight_narratives

    health_df = classify_kpi_health(pd.DataFrame([kpis]))
    health_dict = health_df.iloc[0].to_dict()

    # KPI cards with health indicators (Green/Yellow/Red)
    render_kpi_cards(kpis, health=health_dict)

    st.divider()

    # Executive Insight Narratives
    render_insight_narratives(kpis, health=health_dict)
    # ----------------------------------------------------

    st.divider()

    # Onboarding trend
    render_onboarding_trend(dataframe)

    st.divider()

    # Department overview
    render_department_overview(dataframe)

    st.divider()

    # KPI summary
    st.subheader("KPI Summary")

    summary = pd.DataFrame(
        [
            {
                "KPI": "Total Employees",
                "Value": kpis["employee_count"],
            },
            {
                "KPI": "Onboarding Completion",
                "Value": (
                    f"{kpis['onboarding_completion_rate']:.2f}%"
                ),
            },
            {
                "KPI": "Learning Completion",
                "Value": (
                    f"{kpis['learning_completion_rate']:.2f}%"
                ),
            },
            {
                "KPI": "Tool Adoption",
                "Value": (
                    f"{kpis['tool_adoption_rate']:.2f}%"
                ),
            },
            {
                "KPI": "Average Support Tickets",
                "Value": (
                    f"{kpis['average_support_tickets']:.2f}"
                ),
            },
            {
                "KPI": "Assessment Score",
                "Value": (
                    f"{kpis['average_assessment_score']:.2f}"
                ),
            },
            {
                "KPI": "Productivity Readiness",
                "Value": (
                    f"{kpis['productivity_readiness_score']:.2f}"
                ),
            },
        ]
    )

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True,
    )