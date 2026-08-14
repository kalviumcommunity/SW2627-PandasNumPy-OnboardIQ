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

## Data Sources

The project currently works with five datasets:

1. **Employee Dataset** — employee master/reference information.
2. **Onboarding Progress Dataset** — onboarding tasks, stages, statuses, due dates, and completion progress.
3. **Internal Tool Usage Dataset** — employee activity across internal productivity tools.
4. **Support Ticket Dataset** — support requests, issue categories, priorities, statuses, and resolution times.
5. **Learning Management Dataset** — training assignments, completion status, assessment scores, and completion time.

## Data Validation & Profiling

Dataset intake, validation, profiling, cleaning, and standardization have been performed across all five datasets.

| Dataset | Rows | Columns | Primary Key | Duplicate IDs | Null IDs | Referential Integrity |
|---|---:|---:|---|---:|---:|---|
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
- Late tasks are retained as a potential indicator of onboarding delays.

## Data Preprocessing & Standardization

A reusable preprocessing workflow has been implemented across the five source datasets.

### Missing Value Handling

Missing values are handled according to the meaning of each field rather than through a single global imputation strategy.

Examples include:

- Preserving missing termination dates for active employees.
- Preserving missing completion dates for incomplete onboarding and learning records.
- Handling optional assessment and completion-time fields according to course status.
- Retaining missing resolution times where tickets are not yet resolved.

### Data Type Standardization

Relevant fields are standardized to appropriate analytical types:

- Employee and foreign-key identifiers → integer
- Numeric measures → integer/float
- Dates → datetime-compatible format
- Categorical attributes → standardized strings

### Duplicate Detection & Text Normalization

The preprocessing workflow includes:

- Exact duplicate-row detection and removal.
- Primary-key duplicate validation.
- Leading/trailing whitespace normalization.
- Internal whitespace standardization.
- Preservation of meaningful null values.
- Dataset-specific text normalization without modifying raw source files.

Validation found **0 exact duplicate rows** and **0 duplicate primary-key values** across all five datasets.

The Employee `Department` field contained trailing whitespace in `Production       ` and is normalized to `Production`. A whitespace issue in the `Position` field was also normalized.

## Automated Testing

The preprocessing and ingestion workflows are supported by automated tests using `pytest`.

The suite covers configuration, file utilities, CSV/JSON ingestion, validation, logging, preprocessing, text standardization, null preservation, duplicate removal, and end-to-end preprocessing behavior.

Current test result:

```text
20 passed
```

Run tests with:

```bash
python -m pytest -v
```

## SQLite Database

A relational SQLite database has been designed and populated as the analytical data layer.

### Database Schema

```text
employees
    │
    ├── onboarding_tasks
    ├── tool_usage
    ├── support_tickets
    └── learning_records
```

The `employees` table is the parent/reference table. The other four tables reference `employees.employee_id`.

### Database Tables

| SQLite Table | Source Dataset | Rows |
|---|---|---:|
| `employees` | Employee | 311 |
| `onboarding_tasks` | Onboarding Progress | 4,222 |
| `tool_usage` | Internal Tool Usage | 13,995 |
| `support_tickets` | Support Tickets | 1,048 |
| `learning_records` | Learning Management | 3,192 |

### Database Validation

- 0 duplicate primary-key IDs across all five tables.
- 0 invalid employee foreign-key references.
- Successful employee-to-onboarding relational queries.
- All five source datasets successfully loaded into SQLite.

A reusable Python loader populates the database from the validated CSV datasets. Employees are loaded first so foreign-key relationships can be maintained, and transactions are used during loading.

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

- ✅ PRD completed.
- ✅ MVP scope finalized.
- ✅ Data requirements and source definitions documented.
- ✅ Data dictionary completed for all five datasets.
- ✅ Low-fidelity wireframes designed.
- ✅ Dashboard and supporting pages structured for the MVP.
- ✅ Light/Dark theme options defined.
- ✅ CSV and PDF report export requirements defined.

### Data Engineering & Analysis

- ✅ Five source datasets finalized.
- ✅ Raw data structure created.
- ✅ CSV/JSON ingestion workflow established.
- ✅ Initial validation implemented.
- ✅ Dataset profiling completed.
- ✅ Primary-key and duplicate validation completed.
- ✅ Referential-integrity checks completed.
- ✅ Missing-value analysis and handling completed.
- ✅ Date and numeric validation completed.
- ✅ Categorical and status profiling completed.
- ✅ Data type standardization completed.
- ✅ Duplicate-row detection/removal completed.
- ✅ Text and categorical normalization completed.
- ✅ SQLite relational schema designed.
- ✅ SQLite tables created.
- ✅ All five datasets populated into SQLite.
- ✅ SQLite row-count, primary-key, and foreign-key validation completed.
- ✅ Relational query validation completed.
- ✅ Automated test suite passing.
- ⏳ Analytical KPI and metric development pending.

### Dashboard & Application

- ⏳ Streamlit dashboard implementation pending.
- ⏳ Interactive filters and visualizations pending.
- ⏳ Productivity and onboarding KPI implementation pending.
- ⏳ Final reports and export integration pending.

## GitHub Development Workflow

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

Development is organized through GitHub Issues, milestones, feature branches, commits, and pull requests.

## Repository Structure

```text
src/
    database/
    ingestion/
    preprocessing/
    validation/
    analysis/
    transformation/
    visualization/
data/
    raw/
    processed/
    sample/
database/
notebooks/
reports/
tests/
docs/
assets/
config/
```

## Design

### Low-Fidelity Wireframes

**Figma Link:**

https://www.figma.com/make/i6QNepl4k69jR7MHq3uifz/Data-Analytics-Dashboard---Low-Fid--Copy-?fullscreen=1&t=tpzJzT7vpdmrSJqB-1&code-node-id=0-6

## Data Profiling Notebook

```text
notebooks/
└── 01_data_source_profiling.ipynb
```

The notebook can be executed from a fresh kernel using **Run All** to reproduce the profiling results.

## Database Setup

Initialize the SQLite database:

```bash
python src/database/database.py
```

Load the validated datasets:

```bash
python -m src.database.loader
```

Expected output:

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

- ✅ PRD
- ✅ MVP scope
- ✅ Low-fidelity wireframes
- ✅ Data sources and data dictionary
- ✅ CSV/JSON ingestion workflow
- ✅ Dataset profiling and quality assessment
- ✅ Missing-value handling
- ✅ Data type standardization
- ✅ Duplicate detection and removal
- ✅ Text/categorical normalization
- ✅ SQLite schema and tables
- ✅ SQLite data population
- ✅ Database relationship validation
- ✅ Automated tests
- ✅ GitHub development workflow

### In Progress / Next

- ⏳ Analytical KPI development
- ⏳ Processed analytical dataset refinement
- ⏳ Streamlit dashboard development
- ⏳ Interactive dashboard filters
- ⏳ Productivity and onboarding analytics
- ⏳ Power BI-compatible exports
- ⏳ Final dashboard integration

## Project Objective Outcome

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
      +
Duplicate & Text Normalization
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
