"""Reusable Plotly business visualizations for OnboardIQ."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def onboarding_completion_chart(
    dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Create a bar chart showing average onboarding completion
    rate by department.
    """
    required_columns = {
        "Department",
        "onboarding_completion_rate",
    }

    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    department_data = (
        dataframe.groupby("Department", as_index=False)[
            "onboarding_completion_rate"
        ]
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
        title="Onboarding Completion Rate by Department",
        labels={
            "Department": "Department",
            "onboarding_completion_rate": "Completion Rate (%)",
        },
        text_auto=".1f",
    )

    figure.update_layout(
        yaxis_range=[0, 100],
        hovermode="x unified",
    )

    return figure


def productivity_by_department_chart(
    dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Create a bar chart showing average productivity-related
    metrics by department.
    """
    required_columns = {
        "Department",
        "average_daily_active_usage",
        "EngagementSurvey",
    }

    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    department_data = (
        dataframe.groupby("Department", as_index=False)[
            [
                "average_daily_active_usage",
                "EngagementSurvey",
            ]
        ]
        .mean()
    )

    figure = px.bar(
        department_data,
        x="Department",
        y=[
            "average_daily_active_usage",
            "EngagementSurvey",
        ],
        barmode="group",
        title="Productivity and Engagement by Department",
        labels={
            "value": "Average Value",
            "variable": "Metric",
            "Department": "Department",
        },
    )

    figure.update_layout(
        hovermode="x unified",
    )

    return figure


def support_ticket_chart(
    dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Create a department-level chart showing support-ticket volume.
    """
    required_columns = {
        "Department",
        "total_support_tickets",
    }

    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    department_data = (
        dataframe.groupby("Department", as_index=False)[
            "total_support_tickets"
        ]
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
            "total_support_tickets": "Total Support Tickets",
        },
        text_auto=True,
    )

    figure.update_layout(
        hovermode="x unified",
    )

    return figure


def learning_completion_chart(
    dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Create a department-level chart showing learning completion.
    """
    required_columns = {
        "Department",
        "learning_completion_rate",
    }

    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    department_data = (
        dataframe.groupby("Department", as_index=False)[
            "learning_completion_rate"
        ]
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
        title="Learning Completion Rate by Department",
        labels={
            "Department": "Department",
            "learning_completion_rate": "Learning Completion Rate (%)",
        },
        text_auto=".1f",
    )

    figure.update_layout(
        yaxis_range=[0, 100],
        hovermode="x unified",
    )

    return figure


def onboarding_vs_learning_chart(
    dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Compare onboarding completion and learning completion
    for each department.
    """
    required_columns = {
        "Department",
        "onboarding_completion_rate",
        "learning_completion_rate",
    }

    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    department_data = (
        dataframe.groupby("Department", as_index=False)[
            [
                "onboarding_completion_rate",
                "learning_completion_rate",
            ]
        ]
        .mean()
    )

    figure = go.Figure()

    figure.add_trace(
        go.Bar(
            x=department_data["Department"],
            y=department_data["onboarding_completion_rate"],
            name="Onboarding Completion",
        )
    )

    figure.add_trace(
        go.Bar(
            x=department_data["Department"],
            y=department_data["learning_completion_rate"],
            name="Learning Completion",
        )
    )

    figure.update_layout(
        title="Onboarding vs Learning Completion",
        xaxis_title="Department",
        yaxis_title="Completion Rate (%)",
        barmode="group",
        yaxis_range=[0, 100],
        hovermode="x unified",
    )

    return figure