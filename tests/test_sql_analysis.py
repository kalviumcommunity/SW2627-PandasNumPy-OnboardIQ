import sqlite3

import pandas as pd
import pytest

from src.analysis.sql_analysis import (
    employee_multi_table_summary,
    employee_onboarding_summary,
    employee_ranking_by_department,
)
from src.database.database import (
    create_analytical_indexes,
    create_analytical_views,
    get_connection,
    get_index_names,
    get_view_names,
    initialize_database,
)


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture(scope="module", autouse=True)
def prepare_database():
    """
    Ensure the database schema, analytical indexes,
    and analytical views exist before tests run.
    """

    initialize_database()
    create_analytical_indexes()
    create_analytical_views()

    yield


# ============================================================
# MULTI-TABLE JOIN TESTS
# ============================================================

def test_employee_onboarding_summary_returns_all_employees():
    """
    The employee-level onboarding summary should preserve
    the employee dimension and return one row per employee.
    """

    result = employee_onboarding_summary()

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 311

    assert "employee_id" in result.columns
    assert "department" in result.columns
    assert "total_onboarding_tasks" in result.columns
    assert "completed_onboarding_tasks" in result.columns


def test_employee_multi_table_summary_returns_all_employees():
    """
    The multi-table analytical query should return one row
    per employee.
    """

    result = employee_multi_table_summary()

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 311

    assert result["employee_id"].is_unique

    required_columns = {
        "employee_id",
        "department",
        "total_onboarding_tasks",
        "completed_onboarding_tasks",
        "onboarding_completion_rate",
        "total_learning_records",
        "completed_courses",
        "learning_completion_rate",
        "total_usage_records",
        "total_support_tickets",
        "open_support_tickets",
    }

    assert required_columns.issubset(result.columns)


# ============================================================
# WINDOW FUNCTION TESTS
# ============================================================

def test_department_ranking_uses_window_function():
    """
    Department ranking should generate a rank for every
    employee and restart ranking within each department.
    """

    result = employee_ranking_by_department()

    assert isinstance(result, pd.DataFrame)

    assert len(result) == 311

    assert "employee_id" in result.columns
    assert "department" in result.columns
    assert "department_rank" in result.columns

    assert result["department_rank"].notna().all()

    assert (
        pd.api.types.is_integer_dtype(
            result["department_rank"]
        )
    )


def test_department_ranking_starts_at_one():
    """
    Every department should have a top-ranked employee
    with rank 1.
    """

    result = employee_ranking_by_department()

    minimum_ranks = (
        result.groupby("department")["department_rank"]
        .min()
    )

    assert (minimum_ranks == 1).all()


# ============================================================
# INDEX TESTS
# ============================================================

def test_analytical_indexes_exist():
    """
    Analytical foreign-key indexes should exist.
    """

    indexes = get_index_names()

    expected_indexes = {
        "idx_onboarding_tasks_employee_id",
        "idx_learning_records_employee_id",
        "idx_tool_usage_employee_id",
        "idx_support_tickets_employee_id",
    }

    assert expected_indexes.issubset(
        set(indexes)
    )


# ============================================================
# QUERY PLAN TEST
# ============================================================

def test_onboarding_join_uses_employee_index():
    """
    EXPLAIN QUERY PLAN should demonstrate that the onboarding
    employee_id index is used for the analytical join.
    """

    connection = get_connection()

    try:
        query = """
            SELECT
                e.employee_id,
                e.department,
                AVG(o.completion_percentage)
                    AS onboarding_completion_rate

            FROM employees AS e

            INNER JOIN onboarding_tasks AS o
                ON e.employee_id = o.employee_id

            GROUP BY
                e.employee_id,
                e.department
        """

        plan = connection.execute(
            "EXPLAIN QUERY PLAN " + query
        ).fetchall()

    finally:
        connection.close()

    plan_text = " ".join(
        row[3]
        for row in plan
    )

    assert (
        "idx_onboarding_tasks_employee_id"
        in plan_text
    )


# ============================================================
# VIEW TESTS
# ============================================================

def test_analytical_views_exist():
    """
    Required analytical views should exist.
    """

    views = get_view_names()

    expected_views = {
        "vw_employee_onboarding_summary",
        "vw_employee_analytics_summary",
    }

    assert expected_views.issubset(
        set(views)
    )


def test_onboarding_view_has_one_row_per_employee():
    """
    The onboarding view should maintain employee-level grain.
    """

    connection = get_connection()

    try:
        result = pd.read_sql_query(
            """
            SELECT *
            FROM vw_employee_onboarding_summary
            """,
            connection,
        )

    finally:
        connection.close()

    assert len(result) == 311

    assert result["employee_id"].is_unique


def test_analytics_view_has_one_row_per_employee():
    """
    The complete analytical view should maintain employee-level
    grain despite multiple one-to-many joins.
    """

    connection = get_connection()

    try:
        result = pd.read_sql_query(
            """
            SELECT *
            FROM vw_employee_analytics_summary
            """,
            connection,
        )

    finally:
        connection.close()

    assert len(result) == 311

    assert result["employee_id"].is_unique


# ============================================================
# SQL RESULT VALIDATION
# ============================================================

def test_sql_view_matches_existing_onboarding_analysis():
    """
    Validate the SQL onboarding view against the existing
    Python-generated employee onboarding analysis.
    """

    sql_result = employee_onboarding_summary()

    connection = get_connection()

    try:
        view_result = pd.read_sql_query(
            """
            SELECT
                employee_id,
                department,
                position,
                total_onboarding_tasks,
                completed_onboarding_tasks,
                average_completion_percentage
            FROM vw_employee_onboarding_summary
            ORDER BY employee_id
            """,
            connection,
        )

    finally:
        connection.close()

    sql_result = (
        sql_result
        .sort_values("employee_id")
        .reset_index(drop=True)
    )

    view_result = (
        view_result
        .sort_values("employee_id")
        .reset_index(drop=True)
    )

    pd.testing.assert_frame_equal(
        sql_result,
        view_result,
        check_dtype=False,
        check_exact=False,
        rtol=1e-9,
        atol=1e-9,
    )


# ============================================================
# DATABASE INTEGRITY TEST
# ============================================================

def test_foreign_keys_are_enabled():
    """
    The project database connection should enforce foreign keys.
    """

    connection = get_connection()

    try:
        result = connection.execute(
            "PRAGMA foreign_keys"
        ).fetchone()[0]

    finally:
        connection.close()

    assert result == 1