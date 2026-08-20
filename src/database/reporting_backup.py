"""
SQL reporting and business metrics for OnboardIQ.

This module provides reusable SQLite queries for:
- Employee metrics
- Onboarding metrics
- Learning metrics
- Tool usage metrics
- Support ticket metrics
- Department-level reporting
- Employee filtering
- SQL-based business metrics
- CSV export of report results
"""

from pathlib import Path

import pandas as pd

from src.database.database import get_connection


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_REPORT_DIRECTORY = (
    PROJECT_ROOT / "data" / "processed" / "sql_reports"
)


# ============================================================
# EMPLOYEE METRICS
# ============================================================

EMPLOYEE_METRICS_QUERY = """
SELECT
    COUNT(*) AS total_employees,

    SUM(
        CASE
            WHEN employment_status = 'Active'
            THEN 1
            ELSE 0
        END
    ) AS active_employees,

    SUM(
        CASE
            WHEN terminated = 1
            THEN 1
            ELSE 0
        END
    ) AS terminated_employees,

    ROUND(
        AVG(salary),
        2
    ) AS average_salary,

    ROUND(
        AVG(engagement_survey),
        2
    ) AS average_engagement_score,

    ROUND(
        AVG(emp_satisfaction),
        2
    ) AS average_satisfaction_score,

    ROUND(
        AVG(special_projects_count),
        2
    ) AS average_special_projects

FROM employees;
"""


# ============================================================
# ONBOARDING METRICS
# ============================================================

ONBOARDING_METRICS_QUERY = """
SELECT
    COUNT(DISTINCT e.employee_id) AS total_employees,

    COUNT(
        DISTINCT CASE
            WHEN o.task_status = 'Complete'
            THEN e.employee_id
        END
    ) AS employees_with_completed_tasks,

    ROUND(
        100.0 *
        COUNT(
            DISTINCT CASE
                WHEN o.task_status = 'Complete'
                THEN e.employee_id
            END
        )
        / NULLIF(COUNT(DISTINCT e.employee_id), 0),
        2
    ) AS onboarding_completion_rate,

    COUNT(o.onboarding_task_id) AS total_onboarding_tasks,

    SUM(
        CASE
            WHEN o.task_status = 'Complete'
            THEN 1
            ELSE 0
        END
    ) AS completed_onboarding_tasks,

    SUM(
        CASE
            WHEN o.task_status IN ('Blocked', 'Overdue')
            THEN 1
            ELSE 0
        END
    ) AS delayed_or_blocked_tasks,

    ROUND(
        AVG(o.completion_percentage),
        2
    ) AS average_task_completion_percentage

FROM employees AS e

LEFT JOIN onboarding_tasks AS o
    ON e.employee_id = o.employee_id;
"""


# ============================================================
# LEARNING METRICS
# ============================================================

LEARNING_METRICS_QUERY = """
SELECT
    COUNT(DISTINCT e.employee_id) AS total_employees,

    COUNT(l.learning_record_id) AS total_learning_records,

    SUM(
        CASE
            WHEN l.course_status = 'Completed'
            THEN 1
            ELSE 0
        END
    ) AS completed_learning_records,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN l.course_status = 'Completed'
                THEN 1
                ELSE 0
            END
        )
        / NULLIF(COUNT(l.learning_record_id), 0),
        2
    ) AS learning_completion_rate,

    ROUND(
        AVG(l.assessment_score),
        2
    ) AS average_assessment_score,

    ROUND(
        AVG(l.completion_time_hours),
        2
    ) AS average_completion_time_hours

FROM employees AS e

LEFT JOIN learning_records AS l
    ON e.employee_id = l.employee_id;
"""


# ============================================================
# TOOL USAGE METRICS
# ============================================================

TOOL_USAGE_METRICS_QUERY = """
SELECT
    COUNT(DISTINCT e.employee_id) AS total_employees,

    COUNT(t.usage_id) AS total_usage_records,

    ROUND(
        AVG(t.daily_active_usage),
        2
    ) AS average_daily_active_usage,

    ROUND(
        AVG(t.slack_activity_count),
        2
    ) AS average_slack_activity,

    ROUND(
        AVG(t.jira_usage_count),
        2
    ) AS average_jira_usage,

    ROUND(
        AVG(t.github_activity_count),
        2
    ) AS average_github_activity,

    ROUND(
        AVG(t.teams_activity_count),
        2
    ) AS average_teams_activity,

    ROUND(
        AVG(t.workspace_activity_count),
        2
    ) AS average_workspace_activity

FROM employees AS e

LEFT JOIN tool_usage AS t
    ON e.employee_id = t.employee_id;
"""


# ============================================================
# SUPPORT TICKET METRICS
# ============================================================

SUPPORT_METRICS_QUERY = """
SELECT
    COUNT(DISTINCT e.employee_id) AS total_employees,

    COUNT(s.ticket_id) AS total_support_tickets,

    SUM(
        CASE
            WHEN s.status = 'Open'
            THEN 1
            ELSE 0
        END
    ) AS open_support_tickets,

    SUM(
        CASE
            WHEN s.status = 'Resolved'
            THEN 1
            ELSE 0
        END
    ) AS resolved_support_tickets,

    ROUND(
        AVG(s.resolution_time_hours),
        2
    ) AS average_resolution_time_hours,

    SUM(
        CASE
            WHEN s.priority = 'Critical'
            THEN 1
            ELSE 0
        END
    ) AS critical_support_tickets,

    SUM(
        CASE
            WHEN s.priority = 'High'
            THEN 1
            ELSE 0
        END
    ) AS high_priority_support_tickets

FROM employees AS e

LEFT JOIN support_tickets AS s
    ON e.employee_id = s.employee_id;
"""


# ============================================================
# DEPARTMENT METRICS
# ============================================================

DEPARTMENT_METRICS_QUERY = """
SELECT
    TRIM(e.department) AS department,

    COUNT(DISTINCT e.employee_id) AS employee_count,

    ROUND(
        AVG(e.salary),
        2
    ) AS average_salary,

    ROUND(
        AVG(e.engagement_survey),
        2
    ) AS average_engagement_score,

    ROUND(
        AVG(e.emp_satisfaction),
        2
    ) AS average_satisfaction_score,

    ROUND(
        AVG(o.completion_percentage),
        2
    ) AS average_onboarding_completion,

    ROUND(
        AVG(l.assessment_score),
        2
    ) AS average_learning_assessment_score,

    COUNT(DISTINCT s.ticket_id) AS support_ticket_count,

    ROUND(
        AVG(s.resolution_time_hours),
        2
    ) AS average_resolution_time_hours,

    COUNT(DISTINCT t.usage_id) AS tool_usage_records

FROM employees AS e

LEFT JOIN onboarding_tasks AS o
    ON e.employee_id = o.employee_id

LEFT JOIN learning_records AS l
    ON e.employee_id = l.employee_id

LEFT JOIN support_tickets AS s
    ON e.employee_id = s.employee_id

LEFT JOIN tool_usage AS t
    ON e.employee_id = t.employee_id

GROUP BY TRIM(e.department)

ORDER BY employee_count DESC;
"""


# ============================================================
# EMPLOYEE DETAIL REPORT
# ============================================================

EMPLOYEE_DETAIL_QUERY = """
SELECT
    e.employee_id,
    TRIM(e.employee_name) AS employee_name,
    TRIM(e.department) AS department,
    e.position,
    e.employment_status,
    e.performance_score,
    e.engagement_survey,
    e.emp_satisfaction,

    COUNT(DISTINCT o.onboarding_task_id)
        AS onboarding_task_count,

    ROUND(
        AVG(o.completion_percentage),
        2
    ) AS onboarding_completion_percentage,

    COUNT(
        DISTINCT CASE
            WHEN o.task_status IN ('Blocked', 'Overdue')
            THEN o.onboarding_task_id
        END
    ) AS delayed_or_blocked_tasks,

    COUNT(DISTINCT l.learning_record_id)
        AS learning_record_count,

    COUNT(
        DISTINCT CASE
            WHEN l.course_status = 'Completed'
            THEN l.learning_record_id
        END
    ) AS completed_learning_records,

    ROUND(
        AVG(l.assessment_score),
        2
    ) AS average_assessment_score,

    COUNT(DISTINCT t.usage_id)
        AS tool_usage_records,

    ROUND(
        AVG(t.daily_active_usage),
        2
    ) AS average_daily_active_usage,

    COUNT(DISTINCT s.ticket_id)
        AS support_ticket_count,

    SUM(
        CASE
            WHEN s.status = 'Open'
            THEN 1
            ELSE 0
        END
    ) AS open_support_tickets,

    ROUND(
        AVG(s.resolution_time_hours),
        2
    ) AS average_resolution_time_hours

FROM employees AS e

LEFT JOIN onboarding_tasks AS o
    ON e.employee_id = o.employee_id

LEFT JOIN learning_records AS l
    ON e.employee_id = l.employee_id

LEFT JOIN tool_usage AS t
    ON e.employee_id = t.employee_id

LEFT JOIN support_tickets AS s
    ON e.employee_id = s.employee_id

GROUP BY
    e.employee_id,
    e.employee_name,
    e.department,
    e.position,
    e.employment_status,
    e.performance_score,
    e.engagement_survey,
    e.emp_satisfaction

ORDER BY e.employee_id;
"""


# ============================================================
# DEPARTMENT EMPLOYEE FILTER
# ============================================================

DEPARTMENT_EMPLOYEE_QUERY = """
SELECT
    e.employee_id,
    TRIM(e.employee_name) AS employee_name,
    TRIM(e.department) AS department,
    e.position,
    e.employment_status,
    e.performance_score,
    e.engagement_survey,
    e.emp_satisfaction

FROM employees AS e

WHERE TRIM(e.department) = ?

ORDER BY
    TRIM(e.employee_name);
"""


# ============================================================
# PERFORMANCE FILTER
# ============================================================

PERFORMANCE_FILTER_QUERY = """
SELECT
    e.employee_id,
    TRIM(e.employee_name) AS employee_name,
    TRIM(e.department) AS department,
    e.performance_score,
    e.engagement_survey,
    e.emp_satisfaction

FROM employees AS e

WHERE e.performance_score = ?

ORDER BY
    TRIM(e.department),
    TRIM(e.employee_name);
"""


# ============================================================
# SUPPORT CATEGORY METRICS
# ============================================================

SUPPORT_CATEGORY_METRICS_QUERY = """
SELECT
    s.issue_category,

    COUNT(s.ticket_id) AS ticket_count,

    SUM(
        CASE
            WHEN s.status = 'Open'
            THEN 1
            ELSE 0
        END
    ) AS open_ticket_count,

    SUM(
        CASE
            WHEN s.status = 'Resolved'
            THEN 1
            ELSE 0
        END
    ) AS resolved_ticket_count,

    ROUND(
        AVG(s.resolution_time_hours),
        2
    ) AS average_resolution_time_hours

FROM support_tickets AS s

GROUP BY s.issue_category

ORDER BY ticket_count DESC;
"""


# ============================================================
# LEARNING COURSE METRICS
# ============================================================

LEARNING_COURSE_METRICS_QUERY = """
SELECT
    l.course_type,

    COUNT(l.learning_record_id) AS assigned_records,

    SUM(
        CASE
            WHEN l.course_status = 'Completed'
            THEN 1
            ELSE 0
        END
    ) AS completed_records,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN l.course_status = 'Completed'
                THEN 1
                ELSE 0
            END
        )
        / NULLIF(COUNT(l.learning_record_id), 0),
        2
    ) AS completion_rate,

    ROUND(
        AVG(l.assessment_score),
        2
    ) AS average_assessment_score

FROM learning_records AS l

GROUP BY l.course_type

ORDER BY assigned_records DESC;
"""


# ============================================================
# TOOL ACTIVITY BY EMPLOYEE
# ============================================================

TOOL_ACTIVITY_BY_EMPLOYEE_QUERY = """
SELECT
    e.employee_id,
    TRIM(e.employee_name) AS employee_name,
    TRIM(e.department) AS department,

    COUNT(t.usage_id) AS usage_record_count,

    ROUND(
        AVG(t.daily_active_usage),
        2
    ) AS average_daily_active_usage,

    SUM(t.slack_activity_count) AS total_slack_activity,

    SUM(t.jira_usage_count) AS total_jira_usage,

    SUM(t.github_activity_count) AS total_github_activity,

    SUM(t.teams_activity_count) AS total_teams_activity,

    SUM(t.workspace_activity_count) AS total_workspace_activity

FROM employees AS e

LEFT JOIN tool_usage AS t
    ON e.employee_id = t.employee_id

GROUP BY
    e.employee_id,
    e.employee_name,
    e.department

ORDER BY
    average_daily_active_usage DESC;
"""


# ============================================================
# QUERY EXECUTION HELPER
# ============================================================

def _execute_query(query, parameters=None):
    """
    Execute a SQL query and return a pandas DataFrame.
    """

    connection = get_connection()

    try:
        return pd.read_sql_query(
            query,
            connection,
            params=parameters or (),
        )

    finally:
        connection.close()


# ============================================================
# PUBLIC REPORT FUNCTIONS
# ============================================================

def get_employee_metrics():
    """Return organization-level employee metrics."""
    return _execute_query(EMPLOYEE_METRICS_QUERY)


def get_onboarding_metrics():
    """Return organization-level onboarding metrics."""
    return _execute_query(ONBOARDING_METRICS_QUERY)


def get_learning_metrics():
    """Return organization-level learning metrics."""
    return _execute_query(LEARNING_METRICS_QUERY)


def get_tool_usage_metrics():
    """Return organization-level tool usage metrics."""
    return _execute_query(TOOL_USAGE_METRICS_QUERY)


def get_support_metrics():
    """Return organization-level support metrics."""
    return _execute_query(SUPPORT_METRICS_QUERY)


def get_department_metrics():
    """Return department-level business metrics."""
    return _execute_query(DEPARTMENT_METRICS_QUERY)


def get_employee_details():
    """Return employee-level consolidated reporting data."""
    return _execute_query(EMPLOYEE_DETAIL_QUERY)


def get_employees_by_department(department):
    """
    Return employees belonging to a department.

    Parameters
    ----------
    department : str
        Department name.
    """

    if not department or not str(department).strip():
        raise ValueError("department must not be empty")

    return _execute_query(
        DEPARTMENT_EMPLOYEE_QUERY,
        (str(department).strip(),),
    )


def get_employees_by_performance(performance_score):
    """
    Return employees matching a performance score.
    """

    if performance_score is None:
        raise ValueError("performance_score must not be None")

    return _execute_query(
        PERFORMANCE_FILTER_QUERY,
        (performance_score,),
    )


def get_support_category_metrics():
    """Return support ticket metrics grouped by issue category."""
    return _execute_query(SUPPORT_CATEGORY_METRICS_QUERY)


def get_learning_course_metrics():
    """Return learning metrics grouped by course type."""
    return _execute_query(LEARNING_COURSE_METRICS_QUERY)


def get_tool_activity_by_employee():
    """Return tool usage aggregated at employee level."""
    return _execute_query(TOOL_ACTIVITY_BY_EMPLOYEE_QUERY)


# ============================================================
# EXPORT REPORTS
# ============================================================

def export_sql_reports(output_directory=DEFAULT_REPORT_DIRECTORY):
    """
    Execute all standard SQL reports and save them as CSV files.

    Returns
    -------
    dict
        Dictionary mapping report names to DataFrames.
    """

    output_directory = Path(output_directory)
    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    reports = {
        "employee_metrics": get_employee_metrics(),
        "onboarding_metrics": get_onboarding_metrics(),
        "learning_metrics": get_learning_metrics(),
        "tool_usage_metrics": get_tool_usage_metrics(),
        "support_metrics": get_support_metrics(),
        "department_metrics": get_department_metrics(),
        "employee_details": get_employee_details(),
        "support_category_metrics": get_support_category_metrics(),
        "learning_course_metrics": get_learning_course_metrics(),
        "tool_activity_by_employee": get_tool_activity_by_employee(),
    }

    for report_name, dataframe in reports.items():
        output_path = output_directory / f"{report_name}.csv"

        dataframe.to_csv(
            output_path,
            index=False,
        )

    return reports


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    reports = export_sql_reports(
        DEFAULT_REPORT_DIRECTORY
    )

    print("\nSQL reporting completed successfully.")
    print(f"Reports exported to: {DEFAULT_REPORT_DIRECTORY}")

    print("\nGenerated reports:")

    for report_name, dataframe in reports.items():
        print(
            f"- {report_name}: "
            f"{len(dataframe)} row(s)"
        )