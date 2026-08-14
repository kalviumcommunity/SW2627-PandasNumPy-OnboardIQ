import pandas as pd


def aggregate_onboarding(df: pd.DataFrame) -> pd.DataFrame:
    """Create employee-level onboarding metrics."""

    result = df.copy()

    if "completed_date" in result.columns:
        result["completed_date"] = pd.to_datetime(
            result["completed_date"],
            errors="coerce",
        )

    if "due_date" in result.columns:
        result["due_date"] = pd.to_datetime(
            result["due_date"],
            errors="coerce",
        )

    result["days_overdue"] = (
        result["completed_date"] - result["due_date"]
    ).dt.days.clip(lower=0)

    grouped = (
        result.groupby("employee_id")
        .agg(
            total_onboarding_tasks=(
                "onboarding_task_id",
                "count",
            ),
            completed_onboarding_tasks=(
                "completed_date",
                lambda x: x.notna().sum(),
            ),
            average_completion_percentage=(
                "completion_percentage",
                "mean",
            ),
            late_onboarding_tasks=(
                "days_overdue",
                lambda x: (x > 0).sum(),
            ),
        )
        .reset_index()
    )

    grouped["onboarding_completion_rate"] = (
        grouped["completed_onboarding_tasks"]
        / grouped["total_onboarding_tasks"]
        * 100
    )

    return grouped

def aggregate_tool_usage(df: pd.DataFrame) -> pd.DataFrame:
    """Create employee-level internal tool usage metrics."""

    return (
        df.groupby("employee_id")
        .agg(
            total_usage_records=("usage_id", "count"),
            average_daily_active_usage=(
                "daily_active_usage",
                "mean",
            ),
            total_slack_activity=(
                "slack_activity_count",
                "sum",
            ),
            total_jira_usage=(
                "jira_usage_count",
                "sum",
            ),
            total_github_activity=(
                "github_activity_count",
                "sum",
            ),
            total_teams_activity=(
                "teams_activity_count",
                "sum",
            ),
            total_workspace_activity=(
                "workspace_activity_count",
                "sum",
            ),
        )
        .reset_index()
    )


def aggregate_support_tickets(df: pd.DataFrame) -> pd.DataFrame:
    """Create employee-level support ticket metrics."""

    return (
        df.groupby("employee_id")
        .agg(
            total_support_tickets=("ticket_id", "count"),
            average_resolution_time_hours=(
                "resolution_time_hours",
                "mean",
            ),
            open_support_tickets=(
                "status",
                lambda x: (x != "Closed").sum(),
            ),
        )
        .reset_index()
    )


def aggregate_learning(df: pd.DataFrame) -> pd.DataFrame:
    """Create employee-level learning metrics."""

    grouped = (
        df.groupby("employee_id")
        .agg(
            total_learning_records=(
                "learning_record_id",
                "count",
            ),
            completed_courses=(
                "completed_date",
                lambda x: x.notna().sum(),
            ),
            average_assessment_score=(
                "assessment_score",
                "mean",
            ),
            average_completion_time_hours=(
                "completion_time_hours",
                "mean",
            ),
        )
        .reset_index()
    )

    grouped["learning_completion_rate"] = (
        grouped["completed_courses"]
        / grouped["total_learning_records"]
        * 100
    )

    return grouped


def merge_employee_data(
    employee: pd.DataFrame,
    onboarding: pd.DataFrame,
    tool_usage: pd.DataFrame,
    support_tickets: pd.DataFrame,
    learning: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create one employee-level analytical dataset.

    Child datasets are aggregated before joining so that
    one-to-many relationships do not multiply employee rows.
    """

    onboarding_summary = aggregate_onboarding(onboarding)
    tool_usage_summary = aggregate_tool_usage(tool_usage)
    support_summary = aggregate_support_tickets(support_tickets)
    learning_summary = aggregate_learning(learning)

    result = employee.copy()

    result = result.merge(
        onboarding_summary,
        left_on="EmpID",
        right_on="employee_id",
        how="left",
    )

    result = result.merge(
        tool_usage_summary,
        on="employee_id",
        how="left",
    )

    result = result.merge(
        support_summary,
        on="employee_id",
        how="left",
    )

    result = result.merge(
        learning_summary,
        on="employee_id",
        how="left",
    )

    return result