"""Reusable Plotly charts for the OnboardIQ dashboard."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def _require_columns(
    dataframe: pd.DataFrame,
    columns: list[str],
) -> None:
    """Validate that the dataframe contains the required columns."""
    missing = [
        column
        for column in columns
        if column not in dataframe.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(missing)}"
        )


def create_onboarding_completion_chart(
    dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Create a department-level onboarding completion chart.
    """
    _require_columns(
        dataframe,
        [
            "Department",
            "onboarding_completion_rate",
        ],
    )

    department_data = (
        dataframe
        .groupby("Department", as_index=False)
        ["onboarding_completion_rate"]
        .mean()
        .sort_values(
            "onboarding_completion_rate",
            ascending=False,
        )
    )

    figure = px.bar(
        department_data,
        x="Department",
        y="onboarding_completion_rate",
        title="Onboarding Completion by Department",
        labels={
            "Department": "Department",
            "onboarding_completion_rate":
                "Completion Rate (%)",
        },
        text_auto=".1f",
    )

    figure.update_layout(
        yaxis_range=[0, 100],
        xaxis_title=None,
        hovermode="x unified",
    )

    return figure


def create_productivity_by_department_chart(
    dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Create a department-level productivity comparison chart.
    """
    _require_columns(
        dataframe,
        [
            "Department",
            "average_daily_active_usage",
        ],
    )

    department_data = (
        dataframe
        .groupby("Department", as_index=False)
        ["average_daily_active_usage"]
        .mean()
        .sort_values(
            "average_daily_active_usage",
            ascending=False,
        )
    )

    figure = px.bar(
        department_data,
        x="Department",
        y="average_daily_active_usage",
        title="Average Daily Activity by Department",
        labels={
            "Department": "Department",
            "average_daily_active_usage":
                "Average Daily Active Usage",
        },
        text_auto=".1f",
    )

    figure.update_layout(
        xaxis_title=None,
        hovermode="x unified",
    )

    return figure


def create_learning_completion_chart(
    dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Create a learning completion chart by department.
    """
    _require_columns(
        dataframe,
        [
            "Department",
            "learning_completion_rate",
        ],
    )

    department_data = (
        dataframe
        .groupby("Department", as_index=False)
        ["learning_completion_rate"]
        .mean()
        .sort_values(
            "learning_completion_rate",
            ascending=False,
        )
    )

    figure = px.bar(
        department_data,
        x="Department",
        y="learning_completion_rate",
        title="Learning Completion by Department",
        labels={
            "Department": "Department",
            "learning_completion_rate":
                "Learning Completion Rate (%)",
        },
        text_auto=".1f",
    )

    figure.update_layout(
        yaxis_range=[0, 100],
        xaxis_title=None,
        hovermode="x unified",
    )

    return figure


def create_support_tickets_chart(
    dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Create a department-level support ticket chart.
    """
    _require_columns(
        dataframe,
        [
            "Department",
            "total_support_tickets",
        ],
    )

    department_data = (
        dataframe
        .groupby("Department", as_index=False)
        ["total_support_tickets"]
        .sum()
        .sort_values(
            "total_support_tickets",
            ascending=False,
        )
    )

    figure = px.bar(
        department_data,
        x="Department",
        y="total_support_tickets",
        title="Support Tickets by Department",
        labels={
            "Department": "Department",
            "total_support_tickets":
                "Total Support Tickets",
        },
        text_auto=True,
    )

    figure.update_layout(
        xaxis_title=None,
        hovermode="x unified",
    )

    return figure


def create_tool_usage_chart(
    dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Create a comparison of internal tool activity.
    """
    _require_columns(
        dataframe,
        [
            "total_slack_activity",
            "total_jira_usage",
            "total_github_activity",
            "total_teams_activity",
            "total_workspace_activity",
        ],
    )

    usage = pd.DataFrame(
        {
            "Tool": [
                "Slack",
                "Jira",
                "GitHub",
                "Teams",
                "Workspace",
            ],
            "Activity": [
                dataframe["total_slack_activity"].sum(),
                dataframe["total_jira_usage"].sum(),
                dataframe["total_github_activity"].sum(),
                dataframe["total_teams_activity"].sum(),
                dataframe["total_workspace_activity"].sum(),
            ],
        }
    )

    figure = px.bar(
        usage,
        x="Tool",
        y="Activity",
        title="Internal Tool Usage",
        labels={
            "Tool": "Tool",
            "Activity": "Total Activity",
        },
        text_auto=True,
    )

    figure.update_layout(
        xaxis_title=None,
        hovermode="x unified",
    )

    return figure


def create_performance_distribution_chart(
    dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Create a performance score distribution chart.
    """
    _require_columns(
        dataframe,
        ["PerformanceScore"],
    )

    figure = px.histogram(
        dataframe,
        x="PerformanceScore",
        title="Employee Performance Distribution",
        labels={
            "PerformanceScore": "Performance Score",
        },
        text_auto=True,
    )

    figure.update_layout(
        xaxis_title=None,
        yaxis_title="Number of Employees",
        hovermode="x unified",
    )

    return figure


def create_engagement_vs_completion_chart(
    dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Compare employee engagement with onboarding completion.
    """
    _require_columns(
        dataframe,
        [
            "EngagementSurvey",
            "onboarding_completion_rate",
        ],
    )

    figure = px.scatter(
        dataframe,
        x="EngagementSurvey",
        y="onboarding_completion_rate",
        hover_name=(
            "Employee_Name"
            if "Employee_Name" in dataframe.columns
            else None
        ),
        title=(
            "Employee Engagement vs "
            "Onboarding Completion"
        ),
        labels={
            "EngagementSurvey": "Engagement Score",
            "onboarding_completion_rate":
                "Onboarding Completion Rate (%)",
        },
    )

    figure.update_layout(
        hovermode="closest",
    )

    return figure


def create_activity_vs_support_chart(
    dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Compare employee activity with support ticket volume.
    """
    _require_columns(
        dataframe,
        [
            "average_daily_active_usage",
            "total_support_tickets",
        ],
    )

    figure = px.scatter(
        dataframe,
        x="average_daily_active_usage",
        y="total_support_tickets",
        hover_name=(
            "Employee_Name"
            if "Employee_Name" in dataframe.columns
            else None
        ),
        title=(
            "Employee Activity vs "
            "Support Ticket Volume"
        ),
        labels={
            "average_daily_active_usage":
                "Average Daily Active Usage",
            "total_support_tickets":
                "Total Support Tickets",
        },
    )

    return figure


def create_department_summary_chart(
    dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Create a grouped chart combining key departmental metrics.
    """
    _require_columns(
        dataframe,
        [
            "Department",
            "onboarding_completion_rate",
            "learning_completion_rate",
        ],
    )

    department_data = (
        dataframe
        .groupby("Department", as_index=False)
        .agg(
            onboarding_completion_rate=(
                "onboarding_completion_rate",
                "mean",
            ),
            learning_completion_rate=(
                "learning_completion_rate",
                "mean",
            ),
        )
    )

    long_data = department_data.melt(
        id_vars="Department",
        value_vars=[
            "onboarding_completion_rate",
            "learning_completion_rate",
        ],
        var_name="Metric",
        value_name="Rate",
    )

    long_data["Metric"] = long_data["Metric"].replace(
        {
            "onboarding_completion_rate":
                "Onboarding Completion",
            "learning_completion_rate":
                "Learning Completion",
        }
    )

    figure = px.bar(
        long_data,
        x="Department",
        y="Rate",
        color="Metric",
        barmode="group",
        title="Department Performance Summary",
        labels={
            "Department": "Department",
            "Rate": "Completion Rate (%)",
            "Metric": "Metric",
        },
        text_auto=".1f",
    )

    figure.update_layout(
        yaxis_range=[0, 100],
        xaxis_title=None,
        hovermode="x unified",
    )

    return figure