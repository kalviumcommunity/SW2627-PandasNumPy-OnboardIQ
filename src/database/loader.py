from pathlib import Path

import pandas as pd

from src.database.database import get_connection


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


# ============================================================
# CSV FILES
# ============================================================

DATASET_FILES = {
    "employees": "employee.csv",
    "onboarding_tasks": "onboarding_progress.csv",
    "tool_usage": "internal_tool_usage.csv",
    "support_tickets": "support_tickets.csv",
    "learning_records": "learning_management.csv",
}


# ============================================================
# EMPLOYEE COLUMN MAPPING
# ============================================================

EMPLOYEE_COLUMN_MAPPING = {
    "Employee_Name": "employee_name",
    "EmpID": "employee_id",
    "MarriedID": "married_id",
    "MaritalStatusID": "marital_status_id",
    "GenderID": "gender_id",
    "EmpStatusID": "emp_status_id",
    "DeptID": "dept_id",
    "PerfScoreID": "perf_score_id",
    "FromDiversityJobFairID": "diversity_job_fair_id",
    "Salary": "salary",
    "Termd": "terminated",
    "PositionID": "position_id",
    "Position": "position",
    "State": "state",
    "Zip": "zip",
    "DOB": "dob",
    "Sex": "sex",
    "MaritalDesc": "marital_desc",
    "CitizenDesc": "citizen_desc",
    "HispanicLatino": "hispanic_latino",
    "RaceDesc": "race_desc",
    "DateofHire": "date_of_hire",
    "DateofTermination": "date_of_termination",
    "TermReason": "term_reason",
    "EmploymentStatus": "employment_status",
    "Department": "department",
    "ManagerName": "manager_name",
    "ManagerID": "manager_id",
    "RecruitmentSource": "recruitment_source",
    "PerformanceScore": "performance_score",
    "EngagementSurvey": "engagement_survey",
    "EmpSatisfaction": "emp_satisfaction",
    "SpecialProjectsCount": "special_projects_count",
    "LastPerformanceReview_Date": "last_performance_review_date",
    "DaysLateLast30": "days_late_last_30",
    "Absences": "absences",
}


# ============================================================
# LOAD CSV FILE
# ============================================================

def read_dataset(file_name):
    """
    Read a CSV file from the raw data directory.
    """

    file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


# ============================================================
# LOAD EMPLOYEES
# ============================================================

def load_employees(connection):
    """
    Load employee records into the employees table.
    """

    df = read_dataset(DATASET_FILES["employees"])

    # Convert source column names to database column names.
    df = df.rename(columns=EMPLOYEE_COLUMN_MAPPING)

    # Insert employees first because other tables
    # reference employee_id as a foreign key.
    df.to_sql(
        "employees",
        connection,
        if_exists="append",
        index=False,
    )

    print(
        f"Loaded {len(df)} records into employees."
    )


# ============================================================
# LOAD ONBOARDING TASKS
# ============================================================

def load_onboarding_tasks(connection):
    """
    Load onboarding progress records.
    """

    df = read_dataset(DATASET_FILES["onboarding_tasks"])

    df.to_sql(
        "onboarding_tasks",
        connection,
        if_exists="append",
        index=False,
    )

    print(
        f"Loaded {len(df)} records into onboarding_tasks."
    )


# ============================================================
# LOAD TOOL USAGE
# ============================================================

def load_tool_usage(connection):
    """
    Load internal tool usage records.
    """

    df = read_dataset(DATASET_FILES["tool_usage"])

    df.to_sql(
        "tool_usage",
        connection,
        if_exists="append",
        index=False,
    )

    print(
        f"Loaded {len(df)} records into tool_usage."
    )


# ============================================================
# LOAD SUPPORT TICKETS
# ============================================================

def load_support_tickets(connection):
    """
    Load support ticket records.
    """

    df = read_dataset(DATASET_FILES["support_tickets"])

    df.to_sql(
        "support_tickets",
        connection,
        if_exists="append",
        index=False,
    )

    print(
        f"Loaded {len(df)} records into support_tickets."
    )


# ============================================================
# LOAD LEARNING RECORDS
# ============================================================

def load_learning_records(connection):
    """
    Load learning management records.
    """

    df = read_dataset(DATASET_FILES["learning_records"])

    df.to_sql(
        "learning_records",
        connection,
        if_exists="append",
        index=False,
    )

    print(
        f"Loaded {len(df)} records into learning_records."
    )


# ============================================================
# LOAD ALL DATASETS
# ============================================================

def load_all_datasets():
    """
    Populate all five SQLite tables with a fresh dataset.

    Existing records are cleared before loading so that the
    function can be safely called multiple times, including
    during automated tests.
    """

    connection = get_connection()

    try:
        # Clear child tables before employees because of
        # foreign-key relationships.
        connection.execute("DELETE FROM learning_records")
        connection.execute("DELETE FROM support_tickets")
        connection.execute("DELETE FROM tool_usage")
        connection.execute("DELETE FROM onboarding_tasks")
        connection.execute("DELETE FROM employees")

        # Load employees first because the remaining datasets
        # contain foreign keys referencing employee_id.
        load_employees(connection)
        load_onboarding_tasks(connection)
        load_tool_usage(connection)
        load_support_tickets(connection)
        load_learning_records(connection)

        connection.commit()

        print("\nAll datasets loaded successfully.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    load_all_datasets()