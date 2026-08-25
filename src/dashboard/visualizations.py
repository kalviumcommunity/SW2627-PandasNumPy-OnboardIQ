"""Reusable Plotly visualizations for the OnboardIQ dashboard."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_onboarding_completion_chart(df: pd.DataFrame) -> go.Figure:
    """Create a department-level onboarding completion chart."""

    required_columns = {
        "Department",
        "onboarding_completion_rate",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    department_data = (
        df.groupby("Department", as_index=False)[
            "onboarding_completion_rate"
        ]
        .mean()
        .sort_values(
            "onboarding_completion_rate",
            ascending=False,
        )
    )

    fig = px.bar(
        department_data,
        x="Department",
        y="onboarding_completion_rate",
        title="Onboarding Completion by Department",
        labels={
            "Department": "Department",
            "onboarding_completion_rate": "Completion Rate (%)",
        },
        text_auto=".1f",
    )

    fig.update_layout(
        xaxis_title="Department",
        yaxis_title="Completion Rate (%)",
        yaxis=dict(range=[0, 100]),
        hovermode="x unified",
    )

    return fig


def create_productivity_by_department_chart(
    df: pd.DataFrame,
) -> go.Figure:
    """Create a department productivity comparison chart."""

    required_columns = {
        "Department",
        "average_daily_active_usage",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    department_data = (
        df.groupby("Department", as_index=False)[
            "average_daily_active_usage"
        ]
        .mean()
        .sort_values(
            "average_daily_active_usage",
            ascending=False,
        )
    )

    fig = px.bar(
        department_data,
        x="Department",
        y="average_daily_active_usage",
        title="Average Daily Tool Usage by Department",
        labels={
            "Department": "Department",
            "average_daily_active_usage": (
                "Average Daily Active Usage"
            ),
        },
        text_auto=".1f",
    )

    fig.update_layout(
        xaxis_title="Department",
        yaxis_title="Average Daily Active Usage",
        hovermode="x unified",
    )

    return fig


def create_support_tickets_chart(df: pd.DataFrame) -> go.Figure:
    """Create a department-level support ticket chart."""

    required_columns = {
        "Department",
        "total_support_tickets",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    department_data = (
        df.groupby("Department", as_index=False)[
            "total_support_tickets"
        ]
        .sum()
        .sort_values(
            "total_support_tickets",
            ascending=False,
        )
    )

    fig = px.bar(
        department_data,
        x="Department",
        y="total_support_tickets",
        title="Support Tickets by Department",
        labels={
            "Department": "Department",
            "total_support_tickets": "Support Tickets",
        },
        text_auto=True,
    )

    fig.update_layout(
        xaxis_title="Department",
        yaxis_title="Total Support Tickets",
        hovermode="x unified",
    )

    return fig


def create_learning_completion_chart(df: pd.DataFrame) -> go.Figure:
    """Create a department-level learning completion chart."""

    required_columns = {
        "Department",
        "learning_completion_rate",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    department_data = (
        df.groupby("Department", as_index=False)[
            "learning_completion_rate"
        ]
        .mean()
        .sort_values(
            "learning_completion_rate",
            ascending=False,
        )
    )

    fig = px.bar(
        department_data,
        x="Department",
        y="learning_completion_rate",
        title="Learning Completion by Department",
        labels={
            "Department": "Department",
            "learning_completion_rate": (
                "Learning Completion Rate (%)"
            ),
        },
        text_auto=".1f",
    )

    fig.update_layout(
        xaxis_title="Department",
        yaxis_title="Learning Completion Rate (%)",
        yaxis=dict(range=[0, 100]),
        hovermode="x unified",
    )

    return fig


def create_tool_usage_chart(df: pd.DataFrame) -> go.Figure:
    """Create a comparison of internal tool activity."""

    required_columns = {
        "total_slack_activity",
        "total_jira_usage",
        "total_github_activity",
        "total_teams_activity",
        "total_workspace_activity",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    tool_totals = pd.DataFrame(
        {
            "Tool": [
                "Slack",
                "Jira",
                "GitHub",
                "Teams",
                "Workspace",
            ],
            "Activity": [
                df["total_slack_activity"].sum(),
                df["total_jira_usage"].sum(),
                df["total_github_activity"].sum(),
                df["total_teams_activity"].sum(),
                df["total_workspace_activity"].sum(),
            ],
        }
    )

    fig = px.bar(
        tool_totals,
        x="Tool",
        y="Activity",
        title="Internal Tool Activity",
        labels={
            "Tool": "Tool",
            "Activity": "Total Activity",
        },
        text_auto=True,
    )

    fig.update_layout(
        xaxis_title="Tool",
        yaxis_title="Total Activity",
        hovermode="x unified",
    )

    return fig


def create_onboarding_learning_scatter(
    df: pd.DataFrame,
) -> go.Figure:
    """Create a scatter plot comparing onboarding and learning."""

    required_columns = {
        "average_completion_percentage",
        "average_assessment_score",
        "Department",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    fig = px.scatter(
        df,
        x="average_completion_percentage",
        y="average_assessment_score",
        color="Department",
        hover_data=[
            "Employee_Name",
            "Department",
        ],
        title=(
            "Onboarding Completion vs Learning Assessment "
            "Score"
        ),
        labels={
            "average_completion_percentage": (
                "Onboarding Completion (%)"
            ),
            "average_assessment_score": (
                "Average Assessment Score"
            ),
        },
    )

    fig.update_layout(
        xaxis_title="Onboarding Completion (%)",
        yaxis_title="Average Assessment Score",
        hovermode="closest",
    )

    return fig