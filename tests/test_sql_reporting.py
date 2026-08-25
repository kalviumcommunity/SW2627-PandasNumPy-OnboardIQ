import sqlite3

import pytest

from src.database.reporting import (
    get_department_employee_metrics,
    get_department_metrics,
    get_department_onboarding_metrics,
    get_department_support_metrics,
    get_employee_details,
    get_employee_metrics,
    get_employee_onboarding_support,
    get_high_support_employees,
    get_learning_course_metrics,
    get_learning_metrics,
    get_onboarding_metrics,
    get_support_category_metrics,
    get_support_metrics,
    get_tool_activity_by_employee,
    get_tool_usage_metrics,
)


@pytest.fixture
def test_database(monkeypatch):
    """
    Create an in-memory SQLite database matching the
    production reporting schema.
    """

    connection = sqlite3.connect(":memory:")

    connection.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE employees (
            employee_id INTEGER PRIMARY KEY,
            employee_name TEXT NOT NULL,
            department TEXT,
            position TEXT,
            employment_status TEXT,
            salary REAL,
            performance_score TEXT,
            engagement_survey REAL,
            emp_satisfaction INTEGER,
            special_projects_count INTEGER,
            terminated INTEGER
        );

        CREATE TABLE onboarding_tasks (
            onboarding_task_id TEXT PRIMARY KEY,
            employee_id INTEGER NOT NULL,
            task_name TEXT,
            task_category TEXT,
            current_stage TEXT,
            task_status TEXT,
            due_date TEXT,
            completed_date TEXT,
            completion_percentage REAL,
            FOREIGN KEY (employee_id)
                REFERENCES employees(employee_id)
        );

        CREATE TABLE support_tickets (
            ticket_id TEXT PRIMARY KEY,
            employee_id INTEGER NOT NULL,
            created_date TEXT,
            issue_category TEXT,
            priority TEXT,
            resolution_time_hours REAL,
            assigned_team TEXT,
            status TEXT,
            FOREIGN KEY (employee_id)
                REFERENCES employees(employee_id)
        );

        CREATE TABLE learning_records (
            learning_record_id TEXT PRIMARY KEY,
            employee_id INTEGER NOT NULL,
            course_name TEXT,
            course_type TEXT,
            assigned_date TEXT,
            completed_date TEXT,
            assessment_score REAL,
            completion_time_hours REAL,
            course_status TEXT,
            FOREIGN KEY (employee_id)
                REFERENCES employees(employee_id)
        );

        CREATE TABLE tool_usage (
            usage_id TEXT PRIMARY KEY,
            employee_id INTEGER NOT NULL,
            usage_date TEXT,
            slack_activity_count INTEGER,
            jira_usage_count INTEGER,
            github_activity_count INTEGER,
            teams_activity_count INTEGER,
            workspace_activity_count INTEGER,
            daily_active_usage INTEGER NOT NULL,
            FOREIGN KEY (employee_id)
                REFERENCES employees(employee_id)
        );
        """
    )

    employees = [
        (
            1,
            "Alice",
            "IT/IS",
            "Developer",
            "Active",
            60000,
            "Exceeds",
            4.5,
            5,
            2,
            0,
        ),
        (
            2,
            "Bob",
            "IT/IS",
            "Analyst",
            "Active",
            50000,
            "Fully Meets",
            4.0,
            4,
            1,
            0,
        ),
        (
            3,
            "Carol",
            "Production",
            "Operator",
            "Active",
            45000,
            "Fully Meets",
            3.5,
            3,
            0,
            0,
        ),
    ]

    connection.executemany(
        """
        INSERT INTO employees
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        employees,
    )

    onboarding_tasks = [
        (
            "ONB001",
            1,
            "Task 1",
            "HR",
            "Preboarding",
            "Complete",
            "2026-01-10",
            "2026-01-09",
            100,
        ),
        (
            "ONB002",
            1,
            "Task 2",
            "HR",
            "Orientation",
            "Complete",
            "2026-01-11",
            "2026-01-10",
            100,
        ),
        (
            "ONB003",
            1,
            "Task 3",
            "Tools",
            "Training",
            "Overdue",
            "2026-01-12",
            None,
            50,
        ),
        (
            "ONB004",
            2,
            "Task 4",
            "HR",
            "Preboarding",
            "Complete",
            "2026-01-10",
            "2026-01-09",
            100,
        ),
        (
            "ONB005",
            2,
            "Task 5",
            "Tools",
            "Training",
            "In Progress",
            "2026-01-15",
            None,
            50,
        ),
        (
            "ONB006",
            3,
            "Task 6",
            "HR",
            "Preboarding",
            "Blocked",
            "2026-01-15",
            None,
            25,
        ),
    ]

    connection.executemany(
        """
        INSERT INTO onboarding_tasks
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        onboarding_tasks,
    )

    support_tickets = [
        (
            "TKT001",
            1,
            "2026-01-05",
            "Technical",
            "Medium",
            4.0,
            "IT Support",
            "Resolved",
        ),
        (
            "TKT002",
            1,
            "2026-01-06",
            "Access",
            "High",
            None,
            "IT Support",
            "Open",
        ),
        (
            "TKT003",
            2,
            "2026-01-07",
            "Learning",
            "Medium",
            8.0,
            "Learning & Development",
            "Resolved",
        ),
        (
            "TKT004",
            3,
            "2026-01-08",
            "Technical",
            "Critical",
            None,
            "IT Support",
            "Open",
        ),
    ]

    connection.executemany(
        """
        INSERT INTO support_tickets
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        support_tickets,
    )

    learning_records = [
        (
            "LRN001",
            1,
            "Security Training",
            "Compliance",
            "2026-01-01",
            "2026-01-05",
            90,
            5,
            "Completed",
        ),
        (
            "LRN002",
            2,
            "Security Training",
            "Compliance",
            "2026-01-01",
            "2026-01-06",
            80,
            6,
            "Completed",
        ),
        (
            "LRN003",
            3,
            "Python Basics",
            "Technical",
            "2026-01-01",
            None,
            70,
            None,
            "In Progress",
        ),
    ]

    connection.executemany(
        """
        INSERT INTO learning_records
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        learning_records,
    )

    tool_usage = [
        (
            "USE001",
            1,
            "2026-01-01",
            20,
            15,
            12,
            8,
            10,
            10,
        ),
        (
            "USE002",
            2,
            "2026-01-01",
            15,
            12,
            10,
            7,
            9,
            8,
        ),
        (
            "USE003",
            3,
            "2026-01-01",
            10,
            8,
            7,
            5,
            6,
            6,
        ),
    ]

    connection.executemany(
        """
        INSERT INTO tool_usage
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        tool_usage,
    )

    connection.commit()

    monkeypatch.setattr(
        "src.database.reporting.get_connection",
        lambda: connection,
    )

    yield connection

    connection.close()


# ============================================================
# EMPLOYEE TESTS
# ============================================================

def test_employee_metrics(test_database):
    result = get_employee_metrics()

    assert len(result) == 1
    assert result.loc[0, "total_employees"] == 3
    assert result.loc[0, "active_employees"] == 3
    assert result.loc[0, "terminated_employees"] == 0


def test_department_metrics(test_database):
    result = get_department_metrics()

    assert len(result) == 2
    assert set(result["department"]) == {
        "IT/IS",
        "Production",
    }

    it_is = result[
        result["department"] == "IT/IS"
    ]

    assert it_is.iloc[0]["employee_count"] == 2


# ============================================================
# ONBOARDING TESTS
# ============================================================

def test_onboarding_metrics(test_database):
    result = get_onboarding_metrics()

    assert result.loc[0, "total_employees"] == 3
    assert result.loc[0, "total_onboarding_tasks"] == 6
    assert (
        result.loc[0, "completed_onboarding_tasks"]
        == 3
    )
    assert (
        result.loc[0, "delayed_or_blocked_tasks"]
        == 2
    )


def test_department_onboarding_metrics(test_database):
    result = get_department_onboarding_metrics()

    assert len(result) == 2
    assert "completion_rate" in result.columns


# ============================================================
# SUPPORT TESTS
# ============================================================

def test_support_metrics(test_database):
    result = get_support_metrics()

    assert result.loc[0, "total_support_tickets"] == 4
    assert result.loc[0, "open_support_tickets"] == 2
    assert (
        result.loc[0, "resolved_support_tickets"]
        == 2
    )


def test_department_support_metrics(test_database):
    result = get_department_support_metrics()

    assert len(result) == 2
    assert "total_tickets" in result.columns


def test_high_support_filter(test_database):
    result = get_high_support_employees(
        minimum_tickets=2
    )

    assert len(result) == 1
    assert result.iloc[0]["employee_id"] == 1


def test_negative_support_threshold_raises_error(
    test_database,
):
    with pytest.raises(ValueError):
        get_high_support_employees(
            minimum_tickets=-1
        )


# ============================================================
# LEARNING TESTS
# ============================================================

def test_learning_metrics(test_database):
    result = get_learning_metrics()

    assert result.loc[0, "total_learning_records"] == 3
    assert (
        result.loc[0, "completed_learning_records"]
        == 2
    )


def test_learning_course_metrics(test_database):
    result = get_learning_course_metrics()

    assert len(result) == 2
    assert "completion_rate" in result.columns


# ============================================================
# TOOL USAGE TESTS
# ============================================================

def test_tool_usage_metrics(test_database):
    result = get_tool_usage_metrics()

    assert result.loc[0, "total_usage_records"] == 3


def test_tool_activity_by_employee(test_database):
    result = get_tool_activity_by_employee()

    assert len(result) == 3
    assert "average_daily_active_usage" in result.columns


# ============================================================
# CROSS-DOMAIN TESTS
# ============================================================

def test_employee_onboarding_support(test_database):
    result = get_employee_onboarding_support()

    assert len(result) == 3

    assert (
        "support_ticket_count"
        in result.columns
    )

    assert (
        "onboarding_task_count"
        in result.columns
    )


def test_department_filter(test_database):
    result = get_department_employee_metrics(
        "IT/IS"
    )

    assert len(result) == 2

    assert (
        result["department"] == "IT/IS"
    ).all()


def test_empty_department_raises_error(test_database):
    with pytest.raises(ValueError):
        get_department_employee_metrics("")


def test_employee_details(test_database):
    result = get_employee_details()

    assert len(result) == 3

    assert (
        "onboarding_task_count"
        in result.columns
    )

    assert (
        "learning_record_count"
        in result.columns
    )

    assert (
        "support_ticket_count"
        in result.columns
    )


def test_support_category_metrics(test_database):
    result = get_support_category_metrics()

    assert len(result) == 3
    assert "total_tickets" in result.columns