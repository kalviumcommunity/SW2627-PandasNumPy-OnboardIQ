from src.analysis.trends import (
    add_rolling_metrics,
    calculate_department_productivity,
    calculate_employee_productivity_scores,
    calculate_monthly_onboarding_trend,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DEFAULT_DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "employee_onboarding_analytics.csv"
)


def load_dashboard_dataset() -> pd.DataFrame:
    """Load the default processed employee analytics dataset."""

    if not DEFAULT_DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dashboard dataset not found: {DEFAULT_DATASET_PATH}"
        )

    dataframe = pd.read_csv(DEFAULT_DATASET_PATH)

    if dataframe.empty:
        raise ValueError(
            "Dashboard dataset contains no data."
        )

    return dataframe


def calculate_dashboard_kpis(
    dataframe: pd.DataFrame,
) -> dict:
    """Calculate KPI values using the existing KPI analysis module."""

    kpi_dataframe = calculate_kpis(dataframe)

    if kpi_dataframe.empty:
        raise ValueError(
            "KPI calculation returned no results."
        )

    return kpi_dataframe.iloc[0].to_dict()


def render_onboarding_trend(
    dataframe: pd.DataFrame,
) -> None:
    """Render the monthly onboarding trend visualization."""

    trend = calculate_monthly_onboarding_trend(dataframe)
    trend = add_rolling_metrics(trend)

    if trend.empty:
        st.warning("No onboarding trend data is available.")
        return

    trend["hire_month"] = pd.to_datetime(trend["hire_month"])

    chart_data = trend.set_index("hire_month")[
        [
            "rolling_onboarding_completion_rate",
            "rolling_learning_completion_rate",
        ]
    ].rename(
        columns={
            "rolling_onboarding_completion_rate": "Onboarding Completion",
            "rolling_learning_completion_rate": "Learning Completion",
        }
    )

    st.subheader("Onboarding Trend")

    st.caption(
        "Monthly onboarding and learning completion rates "
        "with rolling metrics."
    )

    st.line_chart(
        chart_data,
        y=["Onboarding Completion", "Learning Completion"],
        use_container_width=True,
    )


def render_department_overview(
    dataframe: pd.DataFrame,
) -> None:
    """Render employee distribution by department."""

    if "Department" not in dataframe.columns:
        st.warning(
            "Department information is not available in the dataset."
        )
        return

    department_data = (
        dataframe["Department"]
        .value_counts()
        .rename_axis("Department")
        .reset_index(name="Employee Count")
    )

    st.subheader("Employees by Department")

    st.caption(
        "Distribution of employees across organizational departments."
    )

    chart_data = department_data.set_index("Department")

    st.bar_chart(
        chart_data,
        y="Employee Count",
        use_container_width=True,
    )


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

    # KPI cards
    render_kpi_cards(kpis)

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


if __name__ == "__main__":
    render_kpi_dashboard()

def render_productivity_by_department(
    dataframe: pd.DataFrame,
) -> None:
    """Render average productivity score by department."""

    required_columns = {"Department"}

    if not required_columns.issubset(dataframe.columns):
        st.warning(
            "Department information is not available in the dataset."
        )
        return

    scored = calculate_employee_productivity_scores(dataframe)

    scored = scored.merge(
        dataframe[["EmpID", "Department"]],
        on="EmpID",
        how="left",
    )

    department_productivity = calculate_department_productivity(
        scored
    )

    if department_productivity.empty:
        st.warning(
            "No department productivity data is available."
        )
        return

    department_productivity = department_productivity.set_index(
        "Department"
    )

    st.subheader("Productivity by Department")

    st.caption(
        "Average employee productivity score across departments."
    )

    st.bar_chart(
        department_productivity[
            ["average_productivity_score"]
        ].rename(
            columns={
                "average_productivity_score": "Average Productivity"
            }
        ),
        use_container_width=True,
    )