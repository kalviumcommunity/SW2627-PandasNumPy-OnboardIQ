from pathlib import Path
from typing import Optional, Sequence

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
# QUERY EXECUTION
# ============================================================

def _execute_query(
    query: str,
    parameters: Optional[Sequence] = None,
) -> pd.DataFrame:
    """
    Execute a SQL query and return the result as a DataFrame.

    The connection lifecycle is intentionally managed by the
    database layer. This keeps the function compatible with
    both normal SQLite connections and test fixtures that
    provide an in-memory connection.
    """
    connection = get_connection()

    return pd.read_sql_query(
        query,
        connection,
        params=parameters or (),
    )


# ============================================================
# 1. EMPLOYEE METRICS
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


def get_employee_metrics() -> pd.DataFrame:
    """Return organization-level employee metrics."""
    return _execute_query(EMPLOYEE_METRICS_QUERY)


# ============================================================
# 2. ONBOARDING METRICS
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


def get_onboarding_metrics() -> pd.DataFrame:
    """Return organization-level onboarding metrics."""
    return _execute_query(ONBOARDING_METRICS_QUERY)


# ============================================================
# 3. LEARNING METRICS
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


def get_learning_metrics() -> pd.DataFrame:
    """Return organization-level learning metrics."""
    return _execute_query(LEARNING_METRICS_QUERY)


# ============================================================
# 4. TOOL USAGE METRICS
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


def get_tool_usage_metrics() -> pd.DataFrame:
    """Return organization-level internal tool usage metrics."""
    return _execute_query(TOOL_USAGE_METRICS_QUERY)


# ============================================================
# 5. SUPPORT METRICS
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
            WHEN s.status IN ('Resolved', 'Closed')
            THEN 1
            ELSE 0
        END
    ) AS resolved_support_tickets,

    ROUND(
        AVG(
            CASE
                WHEN s.resolution_time_hours IS NOT NULL
                THEN s.resolution_time_hours
            END
        ),
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


def get_support_metrics() -> pd.DataFrame:
    """Return organization-level support metrics."""
    return _execute_query(SUPPORT_METRICS_QUERY)


# ============================================================
# 6. DEPARTMENT METRICS
# ============================================================

DEPARTMENT_METRICS_QUERY = """
SELECT
    e.department,

    COUNT(DISTINCT e.employee_id) AS employee_count,

    SUM(
        CASE
            WHEN e.employment_status = 'Active'
            THEN 1
            ELSE 0
        END
    ) AS active_employee_count,

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
        AVG(e.special_projects_count),
        2
    ) AS average_special_projects

FROM employees AS e

GROUP BY e.department

ORDER BY employee_count DESC;
"""

def get_department_metrics() -> pd.DataFrame:
    """Return employee metrics grouped by department."""
    return _execute_query(DEPARTMENT_METRICS_QUERY)


# ============================================================
# 7. DEPARTMENT ONBOARDING METRICS
# ============================================================

DEPARTMENT_ONBOARDING_METRICS_QUERY = """
SELECT
    e.department,

    COUNT(DISTINCT e.employee_id) AS employee_count,

    COUNT(o.onboarding_task_id) AS total_tasks,

    SUM(
        CASE
            WHEN o.task_status = 'Complete'
            THEN 1
            ELSE 0
        END
    ) AS completed_tasks,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN o.task_status = 'Complete'
                THEN 1
                ELSE 0
            END
        )
        / NULLIF(COUNT(o.onboarding_task_id), 0),
        2
    ) AS completion_rate,

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
    ) AS average_completion_percentage

FROM employees AS e

LEFT JOIN onboarding_tasks AS o
    ON e.employee_id = o.employee_id

GROUP BY e.department

ORDER BY completion_rate DESC;
"""


def get_department_onboarding_metrics() -> pd.DataFrame:
    """Return onboarding metrics grouped by department."""
    return _execute_query(DEPARTMENT_ONBOARDING_METRICS_QUERY)


# ============================================================
# 8. DEPARTMENT SUPPORT METRICS
# ============================================================

DEPARTMENT_SUPPORT_METRICS_QUERY = """
SELECT
    e.department,

    COUNT(DISTINCT e.employee_id) AS employee_count,

    COUNT(s.ticket_id) AS total_tickets,

    SUM(
        CASE
            WHEN s.status = 'Open'
            THEN 1
            ELSE 0
        END
    ) AS open_tickets,

    SUM(
        CASE
            WHEN s.status IN ('Resolved', 'Closed')
            THEN 1
            ELSE 0
        END
    ) AS resolved_tickets,

    ROUND(
        AVG(s.resolution_time_hours),
        2
    ) AS average_resolution_time_hours,

    SUM(
        CASE
            WHEN s.priority IN ('High', 'Critical')
            THEN 1
            ELSE 0
        END
    ) AS high_priority_tickets

FROM employees AS e

LEFT JOIN support_tickets AS s
    ON e.employee_id = s.employee_id

GROUP BY e.department

ORDER BY total_tickets DESC;
"""


def get_department_support_metrics() -> pd.DataFrame:
    """Return support metrics grouped by department."""
    return _execute_query(DEPARTMENT_SUPPORT_METRICS_QUERY)


# ============================================================
# 9. EMPLOYEE ONBOARDING + SUPPORT
# ============================================================

EMPLOYEE_ONBOARDING_SUPPORT_QUERY = """
SELECT
    e.employee_id,
    e.employee_name,
    e.department,
    e.position,
    e.employment_status,

    COUNT(DISTINCT o.onboarding_task_id)
        AS onboarding_task_count,

    SUM(
        CASE
            WHEN o.task_status = 'Complete'
            THEN 1
            ELSE 0
        END
    ) AS completed_onboarding_tasks,

    ROUND(
        AVG(o.completion_percentage),
        2
    ) AS onboarding_completion_percentage,

    COUNT(DISTINCT s.ticket_id)
        AS support_ticket_count,

    SUM(
        CASE
            WHEN s.status = 'Open'
            THEN 1
            ELSE 0
        END
    ) AS open_support_ticket_count,

    ROUND(
        AVG(s.resolution_time_hours),
        2
    ) AS average_resolution_time_hours

FROM employees AS e

LEFT JOIN onboarding_tasks AS o
    ON e.employee_id = o.employee_id

LEFT JOIN support_tickets AS s
    ON e.employee_id = s.employee_id

GROUP BY
    e.employee_id,
    e.employee_name,
    e.department,
    e.position,
    e.employment_status

ORDER BY
    support_ticket_count DESC,
    onboarding_completion_percentage ASC;
"""


def get_employee_onboarding_support() -> pd.DataFrame:
    """
    Return employee-level onboarding and support metrics.
    """
    return _execute_query(EMPLOYEE_ONBOARDING_SUPPORT_QUERY)


# ============================================================
# 10. DEPARTMENT EMPLOYEE FILTER
# ============================================================

DEPARTMENT_EMPLOYEE_METRICS_QUERY = """
SELECT
    e.employee_id,
    e.employee_name,
    e.department,
    e.position,
    e.employment_status,
    e.salary,
    e.performance_score,
    e.engagement_survey,
    e.emp_satisfaction,
    e.special_projects_count

FROM employees AS e

WHERE e.department = ?

ORDER BY e.employee_name;
"""


def get_department_employee_metrics(
    department: str,
) -> pd.DataFrame:
    """
    Return employee metrics for a selected department.

    Parameters
    ----------
    department:
        Department name to filter by.

    Raises
    ------
    ValueError
        If department is empty.
    """
    if not isinstance(department, str) or not department.strip():
        raise ValueError("department must be a non-empty string")

    return _execute_query(
        DEPARTMENT_EMPLOYEE_METRICS_QUERY,
        (department,),
    )


# ============================================================
# 11. HIGH SUPPORT EMPLOYEES
# ============================================================

HIGH_SUPPORT_EMPLOYEES_QUERY = """
SELECT
    e.employee_id,
    e.employee_name,
    e.department,
    e.position,
    e.employment_status,

    COUNT(s.ticket_id) AS support_ticket_count,

    SUM(
        CASE
            WHEN s.status = 'Open'
            THEN 1
            ELSE 0
        END
    ) AS open_support_ticket_count,

    SUM(
        CASE
            WHEN s.priority IN ('High', 'Critical')
            THEN 1
            ELSE 0
        END
    ) AS high_priority_ticket_count,

    ROUND(
        AVG(s.resolution_time_hours),
        2
    ) AS average_resolution_time_hours

FROM employees AS e

INNER JOIN support_tickets AS s
    ON e.employee_id = s.employee_id

GROUP BY
    e.employee_id,
    e.employee_name,
    e.department,
    e.position,
    e.employment_status

HAVING COUNT(s.ticket_id) >= ?

ORDER BY
    support_ticket_count DESC;
"""


def get_high_support_employees(
    minimum_tickets: int = 1,
) -> pd.DataFrame:
    """
    Return employees with at least the requested number
    of support tickets.
    """
    if not isinstance(minimum_tickets, int):
        raise ValueError("minimum_tickets must be an integer")

    if minimum_tickets < 0:
        raise ValueError(
            "minimum_tickets cannot be negative"
        )

    return _execute_query(
        HIGH_SUPPORT_EMPLOYEES_QUERY,
        (minimum_tickets,),
    )


# ============================================================
# 12. EMPLOYEE DETAILS
# ============================================================

EMPLOYEE_DETAILS_QUERY = """
SELECT
    e.employee_id,
    e.employee_name,
    e.department,
    e.position,
    e.employment_status,
    e.performance_score,
    e.engagement_survey,
    e.emp_satisfaction,
    e.salary,

    COUNT(DISTINCT o.onboarding_task_id)
        AS onboarding_task_count,

    ROUND(
        AVG(o.completion_percentage),
        2
    ) AS onboarding_completion_percentage,

    COUNT(DISTINCT l.learning_record_id)
        AS learning_record_count,

    SUM(
        CASE
            WHEN l.course_status = 'Completed'
            THEN 1
            ELSE 0
        END
    ) AS completed_learning_records,

    COUNT(DISTINCT t.usage_id)
        AS tool_usage_record_count,

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
    ) AS open_support_ticket_count

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
    e.emp_satisfaction,
    e.salary

ORDER BY e.employee_id;
"""


def get_employee_details() -> pd.DataFrame:
    """Return a consolidated employee reporting dataset."""
    return _execute_query(EMPLOYEE_DETAILS_QUERY)


# ============================================================
# 13. SUPPORT CATEGORY METRICS
# ============================================================

SUPPORT_CATEGORY_METRICS_QUERY = """
SELECT
    issue_category,

    COUNT(ticket_id) AS total_tickets,

    SUM(
        CASE
            WHEN status = 'Open'
            THEN 1
            ELSE 0
        END
    ) AS open_tickets,

    SUM(
        CASE
            WHEN status IN ('Resolved', 'Closed')
            THEN 1
            ELSE 0
        END
    ) AS resolved_tickets,

    ROUND(
        AVG(resolution_time_hours),
        2
    ) AS average_resolution_time_hours,

    SUM(
        CASE
            WHEN priority = 'Critical'
            THEN 1
            ELSE 0
        END
    ) AS critical_tickets,

    SUM(
        CASE
            WHEN priority = 'High'
            THEN 1
            ELSE 0
        END
    ) AS high_tickets

FROM support_tickets

GROUP BY issue_category

ORDER BY total_tickets DESC;
"""


def get_support_category_metrics() -> pd.DataFrame:
    """Return support metrics grouped by issue category."""
    return _execute_query(SUPPORT_CATEGORY_METRICS_QUERY)


# ============================================================
# 14. LEARNING COURSE METRICS
# ============================================================

LEARNING_COURSE_METRICS_QUERY = """
SELECT
    course_name,

    course_type,

    COUNT(learning_record_id) AS total_records,

    SUM(
        CASE
            WHEN course_status = 'Completed'
            THEN 1
            ELSE 0
        END
    ) AS completed_records,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN course_status = 'Completed'
                THEN 1
                ELSE 0
            END
        )
        / NULLIF(COUNT(learning_record_id), 0),
        2
    ) AS completion_rate,

    ROUND(
        AVG(assessment_score),
        2
    ) AS average_assessment_score,

    ROUND(
        AVG(completion_time_hours),
        2
    ) AS average_completion_time_hours

FROM learning_records

GROUP BY
    course_name,
    course_type

ORDER BY total_records DESC;
"""


def get_learning_course_metrics() -> pd.DataFrame:
    """Return learning metrics grouped by course."""
    return _execute_query(LEARNING_COURSE_METRICS_QUERY)


# ============================================================
# 15. TOOL ACTIVITY BY EMPLOYEE
# ============================================================

TOOL_ACTIVITY_BY_EMPLOYEE_QUERY = """
SELECT
    e.employee_id,
    e.employee_name,
    e.department,

    COUNT(t.usage_id) AS usage_record_count,

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
    ON e.employee_id = t.employee_id

GROUP BY
    e.employee_id,
    e.employee_name,
    e.department

ORDER BY
    average_daily_active_usage DESC;
"""


def get_tool_activity_by_employee() -> pd.DataFrame:
    """Return tool usage metrics for every employee."""
    return _execute_query(TOOL_ACTIVITY_BY_EMPLOYEE_QUERY)


# ============================================================
# 16. EXPORT REPORTS
# ============================================================

def export_sql_reports(
    output_directory: Path = DEFAULT_REPORT_DIRECTORY,
) -> dict[str, pd.DataFrame]:
    """
    Execute all SQL reporting queries and export the results
    as CSV files.

    Returns
    -------
    dict[str, pd.DataFrame]
        Dictionary containing all generated reports.
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
        output_path = (
            output_directory / f"{report_name}.csv"
        )

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
    print(
        f"Reports exported to: "
        f"{DEFAULT_REPORT_DIRECTORY}"
    )

    print("\nGenerated reports:")

    for report_name, dataframe in reports.items():
        print(
            f"- {report_name}: "
            f"{len(dataframe)} row(s)"
        )