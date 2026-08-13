# OnboardIQ – Employee Onboarding Analytics Dashboard

## Problem Statement

A rapidly scaling startup stores employee onboarding progress, internal tool usage, and support request history separately, making it difficult to identify operational bottlenecks affecting employee productivity.

## Project Objective

Build an interactive analytics dashboard that consolidates onboarding data, analyzes productivity trends, and provides actionable insights using Python, Pandas, NumPy, SQLite, and Streamlit.

## Technology Stack

- Python
- Pandas
- NumPy
- SQLite
- Streamlit
- GitHub Actions
- Jupyter Notebook
- Git & GitHub
- Figma

## Repository Structure

```text
src/
    database/
data/
    raw/
    processed/
database/
notebooks/
reports/
tests/
docs/
design/
```

## Data Sources

The project currently works with five datasets covering the major dimensions of the onboarding process:

1. **Employee Dataset**
   - Employee master/reference information
   - Used as the primary employee dimension

2. **Onboarding Progress Dataset**
   - Onboarding tasks, stages, statuses, due dates, and completion progress

3. **Internal Tool Usage Dataset**
   - Aggregate employee activity across approved internal productivity tools

4. **Support Ticket Dataset**
   - Structured support requests, issue categories, priorities, statuses, and resolution times

5. **Learning Management Dataset**
   - Training assignments, completion status, assessment scores, and completion time

All datasets are stored in the raw data layer and are validated and processed before analytical use.

## Data Validation & Profiling

Dataset intake, validation, profiling, cleaning, and standardization have been performed across all five source datasets.

The profiling workflow includes:

- Dataset shape and schema inspection
- Column and data-type validation
- Primary-key uniqueness checks
- Null primary-key checks
- Missing-value analysis
- Referential-integrity validation
- Date-order validation
- Numeric range validation
- Categorical-value profiling
- Status and business-rule validation
- Data-quality findings documentation

### Current Profiling Results

| Dataset | Rows | Columns | Primary Key | Duplicate IDs | Null IDs | Referential Integrity |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| Employee | 311 | 36 | EmpID | 0 | 0 | N/A |
| Onboarding Progress | 4,222 | 9 | onboarding_task_id | 0 | 0 | Pass |
| Internal Tool Usage | 13,995 | 9 | usage_id | 0 | 0 | Pass |
| Support Tickets | 1,048 | 8 | ticket_id | 0 | 0 | Pass |
| Learning Management | 3,192 | 9 | learning_record_id | 0 | 0 | Pass |

### Date Validation Findings

- No employee records were found where termination occurred before the hire date.
- No learning records were found where course completion occurred before assignment.
- 1,788 onboarding tasks were completed before their due dates.
- 960 onboarding tasks were completed after their due dates.
- Early completions are retained as a potential indicator of onboarding efficiency.
- Late onboarding tasks are retained as a potential indicator of onboarding delays and operational bottlenecks.

### Data Quality Findings

The profiling stage identified data-quality considerations that were addressed or documented during preprocessing, including:

- Missing values in fields where nulls may represent legitimate business states
- Date columns requiring datetime standardization
- Categorical values requiring whitespace normalization
- Controlled-value standardization
- Business-rule validation for task, learning, and support statuses

Raw source datasets remain unchanged. Processing and standardization are performed through the data-processing workflow.

## Data Preprocessing & Standardization

A preprocessing workflow has been implemented to improve consistency across the five source datasets.

### Missing Value Handling

Missing values were analyzed across all datasets and handled according to the meaning of each field rather than applying a single global imputation strategy.

Examples include:

- Preserving legitimate missing termination dates for active employees
- Preserving missing completion dates for incomplete onboarding and learning records
- Handling optional assessment and completion-time fields according to course status
- Retaining missing resolution times where support tickets are not yet resolved

This approach prevents legitimate business states from being incorrectly converted into artificial values.

### Data Type Standardization

Relevant fields were standardized to appropriate analytical types, including:

- Employee identifiers → integer
- Foreign-key employee identifiers → integer
- Numeric measures → integer/float
- Dates → datetime-compatible format
- Categorical attributes → standardized string values

Whitespace and inconsistent categorical representations were also identified and normalized where required.

### Preprocessing Objective

```text
Raw CSV Data
     ↓
Validation
     ↓
Missing Value Handling
     ↓
Data Type Standardization
     ↓
Cleaned / Processed Data
     ↓
SQLite Database
     ↓
Analytics
```

## SQLite Database

A relational SQLite database has been designed and populated to provide the analytical data layer for OnboardIQ.

### Database Schema

```text
employees
    │
    ├── onboarding_tasks
    ├── tool_usage
    ├── support_tickets
    └── learning_records
```

The `employees` table acts as the parent/reference table.

The remaining four tables reference `employees.employee_id` through foreign-key relationships.

### Database Tables

| SQLite Table | Source Dataset | Rows |
| --- | --- | ---: |
| `employees` | Employee | 311 |
| `onboarding_tasks` | Onboarding Progress | 4,222 |
| `tool_usage` | Internal Tool Usage | 13,995 |
| `support_tickets` | Support Tickets | 1,048 |
| `learning_records` | Learning Management | 3,192 |

### Database Validation

The populated database has been validated for:

- Correct table creation
- Correct row counts
- Primary-key uniqueness
- Foreign-key relationships
- Employee-to-dataset relationships
- Successful relational queries

Validation results:

- **0 duplicate primary-key IDs** across all five tables
- **0 invalid employee foreign-key references**
- Successful employee-to-onboarding relational queries
- All five source datasets successfully loaded into SQLite

### SQLite Data Loading Workflow

A reusable Python loader has been implemented to populate the database from the validated CSV datasets.

The loading sequence is:

```text
Employee CSV
     ↓
employees table
     ↓
Dependent datasets
     ├── onboarding_tasks
     ├── tool_usage
     ├── support_tickets
     └── learning_records
```

Employees are loaded first so that foreign-key relationships can be maintained when dependent datasets are inserted.

Database transactions are used during the loading process so that failures can be rolled back instead of leaving a partially populated database.

### Database Files

```text
src/
└── database/
    ├── database.py
    └── loader.py

database/
└── schema.sql
```

The generated SQLite database is treated as a runtime/generated artifact and is not committed to the repository.

## Current Progress

### Product & Design

- ✅ Product Requirements Document (PRD) completed.
- ✅ MVP scope finalized, including features and exclusions.
- ✅ Data requirements and source definitions documented.
- ✅ Data dictionary completed for all five datasets.
- ✅ Low-fidelity wireframes designed.
- ✅ Unified dashboard and supporting pages structured for the MVP.
- ✅ Settings page updated with Light and Dark theme options.
- ✅ Reports & Export page updated to support CSV and PDF exports.

### Data Engineering & Analysis

- ✅ Five source datasets identified and added to the project.
- ✅ Raw data directory structure created.
- ✅ CSV/JSON data ingestion workflow established.
- ✅ Dataset loading and initial validation implemented.
- ✅ Dataset profiling notebook created.
- ✅ All five datasets profiled for data quality.
- ✅ Primary-key and duplicate validation completed.
- ✅ Referential-integrity checks completed.
- ✅ Missing-value analysis completed.
- ✅ Missing-value handling implemented.
- ✅ Date validation completed.
- ✅ Numeric validation completed.
- ✅ Categorical and status profiling completed.
- ✅ Data type standardization implemented.
- ✅ SQLite relational schema designed.
- ✅ SQLite tables created.
- ✅ All five datasets populated into SQLite.
- ✅ SQLite row-count validation completed.
- ✅ SQLite primary-key validation completed.
- ✅ SQLite foreign-key validation completed.
- ✅ Relational database query validation completed.
- ⏳ Analytical KPI and metric development pending.

### Dashboard & Application

- ⏳ Dashboard implementation pending.
- ⏳ Streamlit application development pending.
- ⏳ Interactive filters and visualizations pending.
- ⏳ Productivity and onboarding KPI implementation pending.
- ⏳ Final reports and export integration pending.

## GitHub Development Workflow

The project follows a structured GitHub workflow:

```text
Issue
  ↓
Branch
  ↓
Development
  ↓
Commit
  ↓
Pull Request
  ↓
Review
  ↓
Merge
```

Development work is organized through GitHub Issues, milestones, feature branches, commits, and pull requests.

Each major implementation task is developed independently and merged into the main branch through a pull request.

## Design

### Low-Fidelity Wireframes

**Figma Link:**

> https://www.figma.com/make/i6QNepl4k69jR7MHq3uifz/Data-Analytics-Dashboard---Low-Fid--Copy-?fullscreen=1&t=tpzJzT7vpdmrSJqB-1&code-node-id=0-6

## Data Profiling Notebook

The initial data-quality profiling workflow is available at:

```text
notebooks/
└── 01_data_source_profiling.ipynb
```

The notebook can be executed from a fresh kernel using **Run All** to reproduce the profiling results.

## Database Setup

The SQLite database can be initialized using:

```bash
python src/database/database.py
```

The validated source datasets can then be loaded using:

```bash
python -m src.database.loader
```

Expected successful loading output:

```text
Loaded 311 records into employees.
Loaded 4222 records into onboarding_tasks.
Loaded 13995 records into tool_usage.
Loaded 1048 records into support_tickets.
Loaded 3192 records into learning_records.

All datasets loaded successfully.
```

## Run the App

The Streamlit application will be run using:

```bash
python app.py
```

Application implementation is currently pending.

## Project Status

🚧 **Data Engineering & Application Development Phase**

### Completed

- ✅ PRD Completed
- ✅ MVP Scope Defined
- ✅ Low-Fidelity Wireframes Completed
- ✅ Data Sources Finalized
- ✅ Data Dictionary Completed
- ✅ CSV/JSON Data Ingestion Workflow Established
- ✅ Dataset Profiling Completed
- ✅ Data Quality Assessment Completed
- ✅ Missing Value Handling Completed
- ✅ Data Type Standardization Completed
- ✅ SQLite Schema Designed
- ✅ SQLite Database Tables Created
- ✅ SQLite Data Population Completed
- ✅ Database Relationship Validation Completed
- ✅ GitHub Project Workflow Established

### In Progress / Next

- ⏳ Analytical KPI Development
- ⏳ Processed Analytical Dataset Refinement
- ⏳ Streamlit Dashboard Development
- ⏳ Interactive Dashboard Filters
- ⏳ Productivity and Onboarding Analytics
- ⏳ Power BI-Compatible Data Exports
- ⏳ Testing & Validation
- ⏳ Final Dashboard Integration

## Project Objective Outcome

The final OnboardIQ product will provide a consolidated view of employee onboarding health by combining:

```text
Employee Data
      +
Onboarding Progress
      +
Internal Tool Usage
      +
Support Tickets
      +
Learning Management
      ↓
Data Validation & Profiling
      ↓
Missing Value Handling
      +
Data Type Standardization
      ↓
SQLite Relational Data Layer
      ↓
KPI & Metric Calculation
      ↓
Streamlit Dashboard
      ↓
Onboarding Insights & Bottleneck Identification
```

The intended outcome is to help stakeholders identify onboarding friction, monitor completion and productivity proxies, understand support and learning patterns, and identify operational factors that may delay new-hire productivity.
