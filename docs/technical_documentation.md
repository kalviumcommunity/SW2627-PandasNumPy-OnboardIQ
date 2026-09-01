# OnboardIQ – Employee Onboarding Analytics Dashboard

## 1. Project Overview

OnboardIQ is an employee onboarding analytics data product designed to help organizations monitor onboarding progress, learning completion, internal tool adoption, support activity, and productivity-readiness indicators from a single analytical view.

The project consolidates five related datasets into a reusable data workflow and exposes the resulting analytics through a Streamlit dashboard.

### Problem Statement

A rapidly scaling startup stores employee onboarding progress, internal tool usage, learning activity, and support request history separately. Because these sources are disconnected, it is difficult to identify onboarding bottlenecks, compare employee or departmental readiness, and understand factors that may affect productivity.

### Project Objective

OnboardIQ addresses this problem by:

- Consolidating five onboarding-related datasets.
- Validating and standardizing source data.
- Preprocessing analytical fields and deriving useful date features.
- Merging employee-level information into a consolidated analytical dataset.
- Loading validated source data into SQLite for relational analysis.
- Calculating onboarding, learning, support, tool-adoption, and productivity KPIs.
- Providing interactive Streamlit dashboards and visualizations.
- Supporting report/export workflows.
- Maintaining automated tests and CI validation.

---

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and data-processing language |
| Pandas | Data ingestion, cleaning, transformation, and analysis |
| NumPy | Numerical analysis and supporting calculations |
| SQLite | Relational analytical data layer |
| Streamlit | Interactive dashboard application |
| Plotly | Interactive charts and visualizations |
| pytest | Automated testing |
| Git & GitHub | Version control and collaboration |
| GitHub Actions | Continuous integration |
| Jupyter Notebook | Dataset profiling and exploratory analysis |
| Figma | UI/UX and wireframe design |

Dependencies are listed in `requirements.txt`.

---

# 3. System Architecture

The project follows a layered data-product architecture.

```text
                    ┌──────────────────────┐
                    │      Raw CSV/JSON    │
                    │      Data Sources    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Ingestion       │
                    │ src/ingestion/       │
                    │ loader.py            │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Validation &      │
                    │    Preprocessing     │
                    │ src/preprocessing/   │
                    │ src/validation/      │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
      ┌─────────────────────┐      ┌─────────────────────┐
      │ Transformation /    │      │ SQLite Database     │
      │ Employee-level      │      │ src/database/       │
      │ consolidation       │      │ database.py         │
      │ src/transformation/ │      │ loader.py           │
      └──────────┬──────────┘      └──────────┬──────────┘
                 │                            │
                 └─────────────┬──────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Analysis & Features  │
                    │ src/analysis/        │
                    │ src/features/        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Visualization /      │
                    │ Dashboard            │
                    │ src/visualization/   │
                    │ src/dashboard/       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Streamlit       │
                    │      app.py          │
                    └──────────────────────┘
```

---

# 4. Repository Structure

```text
OnboardIQ/
│
├── app.py
├── README.md
├── PRD.md
├── requirements.txt
├── LICENSE
├── .gitignore
│
├── .github/
│   └── pull_request_template.md
│
├── assets/
│
├── config/
│   ├── __init__.py
│   └── config.py
│
├── data/
│   ├── raw/
│   │   ├── employee.csv
│   │   ├── onboarding_progress.csv
│   │   ├── internal_tool_usage.csv
│   │   ├── support_tickets.csv
│   │   └── learning_management.csv
│   ├── processed/
│   │   └── employee_onboarding_analytics.csv
│   └── sample/
│
├── database/
│   └── schema.sql
│
├── docs/
│   ├── data_dictionary.md
│   └── github_workflow.md
│
├── notebooks/
│   └── 01_data_source_profiling.ipynb
│
├── reports/
│
├── src/
│   ├── analysis/
│   │   ├── alerts.py
│   │   ├── anomaly.py
│   │   ├── funnel.py
│   │   ├── kpis.py
│   │   ├── sql_analysis.py
│   │   ├── statistics.py
│   │   └── trends.py
│   │
│   ├── cleaning/
│   ├── config/
│   ├── dashboard/
│   │   ├── data.py
│   │   ├── filters.py
│   │   ├── kpis.py
│   │   ├── layout.py
│   │   ├── navigation.py
│   │   ├── session.py
│   │   ├── visualizations.py
│   │   └── pages/
│   │
│   ├── database/
│   │   ├── database.py
│   │   ├── loader.py
│   │   └── reporting.py
│   │
│   ├── features/
│   │   └── business_features.py
│   │
│   ├── ingestion/
│   │   └── loader.py
│   │
│   ├── preprocessing/
│   │   └── cleaning.py
│   │
│   ├── transformation/
│   │   └── merge.py
│   │
│   ├── utils/
│   │   ├── constants.py
│   │   ├── email_reporting.py
│   │   ├── export_utils.py
│   │   ├── file_utils.py
│   │   └── logging_utils.py
│   │
│   └── visualization/
│       ├── charts.py
│       └── plotly_charts.py
│
└── tests/
    ├── test_alerts.py
    ├── test_analysis.py
    ├── test_anomaly.py
    ├── test_config.py
    ├── test_dashboard.py
    ├── test_dashboard_filters.py
    ├── test_dashboard_visualizations.py
    ├── test_email_reporting.py
    ├── test_export_utils.py
    ├── test_file_utils.py
    ├── test_funnel.py
    ├── test_ingestion.py
    ├── test_kpis.py
    ├── test_layout.py
    ├── test_logging_utils.py
    ├── test_merge.py
    ├── test_pipeline.py
    ├── test_plotly_charts.py
    ├── test_preprocessing.py
    ├── test_sql_analysis.py
    ├── test_sql_reporting.py
    ├── test_statistics.py
    ├── test_trends.py
    └── test_visualization.py
```

Generated runtime files such as SQLite database state, logs, caches, and Python bytecode should not be treated as source code.

---

# 5. Data Sources

OnboardIQ currently uses five datasets.

| Dataset | Description | Rows | Columns |
|---|---|---:|---:|
| Employee | Employee master/reference information | 311 | 36 |
| Onboarding Progress | Tasks, stages, statuses, due dates, completion progress | 4,222 | 9 |
| Internal Tool Usage | Employee activity across internal productivity tools | 13,995 | 9 |
| Support Tickets | Support requests, categories, priorities, statuses, resolution data | 1,048 | 8 |
| Learning Management | Training assignments, completion, assessment scores, completion time | 3,192 | 9 |

Raw files are stored under:

```text
data/raw/
```

---

# 6. Data Quality and Validation

The project validates data before analytical use.

Validation includes:

- File existence checks.
- Supported file-extension checks.
- Empty-file detection.
- CSV and JSON parsing validation.
- Required-column validation.
- Primary-key duplicate detection.
- Referential-integrity validation.
- Date consistency validation.
- Numeric and categorical validation.
- Exact duplicate-row detection.
- Text whitespace normalization.
- Missing-value handling.

### Date Validation Findings

- No employee records were found where termination occurred before hire.
- No learning records were found where completion occurred before assignment.
- 1,788 onboarding tasks were completed before their due dates.
- 960 onboarding tasks were completed after their due dates.
- Early completion is retained as a potential onboarding-efficiency indicator.
- Late completion is retained as a potential onboarding-delay indicator.

Raw data is not modified during preprocessing.

---

# 7. Data Preprocessing Workflow

The reusable preprocessing workflow is implemented in:

```text
src/preprocessing/cleaning.py
```

The main workflow is:

```text
Input DataFrame
      │
      ▼
Text Standardization
      │
      ▼
Duplicate Removal
      │
      ▼
Data Type Conversion
      │
      ▼
Missing Value Handling
      │
      ▼
Date Feature Engineering
      │
      ▼
IQR Outlier Detection
      │
      ▼
Processed-Data Validation
      │
      ▼
Clean DataFrame
```

### Missing Values

Missing values are handled according to field meaning rather than using a single global imputation rule.

Examples:

- Missing employee termination dates are preserved for active employees.
- Missing onboarding completion dates are preserved for incomplete tasks.
- Missing learning completion dates are preserved for incomplete courses.
- Missing support-ticket resolution times can represent unresolved tickets.

### Data Types

The workflow standardizes:

- IDs → integer-compatible types.
- Numeric measures → integer/float.
- Dates → datetime-compatible types.
- Text/categorical fields → standardized strings.

### Outlier Detection

IQR-based outlier detection is used for selected analytical measures such as:

- Salary
- Absences
- Days late
- Special-project counts
- Support resolution time
- Assessment score
- Learning completion time

Outliers are **flagged rather than automatically deleted**, preserving potentially meaningful business information.

---

# 8. End-to-End Data Pipeline

The end-to-end pipeline is implemented in:

```text
src/pipeline.py
```

The pipeline provides reusable functions for loading, preprocessing, and producing the employee-level analytical dataset.

The processed output is:

```text
data/processed/employee_onboarding_analytics.csv
```

The pipeline was validated through dedicated tests.

Current full-suite validation:

```text
162 passed, 3 warnings
```

Run the complete test suite with:

```bash
python -m pytest -q
```

Use module invocation rather than relying on the `pytest` executable when the environment does not automatically expose the project root on `PYTHONPATH`:

```bash
python -m pytest -q
```

---

# 9. Employee-Level Data Consolidation

The transformation layer is implemented in:

```text
src/transformation/merge.py
```

The five source datasets are aggregated and combined around the employee reference table.

```text
Employee
   │
   ├── Onboarding
   ├── Tool Usage
   ├── Support Tickets
   └── Learning
```

The final employee-level dataset preserves all 311 employees.

Support-ticket aggregation covers employees who have tickets while employees without tickets remain in the final employee population through the merge strategy.

The transformation tests verify:

- One-row-per-employee aggregation where expected.
- No duplicate employee IDs in aggregated results.
- Preservation of all employees.
- Correct support-ticket coverage.
- Valid employee foreign-key references.

---

# 10. SQLite Database

SQLite provides the relational analytical layer.

Schema:

```text
employees
    │
    ├── onboarding_tasks
    ├── tool_usage
    ├── support_tickets
    └── learning_records
```

The `employees` table acts as the parent/reference table.

### Database Tables

| Table | Source | Rows |
|---|---|---:|
| `employees` | Employee | 311 |
| `onboarding_tasks` | Onboarding Progress | 4,222 |
| `tool_usage` | Internal Tool Usage | 13,995 |
| `support_tickets` | Support Tickets | 1,048 |
| `learning_records` | Learning Management | 3,192 |

### Database Loader

The database loader is:

```text
src/database/loader.py
```

It:

1. Reads the raw datasets.
2. Maps employee source column names to database-friendly names.
3. Clears existing table data in dependency order.
4. Loads employees first.
5. Loads child tables.
6. Commits the transaction.
7. Rolls back if an exception occurs.
8. Closes the connection.

This makes repeated database initialization safer, including during automated testing.

### Database Setup

Initialize the SQLite database:

```bash
python src/database/database.py
```

Load all datasets:

```bash
python -m src.database.loader
```

Expected load counts:

```text
Loaded 311 records into employees.
Loaded 4222 records into onboarding_tasks.
Loaded 13995 records into tool_usage.
Loaded 1048 records into support_tickets.
Loaded 3192 records into learning_records.

All datasets loaded successfully.
```

---

# 11. Analytics Layer

Analytical functionality is organized under:

```text
src/analysis/
```

Current modules include:

- `kpis.py` — KPI calculations.
- `alerts.py` — analytical alerts.
- `anomaly.py` — anomaly detection.
- `funnel.py` — onboarding funnel analysis.
- `statistics.py` — statistical analysis.
- `trends.py` — trend analysis.
- `sql_analysis.py` — SQL-based analytical operations.

Business-oriented feature calculations are available under:

```text
src/features/business_features.py
```

The analytics layer supports analysis of:

- Onboarding completion.
- Productivity-readiness indicators.
- Learning completion.
- Assessment performance.
- Tool adoption.
- Support demand.
- Resolution time.
- Department-level performance.
- Employee-level activity.
- Trends and anomalies.

---

# 12. Dashboard Architecture

The Streamlit application entry point is:

```text
app.py
```

The dashboard is organized into reusable modules:

```text
src/dashboard/
├── data.py
├── filters.py
├── kpis.py
├── layout.py
├── navigation.py
├── session.py
├── visualizations.py
└── pages/
    ├── analytics.py
    ├── dashboard.py
    ├── data_preview.py
    ├── employees.py
    └── onboarding.py
```

The application includes functionality for:

- Dashboard navigation.
- KPI display.
- Filtering.
- Employee-level views.
- Onboarding analysis.
- Analytics views.
- Dataset preview.
- Interactive visualizations.
- Uploaded CSV/JSON dataset handling.
- Session-state management.

The default processed dataset is:

```text
data/processed/employee_onboarding_analytics.csv
```

Uploaded datasets can take priority over the default processed dataset in the application session.

---

# 13. Running the Streamlit Application

Activate the virtual environment first.

Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Then install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

If `streamlit` is directly available in the environment, this also works:

```bash
streamlit run app.py
```

The Streamlit terminal output provides the local application address.

---

# 14. Dataset Upload

The application supports CSV and JSON uploads.

Supported file types:

```text
.csv
.json
```

Upload validation includes:

- Extension validation.
- Empty-file validation.
- CSV parsing.
- JSON parsing.
- Empty-dataset validation.

The application displays uploaded dataset information such as:

- Filename.
- File type.
- Row count.
- Column count.
- Missing-value count.
- Memory usage.
- Column names.
- Data preview.
- Missing-value summary.

Uploaded data can be cleared from the application session.

---

# 15. Testing

Automated tests are stored in:

```text
tests/
```

The suite covers:

- Configuration.
- File utilities.
- Logging.
- CSV/JSON ingestion.
- Data validation.
- Preprocessing.
- Duplicate handling.
- Missing-value behavior.
- Date features.
- Outlier detection.
- Dataset merging.
- KPI calculations.
- Statistical analysis.
- Trend analysis.
- Funnel analysis.
- Anomaly detection.
- Alerts.
- SQL analysis.
- SQL reporting.
- Dashboard functionality.
- Dashboard filters.
- Dashboard visualizations.
- Plotly charts.
- Export utilities.
- Email reporting.
- End-to-end pipeline behavior.

Run all tests:

```bash
python -m pytest -q
```

Run one test module:

```bash
python -m pytest -q tests/test_pipeline.py
```

### Current Validation

The project has reached:

```text
162 passed
3 warnings
```

The remaining warnings are related to Pandas date-format inference in the preprocessing layer. They do not currently cause test failures.

---

# 16. Continuous Integration

GitHub Actions is configured to execute automated validation.

The intended workflow is:

```text
Push / Pull Request
        │
        ▼
GitHub Actions
        │
        ▼
Install dependencies
        │
        ▼
Run automated tests
        │
        ▼
Pass / Fail
```

Before opening a pull request, run:

```bash
python -m pytest -q
```

and verify:

```bash
git status
```

The working tree should be clean after committing intended changes.

---

# 17. GitHub Development Workflow

The project uses an issue-driven workflow:

```text
GitHub Issue
     ↓
Feature Branch
     ↓
Implementation
     ↓
Automated Tests
     ↓
Commit
     ↓
Pull Request
     ↓
Review / CI
     ↓
Merge
```

Example branch:

```bash
git checkout -b feature/issue-33-technical-documentation
```

Check changes:

```bash
git status
git diff
```

Stage changes:

```bash
git add <files>
```

Commit:

```bash
git commit -m "docs: add technical documentation"
```

Push:

```bash
git push -u origin feature/issue-33-technical-documentation
```

Pull requests should reference the relevant issue and summarize:

- What changed.
- Why it changed.
- Testing performed.
- Any known limitations.

---

# 18. Configuration and Paths

Project configuration is split between:

```text
config/config.py
```

and:

```text
src/config/settings.py
```

Project-level paths include raw data, processed data, error output, logs, and application settings.

Before changing paths, check the existing configuration modules rather than hard-coding new absolute paths.

The project is designed to use relative/project-root-based paths so that it can be moved between development environments.

---

# 19. Logging

Logging utilities are implemented in:

```text
src/utils/logging_utils.py
```

Runtime logs are written under:

```text
logs/
```

The application and data workflow use logging to record major workflow events and operational information.

Avoid committing generated logs unless they are intentionally required as documentation artifacts.

---

# 20. Reporting and Exports

Reporting functionality is available through:

```text
src/database/reporting.py
src/utils/export_utils.py
src/utils/email_reporting.py
```

The project supports analytical reporting and export-oriented workflows.

Generated reports should be treated as output artifacts and stored under:

```text
reports/
```

where appropriate.

---

# 21. Data Profiling Notebook

The primary profiling notebook is:

```text
notebooks/01_data_source_profiling.ipynb
```

It documents exploratory profiling and data-quality assessment.

To reproduce the notebook analysis:

1. Activate the virtual environment.
2. Ensure dependencies are installed.
3. Open the notebook.
4. Restart the kernel if required.
5. Execute all cells using **Run All**.

The notebook should be used to understand source-data characteristics rather than as the production pipeline itself.

---

# 22. UI/UX Design

Low-fidelity dashboard wireframes were created in Figma.

Design reference:

https://www.figma.com/make/i6QNepl4k69jR7MHq3uifz/Data-Analytics-Dashboard---Low-Fid--Copy-?fullscreen=1&t=tpzJzT7vpdmrSJqB-1&code-node-id=0-6

The design work covers the dashboard structure, supporting analytical pages, navigation, filters, and theme considerations.

---

# 23. User Guide

## For an analyst or manager

1. Launch the Streamlit application.
2. Open the dashboard.
3. Review the headline onboarding and productivity KPIs.
4. Use filters to narrow the analysis by relevant employee attributes.
5. Review onboarding progress and completion patterns.
6. Review learning and assessment indicators.
7. Review internal tool usage.
8. Review support-ticket demand and resolution patterns.
9. Inspect employee-level records when deeper investigation is required.
10. Use available reporting/export functions for sharing results.

## For data users

Use the processed employee-level dataset for consolidated analysis:

```text
data/processed/employee_onboarding_analytics.csv
```

Use the SQLite database when relational SQL analysis is more appropriate.

---

# 24. Troubleshooting

## `ModuleNotFoundError: No module named 'src'`

If this occurs while running tests, use:

```bash
python -m pytest -q
```

instead of:

```bash
pytest -q
```

This ensures the project is executed using the active Python environment and project context.

## Missing dependencies

Run:

```bash
python -m pip install -r requirements.txt
```

## Missing default dataset

Verify that:

```text
data/processed/employee_onboarding_analytics.csv
```

exists.

The end-to-end pipeline can be used to regenerate the processed dataset when appropriate.

## Missing raw dataset

Verify that all five files exist under:

```text
data/raw/
```

Expected files:

```text
employee.csv
onboarding_progress.csv
internal_tool_usage.csv
support_tickets.csv
learning_management.csv
```

## Database loading problems

Initialize the database and reload the datasets:

```bash
python src/database/database.py
python -m src.database.loader
```

## Streamlit does not start

Verify the environment:

```bash
python --version
python -m pip --version
```

Then verify Streamlit:

```bash
python -m streamlit --version
```

Run:

```bash
python -m streamlit run app.py
```

---

# 25. Known Limitations and Release Notes

Before final release, verify the following items against the latest code:

- Final dashboard functionality and page coverage.
- Final KPI definitions and business thresholds.
- Final report/export behavior.
- Final Streamlit user flow.
- Remaining Pandas date-format warnings.
- Production handling of generated SQLite/database artifacts.
- Final dependency versions.
- Final presentation/demo assets.
- Final release tag and version information.

Documentation should be updated whenever these implementation details change.

---

# 26. Project Completion Checklist

## Product

- [x] PRD completed.
- [x] MVP scope defined.
- [x] Data sources finalized.
- [x] Data dictionary completed.
- [x] UI/UX wireframes created.

## Data Engineering

- [x] Raw datasets established.
- [x] Ingestion workflow implemented.
- [x] Validation implemented.
- [x] Preprocessing implemented.
- [x] Date features implemented.
- [x] Outlier detection implemented.
- [x] Employee-level data pipeline implemented.
- [x] SQLite schema implemented.
- [x] Database loading implemented.
- [x] Relational validation implemented.

## Analytics

- [x] KPI analysis modules implemented.
- [x] Trend analysis implemented.
- [x] Funnel analysis implemented.
- [x] Anomaly analysis implemented.
- [x] Alert functionality implemented.
- [x] SQL analysis/reporting implemented.

## Application

- [x] Streamlit entry point exists.
- [x] Dashboard modules exist.
- [x] Filtering functionality exists.
- [x] Employee view exists.
- [x] Onboarding view exists.
- [x] Analytics view exists.
- [x] Data preview/upload functionality exists.
- [x] Visualization modules exist.

## Quality

- [x] Automated test suite implemented.
- [x] Full test suite passing.
- [x] GitHub Actions CI implemented.
- [ ] Final refactoring/performance review.
- [ ] Final end-to-end release testing.
- [ ] Version 1.0 release preparation.
- [ ] Final presentation/demo assets.

---

# 27. Related Documentation

- `PRD.md` — Product requirements and project scope.
- `docs/data_dictionary.md` — Dataset and field definitions.
- `docs/github_workflow.md` — GitHub development workflow.
- `notebooks/01_data_source_profiling.ipynb` — Data profiling.
- `database/schema.sql` — SQLite schema.
- `requirements.txt` — Python dependencies.

---

# 28. Support / Development Reference

When extending OnboardIQ:

1. Create or update the relevant GitHub Issue.
2. Create a dedicated feature branch.
3. Identify the correct application layer.
4. Keep raw data immutable.
5. Add or update automated tests.
6. Run the complete test suite.
7. Update documentation if behavior changes.
8. Commit using a clear conventional-style message.
9. Push the branch.
10. Open a pull request linked to the issue.
11. Confirm CI passes before merge.

The preferred architecture is modular: ingestion, preprocessing, transformation, database, analysis, visualization, dashboard, and utilities should remain separated rather than placing business logic directly in `app.py`.

---

# 29. Final Project Summary

OnboardIQ provides an end-to-end employee onboarding analytics workflow:

```text
Raw Data
   ↓
Ingestion
   ↓
Validation
   ↓
Preprocessing
   ↓
Transformation
   ↓
Employee-Level Dataset
   ↓
SQLite + Analytical Modules
   ↓
KPIs / Trends / Alerts / Analysis
   ↓
Streamlit Dashboard
   ↓
Reports & Decision Support
```

The project combines data engineering, analytics, relational database design, automated testing, visualization, and interactive application development into a single data product.
