from __future__ import annotations

import sqlite3

import pandas as pd

from src.database.database import get_connection


# ============================================================
# SQL ANALYSIS
# ============================================================


def _read_sql(
    query: str,
    connection: sqlite3.Connection | None = None,
) -> pd.DataFrame:
    """
    Execute a SQL query and return the result as a DataFrame.

    If no connection is supplied, a project database
    connection is created and closed automatically.
    """

    if connection is not None:
        return pd.read_sql_query(
            query,
            connection,
        )

    connection = get_connection()

    try:
        return pd.read_sql_query(
            query,
            connection,
        )
    finally:
        connection.close()


# ============================================================
# EMPLOYEE ONBOARDING SUMMARY
# ============================================================


def employee_onboarding_summary() -> pd.DataFrame:
    """
    Return one onboarding-analysis row per employee.

    Uses an INNER JOIN between employees and onboarding_tasks
    and aggregates onboarding task records at employee level.

    The employee dimension is preserved by using a LEFT JOIN
    so that employees without onboarding records are still
    represented in the analytical result.
    """

    query = """
        SELECT
            e.employee_id,
            e.department,
            e.position,

            COUNT(o.onboarding_task_id)
                AS total_onboarding_tasks,

            SUM(
                CASE
                    WHEN o.task_status = 'Complete'
                    THEN 1
                    ELSE 0
                END
            ) AS completed_onboarding_tasks,

            AVG(o.completion_percentage)
                AS average_completion_percentage

        FROM employees AS e

        LEFT JOIN onboarding_tasks AS o
            ON e.employee_id = o.employee_id

        GROUP BY
            e.employee_id,
            e.department,
            e.position

        ORDER BY
            e.employee_id
    """

    return _read_sql(query)


# ============================================================
# MULTI-TABLE EMPLOYEE ANALYTICS
# ============================================================


def employee_multi_table_summary() -> pd.DataFrame:
    """
    Return one analytical row per employee using all
    operational datasets.

    The query combines:

    employees
    onboarding_tasks
    learning_records
    tool_usage
    support_tickets

    Each one-to-many dataset is aggregated independently
    before being joined to the employee dimension.

    This prevents row multiplication caused by directly
    joining several one-to-many tables together.
    """

    query = """
        WITH onboarding AS (
            SELECT
                employee_id,

                COUNT(*) AS total_onboarding_tasks,

                SUM(
                    CASE
                        WHEN task_status = 'Complete'
                        THEN 1
                        ELSE 0
                    END
                ) AS completed_onboarding_tasks,

                AVG(completion_percentage)
                    AS onboarding_completion_rate

            FROM onboarding_tasks

            GROUP BY employee_id
        ),

        learning AS (
            SELECT
                employee_id,

                COUNT(*) AS total_learning_records,

                SUM(
                    CASE
                        WHEN course_status = 'Completed'
                        THEN 1
                        ELSE 0
                    END
                ) AS completed_courses,

                CASE
                    WHEN COUNT(*) > 0
                    THEN
                        100.0
                        * SUM(
                            CASE
                                WHEN course_status = 'Completed'
                                THEN 1
                                ELSE 0
                            END
                        )
                        / COUNT(*)
                    ELSE 0
                END AS learning_completion_rate

            FROM learning_records

            GROUP BY employee_id
        ),

        usage AS (
            SELECT
                employee_id,

                COUNT(*) AS total_usage_records,

                AVG(
                    daily_active_usage
                ) AS average_daily_active_usage

            FROM tool_usage

            GROUP BY employee_id
        ),

        support AS (
            SELECT
                employee_id,

                COUNT(*) AS total_support_tickets,

                SUM(
                    CASE
                        WHEN status IN (
                            'Open',
                            'In Progress'
                        )
                        THEN 1
                        ELSE 0
                    END
                ) AS open_support_tickets,

                AVG(
                    resolution_time_hours
                ) AS average_resolution_time_hours

            FROM support_tickets

            GROUP BY employee_id
        )

        SELECT
            e.employee_id,
            e.department,

            COALESCE(
                o.total_onboarding_tasks,
                0
            ) AS total_onboarding_tasks,

            COALESCE(
                o.completed_onboarding_tasks,
                0
            ) AS completed_onboarding_tasks,

            COALESCE(
                o.onboarding_completion_rate,
                0
            ) AS onboarding_completion_rate,

            COALESCE(
                l.total_learning_records,
                0
            ) AS total_learning_records,

            COALESCE(
                l.completed_courses,
                0
            ) AS completed_courses,

            COALESCE(
                l.learning_completion_rate,
                0
            ) AS learning_completion_rate,

            COALESCE(
                u.total_usage_records,
                0
            ) AS total_usage_records,

            COALESCE(
                u.average_daily_active_usage,
                0
            ) AS average_daily_active_usage,

            COALESCE(
                s.total_support_tickets,
                0
            ) AS total_support_tickets,

            COALESCE(
                s.open_support_tickets,
                0
            ) AS open_support_tickets,

            s.average_resolution_time_hours

        FROM employees AS e

        LEFT JOIN onboarding AS o
            ON e.employee_id = o.employee_id

        LEFT JOIN learning AS l
            ON e.employee_id = l.employee_id

        LEFT JOIN usage AS u
            ON e.employee_id = u.employee_id

        LEFT JOIN support AS s
            ON e.employee_id = s.employee_id

        ORDER BY
            e.employee_id
    """

    return _read_sql(query)


# ============================================================
# WINDOW FUNCTION — DEPARTMENT RANKING
# ============================================================


def employee_ranking_by_department() -> pd.DataFrame:
    """
    Rank employees within each department.

    The ranking uses a SQL window function:

        RANK() OVER (
            PARTITION BY department
            ORDER BY salary DESC
        )

    Employees are therefore ranked against other employees
    in the same department.

    Ties receive the same rank, which is the intended
    behaviour of SQL RANK().
    """

    query = """
        SELECT
            employee_id,
            department,
            salary,

            RANK() OVER (
                PARTITION BY department
                ORDER BY salary DESC
            ) AS department_rank

        FROM employees

        ORDER BY
            department,
            department_rank,
            employee_id
    """

    result = _read_sql(query)

    # SQLite normally returns the window-function rank as
    # an integer. Explicit conversion makes the public
    # Python API consistent and satisfies the analytical
    # contract of this function.
    result["department_rank"] = (
        result["department_rank"].astype("int64")
    )

    return result