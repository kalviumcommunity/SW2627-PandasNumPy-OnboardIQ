# OnboardIQ — Data Dictionary

## 1. Purpose

This data dictionary documents the five datasets used by the OnboardIQ MVP. It defines the business meaning, data type, validation expectations, and analytical role of each field.

Datasets:
1. Employee
2. Onboarding Progress
3. Internal Tool Usage
4. Support Tickets
5. Learning Management

The Employee dataset acts as the master dimension. `EmpID` is aligned to the `employee_id` foreign-key field used by the other four datasets during processing.

---

## 2. Dataset Overview

| Dataset | Rows | Columns | Primary Key | Role |
|---|---:|---:|---|---|
| Employee | 311 | 36 | `EmpID` | Employee/master dimension |
| Onboarding Progress | 4,222 | 9 | `onboarding_task_id` | Onboarding task and stage progression |
| Internal Tool Usage | 13,995 | 9 | `usage_id` | Daily tool-adoption signals |
| Support Tickets | 1,048 | 8 | `ticket_id` | Onboarding support friction |
| Learning Management | 3,192 | 9 | `learning_record_id` | Learning and enablement progress |

---

# 3. Employee Dataset

## 3.1 Business Purpose

The Employee dataset is the master employee dimension for onboarding analysis. It provides organizational context and the employee identifier required to join onboarding, tool usage, support, and learning records.

The source contains additional HR attributes that are not required for the MVP. Sensitive or out-of-scope fields should be removed or excluded during processing and cleaning before analytical use.

## 3.2 Source Profile

- Rows: **311**
- Columns: **36**
- Primary key: `EmpID`
- Duplicate `EmpID` values: **0**
- Null `EmpID` values: **0**
- Missing `DateofTermination`: **207 (66.56%)**
- Missing `ManagerID`: **8 (2.57%)**

## 3.3 Fields

| Field | Type | Business Meaning | Validation / Processing |
|---|---|---|---|
| `Employee_Name` | String | Employee name in source | Exclude from analytical layer if de-identification is required |
| `EmpID` | Integer | Unique employee identifier | Required; unique; non-null |
| `MarriedID` | Integer | Source marital-status indicator | Exclude from MVP |
| `MaritalStatusID` | Integer | Source marital-status identifier | Exclude from MVP |
| `GenderID` | Integer | Source gender identifier | Exclude from MVP |
| `EmpStatusID` | Integer | Employment-status identifier | Controlled values; use only for approved eligibility logic |
| `DeptID` | Integer | Department identifier | Map to standardized department |
| `PerfScoreID` | Integer | Source performance-score identifier | Exclude from MVP productivity score |
| `FromDiversityJobFairID` | Integer | Recruitment-source indicator | Exclude from MVP |
| `Salary` | Integer | Employee salary | Exclude from MVP |
| `Termd` | Integer | Termination indicator | Use only for approved eligibility filtering |
| `PositionID` | Integer | Position identifier | Map to normalized role where required |
| `Position` | String | Employee position/job role | Normalize into role/role family |
| `State` | String | State/location in source | Map to approved location/region |
| `Zip` | Integer | ZIP/postal code | Exclude from MVP |
| `DOB` | Date/String | Date of birth | Exclude from MVP |
| `Sex` | String | Sex field | Exclude from MVP |
| `MaritalDesc` | String | Marital-status description | Exclude from MVP |
| `CitizenDesc` | String | Citizenship description | Exclude from MVP |
| `HispanicLatino` | String | Hispanic/Latino indicator | Exclude from MVP |
| `RaceDesc` | String | Race description | Exclude from MVP |
| `DateofHire` | Date | Employee hire/start date | Required; valid date |
| `DateofTermination` | Date | Employee termination date | Nullable; must not precede hire date |
| `ManagerID` | Integer/String | Manager identifier | Nullable where unavailable; validate references where applicable |
| `ManagerName` | String | Manager name | Exclude or de-identify |
| `RecruitmentSource` | String | Recruitment source | Optional; exclude if not needed |
| `PerformanceScore` | String | Source performance classification | Not the MVP productivity score |
| `EngagementSurvey` | Numeric | Source engagement survey score | Optional; exclude if not needed |
| `EmpSatisfaction` | Numeric | Employee satisfaction measure | Optional; exclude if not needed |
| `SpecialProjectsCount` | Integer | Number of special projects | Non-negative; not required for MVP |
| `LastPerformanceReview_Date` | Date | Last performance review date | Valid date; not required for onboarding KPI |
| `DaysLateLast30` | Integer | Days late during last 30 days | Non-negative |
| `Absences` | Integer | Recorded absences | Non-negative |

> The raw source contains 36 columns. The raw file should remain unchanged; processing should create an MVP-specific employee dimension containing only approved fields.

## 3.4 Recommended Analytical Employee Fields

| Analytical Field | Source / Derivation |
|---|---|
| `employee_id` | `EmpID` |
| `department` | Normalized department source field |
| `manager_id` | `ManagerID` where available |
| `joining_date` | `DateofHire` |
| `role` | Normalized `Position` |
| `location` | Standardized `State`/location |
| `employment_type` | Derived/mapped from approved employment-status information |
| `onboarding_cohort` | Derived from `joining_date` as joining month |

---

# 4. Onboarding Progress Dataset

## 4.1 Business Purpose

Captures onboarding checklist tasks, stages, statuses, due dates, completion dates, and completion percentages. One employee can have many task records.

## 4.2 Source Profile

- Rows: **4,222**
- Columns: **9**
- Primary key: `onboarding_task_id`
- Duplicate IDs: **0**
- Null IDs: **0**
- Referential integrity: **Pass**
- Missing `completed_date`: **1,142 (27.05%)**

## 4.3 Fields

| Field | Type | Business Meaning | Validation |
|---|---|---|---|
| `onboarding_task_id` | String | Unique onboarding task record | Required; unique; non-null |
| `employee_id` | Integer/String | Employee associated with task | Required; valid employee foreign key |
| `task_name` | String | Human-readable onboarding task | Required |
| `task_category` | Categorical | Functional task category | Controlled: HR, IT, Manager, Role-specific, Compliance |
| `current_stage` | Categorical | Onboarding stage | Controlled: Preboarding, Setup, Orientation, Enablement, Productive |
| `task_status` | Categorical | Current task state | Controlled: Not Started, In Progress, Complete, Blocked, Overdue |
| `due_date` | Date | Expected completion date | Required; valid date |
| `completed_date` | Date | Actual completion date | Nullable when incomplete |
| `completion_percentage` | Decimal | Task completion percentage | 0–100 |

Observed statuses: Complete 3,080; In Progress 504; Blocked 282; Not Started 154; Overdue 202.

---

# 5. Internal Tool Usage Dataset

## 5.1 Business Purpose

Provides privacy-conscious aggregate daily adoption indicators for required internal tools. No message content, file content, or detailed surveillance data is used.

## 5.2 Source Profile

- Rows: **13,995**
- Columns: **9**
- Primary key: `usage_id`
- Duplicate IDs: **0**
- Null IDs: **0**
- Referential integrity: **Pass**
- Missing values: **None identified**

## 5.3 Fields

| Field | Type | Business Meaning | Validation |
|---|---|---|---|
| `usage_id` | String | Unique daily usage record | Required; unique; non-null |
| `employee_id` | Integer/String | Employee associated with usage | Required; valid foreign key |
| `usage_date` | Date | Activity date | Required; valid date |
| `slack_activity_count` | Integer | Aggregate Slack collaboration activity | Non-negative |
| `jira_usage_count` | Integer | Aggregate Jira/project activity | Non-negative |
| `github_activity_count` | Integer | Aggregate GitHub/repository activity | Non-negative; role-aware |
| `teams_activity_count` | Integer | Aggregate Microsoft Teams activity | Non-negative |
| `workspace_activity_count` | Integer | Aggregate Google Workspace activity | Non-negative |
| `daily_active_usage` | Boolean | Whether daily adoption threshold was met | Required; Boolean |

Observed ranges: Slack 0–19, Jira 0–12, GitHub 0–14, Teams 0–13, Workspace 0–21.

---

# 6. Support Tickets Dataset

## 6.1 Business Purpose

Captures structured support friction during onboarding, including access, hardware, HR, learning, and other operational issues.

## 6.2 Source Profile

- Rows: **1,048**
- Columns: **8**
- Primary key: `ticket_id`
- Duplicate IDs: **0**
- Null IDs: **0**
- Referential integrity: **Pass**
- Missing `resolution_time_hours`: **105 (10.02%)**

## 6.3 Fields

| Field | Type | Business Meaning | Validation |
|---|---|---|---|
| `ticket_id` | String | Unique support ticket identifier | Required; unique; non-null |
| `employee_id` | Integer/String | Employee affected by ticket | Required; valid foreign key |
| `created_date` | DateTime | Ticket creation timestamp | Required; valid timestamp |
| `issue_category` | Categorical | Type of support issue | Controlled: Access, Hardware, Payroll, HR Policy, Learning, Other |
| `priority` | Categorical | Ticket priority | Controlled: Low, Medium, High, Critical |
| `resolution_time_hours` | Decimal | Time from creation to resolution | Non-negative; nullable while unresolved |
| `assigned_team` | String | Responsible support team | Required |
| `status` | Categorical | Ticket lifecycle status | Controlled: Open, In Progress, Resolved, Closed |

Observed statuses: Open 22; In Progress 83; Resolved 0; Closed 0.

---

# 7. Learning Management Dataset

## 7.1 Business Purpose

Records mandatory, orientation, role-specific, and optional learning assignments. Supports analysis of training completion alongside onboarding progress and productivity-readiness indicators.

## 7.2 Source Profile

- Rows: **3,192**
- Columns: **9**
- Primary key: `learning_record_id`
- Duplicate IDs: **0**
- Null IDs: **0**
- Referential integrity: **Pass**
- Missing `completed_date`: **961 (30.11%)**
- Missing `assessment_score`: **840 (26.32%)**
- Missing `completion_time_hours`: **961 (30.11%)**

## 7.3 Fields

| Field | Type | Business Meaning | Validation |
|---|---|---|---|
| `learning_record_id` | String | Unique learning assignment record | Required; unique; non-null |
| `employee_id` | Integer/String | Employee assigned to course | Required; valid foreign key |
| `course_name` | String | Learning course title | Required |
| `course_type` | Categorical | Learning category | Controlled: Compliance, Orientation, Role-specific, Optional |
| `assigned_date` | Date | Date assigned | Required; valid date |
| `completed_date` | Date | Completion date | Nullable until completed; must not precede assignment |
| `assessment_score` | Decimal | Assessment result | 0–100 or null |
| `completion_time_hours` | Decimal | Time to complete course | Non-negative when complete |
| `course_status` | Categorical | Current learning status | Controlled: Assigned, In Progress, Completed, Overdue |

Observed statuses: Completed 2,231; In Progress 447; Assigned 288; Overdue 226.

---

# 8. Cross-Source Data Quality Rules

## 8.1 Primary Keys

| Dataset | Primary Key | Duplicate IDs | Null IDs |
|---|---|---:|---:|
| Employee | `EmpID` | 0 | 0 |
| Onboarding Progress | `onboarding_task_id` | 0 | 0 |
| Internal Tool Usage | `usage_id` | 0 | 0 |
| Support Tickets | `ticket_id` | 0 | 0 |
| Learning Management | `learning_record_id` | 0 | 0 |

All five datasets passed primary-key uniqueness and null checks.

## 8.2 Referential Integrity

- Onboarding Progress → Employee: **Pass**
- Internal Tool Usage → Employee: **Pass**
- Support Tickets → Employee: **Pass**
- Learning Management → Employee: **Pass**

No orphan employee IDs were identified.

## 8.3 Date Validation

| Check | Result |
|---|---:|
| Employee termination before hire | 0 |
| Learning completion before assignment | 0 |
| Invalid/null parsing for required date fields | 0 |

Onboarding tasks completed before their due date are treated as valid early completions rather than errors.

## 8.4 Numeric Validation

| Field | Minimum | Maximum | Result |
|---|---:|---:|---|
| Onboarding `completion_percentage` | 0 | 100 | Pass |
| Slack activity | 0 | 19 | Pass |
| Jira activity | 0 | 12 | Pass |
| GitHub activity | 0 | 14 | Pass |
| Teams activity | 0 | 13 | Pass |
| Workspace activity | 0 | 21 | Pass |
| Support resolution time | 1.05 | 112.88 | Pass |
| Learning assessment score | 40 | 100 | Pass |
| Learning completion time | 0.86 | 9.09 | Pass |
| Employee `Salary` | 45,046 | 250,000 | Pass |
| Employee `Absences` | 1 | 20 | Pass |
| Employee `DaysLateLast30` | 0 | 6 | Pass |
| Employee `SpecialProjectsCount` | 0 | 8 | Pass |
| Employee `PerfScoreID` | 1 | 4 | Pass |
| Employee `EmpStatusID` | 1 | 5 | Pass |

---

# 9. Missing-Value Handling

Missing values are not automatically errors.

| Dataset | Field | Missing Count | Interpretation |
|---|---|---:|---|
| Employee | `DateofTermination` | 207 | Expected for employees without termination records |
| Employee | `ManagerID` | 8 | Manager information unavailable |
| Onboarding Progress | `completed_date` | 1,142 | Expected for incomplete tasks |
| Support Tickets | `resolution_time_hours` | 105 | Expected for unresolved tickets |
| Learning Management | `completed_date` | 961 | Expected for incomplete learning |
| Learning Management | `assessment_score` | 840 | Unavailable/not applicable |
| Learning Management | `completion_time_hours` | 961 | Expected for incomplete learning |

Meaningful nulls should be preserved rather than blindly replaced with zero.

---

# 10. Standardization Rules

During processing and cleaning:

1. Standardize column names to `snake_case`.
2. Trim leading/trailing whitespace from categorical values.
3. Normalize inconsistent labels such as `Production       `.
4. Normalize role labels and duplicate labels caused by whitespace.
5. Convert date fields to proper datetime/date types.
6. Convert numeric fields to appropriate numeric types.
7. Convert Boolean fields to consistent Boolean representation.
8. Map source `EmpID` to analytical `employee_id`.
9. Apply controlled mappings for departments, task categories, onboarding stages, support categories, learning types, and statuses.
10. Exclude sensitive/non-MVP employee attributes from the analytical layer.
11. Preserve raw source files unchanged.
12. Record rejected records and validation reasons rather than silently discarding them.
13. Preserve source lineage and processing/refresh timestamps.

---

# 11. Analytical Relationship Model

```text
                    ┌──────────────────────┐
                    │       Employee       │
                    │        EmpID         │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼──────────────────┐
             │                 │                  │
             ▼                 ▼                  ▼
┌────────────────────┐ ┌──────────────────┐ ┌────────────────────┐
│ Onboarding         │ │ Internal Tool    │ │ Support Tickets    │
│ Progress           │ │ Usage            │ │                    │
│ employee_id        │ │ employee_id      │ │ employee_id        │
└────────────────────┘ └──────────────────┘ └────────────────────┘

                               ▼
                    ┌────────────────────┐
                    │ Learning           │
                    │ Management         │
                    │ employee_id        │
                    └────────────────────┘
```

### Relationship Cardinality

- One employee → many onboarding task records.
- One employee → many daily tool usage records.
- One employee → many support tickets.
- One employee → many learning assignment records.

---

# 12. Dataset Readiness Summary

| Dataset | Structural Quality | Referential Integrity | Main Processing Requirement | MVP Readiness |
|---|---|---|---|---|
| Employee | Good | Master | Remove/exclude sensitive and unnecessary fields; normalize labels | Ready after cleaning |
| Onboarding Progress | Good | Pass | Parse dates and preserve meaningful incomplete-task nulls | Ready |
| Internal Tool Usage | Good | Pass | Validate role-appropriate tool usage and normalize types | Ready |
| Support Tickets | Good | Pass | Handle unresolved-ticket resolution-time nulls | Ready |
| Learning Management | Good | Pass | Preserve completion-related nulls and normalize statuses | Ready |

---

# 13. Data Governance Note

The raw Employee dataset contains personal, demographic, compensation, and other HR attributes. These fields should **not** be carried into the MVP analytical layer unless explicitly approved.

The preferred analytical employee dimension is:

- `employee_id`
- `department`
- `manager_id`
- `joining_date`
- `role`
- `location`
- `employment_type`
- `onboarding_cohort`

The raw files should remain unchanged for source traceability, while the processed layer should contain only approved fields and derived analytical features.
