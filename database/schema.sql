PRAGMA foreign_keys = ON;

-- ============================================================
-- 1. EMPLOYEES
-- ============================================================

CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    employee_name TEXT NOT NULL,

    married_id INTEGER,
    marital_status_id INTEGER,
    gender_id INTEGER,
    emp_status_id INTEGER,
    dept_id INTEGER,
    perf_score_id INTEGER,
    diversity_job_fair_id INTEGER,

    salary INTEGER,
    terminated INTEGER,
    position_id INTEGER,

    position TEXT,
    state TEXT,
    zip INTEGER,
    dob TEXT,
    sex TEXT,
    marital_desc TEXT,
    citizen_desc TEXT,
    hispanic_latino TEXT,
    race_desc TEXT,

    date_of_hire TEXT,
    date_of_termination TEXT,
    term_reason TEXT,
    employment_status TEXT,
    department TEXT,

    manager_name TEXT,
    manager_id REAL,

    recruitment_source TEXT,
    performance_score TEXT,
    engagement_survey REAL,
    emp_satisfaction INTEGER,
    special_projects_count INTEGER,
    last_performance_review_date TEXT,
    days_late_last_30 INTEGER,
    absences INTEGER
);

-- ============================================================
-- 2. ONBOARDING PROGRESS
-- ============================================================

CREATE TABLE IF NOT EXISTS onboarding_tasks (
    onboarding_task_id TEXT PRIMARY KEY,

    employee_id INTEGER NOT NULL,

    task_name TEXT NOT NULL,
    task_category TEXT NOT NULL,
    current_stage TEXT NOT NULL,
    task_status TEXT NOT NULL,

    due_date TEXT NOT NULL,
    completed_date TEXT,

    completion_percentage REAL,

    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);

-- ============================================================
-- 3. INTERNAL TOOL USAGE
-- ============================================================

CREATE TABLE IF NOT EXISTS tool_usage (
    usage_id TEXT PRIMARY KEY,

    employee_id INTEGER NOT NULL,

    usage_date TEXT NOT NULL,

    slack_activity_count INTEGER,
    jira_usage_count INTEGER,
    github_activity_count INTEGER,
    teams_activity_count,
    workspace_activity_count,

    daily_active_usage INTEGER NOT NULL,

    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);

-- ============================================================
-- 4. SUPPORT TICKETS
-- ============================================================

CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id TEXT PRIMARY KEY,

    employee_id INTEGER NOT NULL,

    created_date TEXT NOT NULL,
    issue_category TEXT NOT NULL,
    priority TEXT NOT NULL,

    resolution_time_hours REAL,

    assigned_team TEXT NOT NULL,
    status TEXT NOT NULL,

    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);

-- ============================================================
-- 5. LEARNING MANAGEMENT
-- ============================================================

CREATE TABLE IF NOT EXISTS learning_records (
    learning_record_id TEXT PRIMARY KEY,

    employee_id INTEGER NOT NULL,

    course_name TEXT NOT NULL,
    course_type TEXT NOT NULL,

    assigned_date TEXT NOT NULL,
    completed_date TEXT,

    assessment_score REAL,
    completion_time_hours REAL,

    course_status TEXT NOT NULL,

    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);
-- ============================================================
-- ANALYTICAL INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_onboarding_tasks_employee_id
    ON onboarding_tasks(employee_id);

CREATE INDEX IF NOT EXISTS idx_learning_records_employee_id
    ON learning_records(employee_id);

CREATE INDEX IF NOT EXISTS idx_tool_usage_employee_id
    ON tool_usage(employee_id);

CREATE INDEX IF NOT EXISTS idx_support_tickets_employee_id
    ON support_tickets(employee_id);