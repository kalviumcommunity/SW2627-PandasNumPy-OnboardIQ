from pathlib import Path
import sqlite3


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_PATH = DATABASE_DIR / "onboardiq.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create and return a SQLite database connection.

    Foreign-key enforcement is enabled for the connection.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database():
    """
    Create the SQLite database schema from schema.sql.
    """

    connection = get_connection()

    try:
        with open(
            SCHEMA_PATH,
            "r",
            encoding="utf-8",
        ) as schema_file:

            schema = schema_file.read()

        connection.executescript(schema)
        connection.commit()

    finally:
        connection.close()


# ============================================================
# TABLE INSPECTION
# ============================================================

def get_table_names():
    """
    Return all user-created tables in the database.
    """

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        )

        return [
            row[0]
            for row in cursor.fetchall()
        ]

    finally:
        connection.close()


# ============================================================
# QUERY OPTIMIZATION INDEXES
# ============================================================

def create_analytical_indexes():
    """
    Create indexes that improve common analytical joins.

    Foreign-key columns used by analytical joins are indexed
    to reduce unnecessary table scans.
    """

    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_onboarding_tasks_employee_id
            ON onboarding_tasks(employee_id)
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_learning_records_employee_id
            ON learning_records(employee_id)
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_tool_usage_employee_id
            ON tool_usage(employee_id)
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_support_tickets_employee_id
            ON support_tickets(employee_id)
            """
        )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# INDEX INSPECTION
# ============================================================

def get_index_names():
    """
    Return user-created analytical index names.

    SQLite automatically creates internal indexes for primary
    keys. Those internal indexes are excluded from this result.
    """

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'index'
              AND name NOT LIKE 'sqlite_autoindex_%'
            ORDER BY name
            """
        )

        return [
            row[0]
            for row in cursor.fetchall()
        ]

    finally:
        connection.close()


# ============================================================
# ANALYTICAL VIEWS
# ============================================================

def create_analytical_views():
    """
    Create reusable SQL views for the analytical reporting layer.

    Views provide employee-level summaries that can be queried
    directly by analysis modules and dashboard components.
    """

    connection = get_connection()

    try:

        # --------------------------------------------------------
        # VIEW 1: EMPLOYEE ONBOARDING SUMMARY
        # --------------------------------------------------------

        connection.execute(
            """
            CREATE VIEW IF NOT EXISTS
            vw_employee_onboarding_summary AS

            SELECT
                e.employee_id,
                e.department,
                e.position,

                COUNT(
                    o.onboarding_task_id
                ) AS total_onboarding_tasks,

                SUM(
                    CASE
                        WHEN o.task_status = 'Complete'
                        THEN 1
                        ELSE 0
                    END
                ) AS completed_onboarding_tasks,

                AVG(
                    o.completion_percentage
                ) AS average_completion_percentage

            FROM employees AS e

            LEFT JOIN onboarding_tasks AS o
                ON e.employee_id = o.employee_id

            GROUP BY
                e.employee_id,
                e.department,
                e.position
            """
        )

        # --------------------------------------------------------
        # VIEW 2: EMPLOYEE ANALYTICS SUMMARY
        # --------------------------------------------------------

        connection.execute(
            """
            CREATE VIEW IF NOT EXISTS
            vw_employee_analytics_summary AS

            SELECT
                e.employee_id,
                e.department,

                COUNT(
                    DISTINCT o.onboarding_task_id
                ) AS total_onboarding_tasks,

                COUNT(
                    DISTINCT CASE
                        WHEN o.task_status = 'Complete'
                        THEN o.onboarding_task_id
                    END
                ) AS completed_onboarding_tasks,

                AVG(
                    o.completion_percentage
                ) AS onboarding_completion_rate,

                COUNT(
                    DISTINCT l.learning_record_id
                ) AS total_learning_records,

                COUNT(
                    DISTINCT CASE
                        WHEN l.course_status = 'Completed'
                        THEN l.learning_record_id
                    END
                ) AS completed_courses,

                AVG(
                    l.assessment_score
                ) AS average_assessment_score,

                COUNT(
                    DISTINCT t.usage_id
                ) AS total_usage_records,

                AVG(
                    t.daily_active_usage
                ) AS average_daily_active_usage,

                COUNT(
                    DISTINCT s.ticket_id
                ) AS total_support_tickets,

                COUNT(
                    DISTINCT CASE
                        WHEN s.status IN (
                            'Open',
                            'In Progress'
                        )
                        THEN s.ticket_id
                    END
                ) AS open_support_tickets,

                AVG(
                    s.resolution_time_hours
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
                e.department
            """
        )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# VIEW INSPECTION
# ============================================================

def get_view_names():
    """
    Return all user-created analytical views.
    """

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'view'
            ORDER BY name
            """
        )

        return [
            row[0]
            for row in cursor.fetchall()
        ]

    finally:
        connection.close()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    initialize_database()

    create_analytical_indexes()

    create_analytical_views()

    tables = get_table_names()

    indexes = get_index_names()

    views = get_view_names()

    print("Database initialized successfully.")

    print("\nTables:")

    for table in tables:
        print(f"- {table}")

    print("\nAnalytical indexes:")

    for index in indexes:
        print(f"- {index}")

    print("\nAnalytical views:")

    for view in views:
        print(f"- {view}")