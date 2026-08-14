import pandas as pd


def calculate_onboarding_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate employee-level onboarding completion features."""
    result = df.copy()

    if "task_status" in result.columns:
        result["completed_onboarding_tasks"] = (
            result["task_status"].astype("string").str.lower().eq("completed")
        )

        result["completed_onboarding_tasks"] = (
            result["completed_onboarding_tasks"].astype(int)
        )

        grouped = result.groupby("employee_id")["completed_onboarding_tasks"]

        summary = grouped.agg(
            completed_onboarding_tasks="sum",
            total_onboarding_tasks="count",
        ).reset_index()

        summary["onboarding_completion_percentage"] = (
            summary["completed_onboarding_tasks"]
            / summary["total_onboarding_tasks"]
            * 100
        )

        return summary

    return result


def calculate_support_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate employee-level support ticket burden."""
    if "employee_id" not in df.columns:
        return df.copy()

    result = (
        df.groupby("employee_id")
        .size()
        .reset_index(name="support_ticket_count")
    )

    return result


def calculate_first_week_activity(
    tool_usage: pd.DataFrame,
    employee: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate tool activity during each employee's first seven days."""
    usage = tool_usage.copy()
    employees = employee.copy()

    if not {"employee_id", "usage_date"}.issubset(usage.columns):
        return pd.DataFrame()

    if not {"EmpID", "DateofHire"}.issubset(employees.columns):
        return pd.DataFrame()

    usage["usage_date"] = pd.to_datetime(
        usage["usage_date"], errors="coerce"
    )
    employees["DateofHire"] = pd.to_datetime(
        employees["DateofHire"], errors="coerce"
    )

    usage = usage.merge(
        employees[["EmpID", "DateofHire"]],
        left_on="employee_id",
        right_on="EmpID",
        how="left",
    )

    days_from_hire = (
        usage["usage_date"] - usage["DateofHire"]
    ).dt.days

    usage = usage[days_from_hire.between(0, 6)]

    activity_columns = [
        "slack_activity_count",
        "jira_usage_count",
        "github_activity_count",
        "teams_activity_count",
        "workspace_activity_count",
    ]

    available_columns = [
        column for column in activity_columns
        if column in usage.columns
    ]

    if not available_columns:
        return pd.DataFrame()

    usage["first_week_activity"] = usage[available_columns].fillna(0).sum(
        axis=1
    )

    return (
        usage.groupby("employee_id")["first_week_activity"]
        .sum()
        .reset_index()
    )


def calculate_learning_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate employee-level learning completion rate."""
    if not {"employee_id", "course_status"}.issubset(df.columns):
        return pd.DataFrame()

    result = df.copy()

    result["completed_course"] = (
        result["course_status"]
        .astype("string")
        .str.lower()
        .eq("completed")
    )

    summary = (
        result.groupby("employee_id")
        .agg(
            total_learning_courses=("course_status", "count"),
            completed_learning_courses=("completed_course", "sum"),
        )
        .reset_index()
    )

    summary["learning_completion_rate"] = (
        summary["completed_learning_courses"]
        / summary["total_learning_courses"]
        * 100
    )

    return summary


def calculate_productivity_indicator(df: pd.DataFrame) -> pd.DataFrame:
    """Create a simple onboarding productivity proxy."""
    result = df.copy()

    required = {
        "onboarding_completion_percentage",
        "learning_completion_rate",
        "first_week_activity",
    }

    if not required.issubset(result.columns):
        return result

    result["productivity_indicator"] = (
        result["onboarding_completion_percentage"].fillna(0)
        + result["learning_completion_rate"].fillna(0)
        + result["first_week_activity"].fillna(0)
    )

    return result
