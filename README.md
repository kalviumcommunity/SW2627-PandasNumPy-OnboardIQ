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

All datasets are currently stored in the raw data layer and are subject to validation and processing before analytical use.

## Data Validation & Profiling

Dataset intake, validation, and profiling have been completed for all five source datasets.

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
- Late onboarding tasks will be retained as a potential indicator of onboarding delays and operational bottlenecks.

### Data Quality Findings

The profiling stage identified data-quality considerations that will be addressed during processing and cleaning, including:

- Missing values in fields where nulls may represent legitimate business states
- Date columns currently stored as string/object types
- Categorical values requiring whitespace normalization
- Controlled-value standardization
- Business-rule validation for task, learning, and support statuses

Raw source datasets are not modified during the profiling stage.

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
- ✅ CSV data ingestion workflow established.
- ✅ Dataset loading and initial validation implemented.
- ✅ Dataset profiling notebook created.
- ✅ All five datasets profiled for data quality.
- ✅ Primary-key and duplicate validation completed.
- ✅ Referential-integrity checks completed.
- ✅ Missing-value analysis completed.
- ✅ Date and numeric validation completed.
- ✅ Categorical and status profiling completed.
- 🚧 Data cleaning and transformation in progress / next stage.
- ⏳ Processed analytical dataset creation pending.
- ⏳ SQLite database integration pending.
- ⏳ Analytical metrics and KPI development pending.

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

Development work is organized through GitHub Issues, milestones, branches, commits, and pull requests.

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

## Run the App

The Streamlit application will be run using:

```bash
python app.py
```

Application implementation is currently pending.

## Project Status

🚧 **Data Preparation & Development Phase**

### Completed

- ✅ PRD Completed
- ✅ MVP Scope Defined
- ✅ Low-Fidelity Wireframes Completed
- ✅ Data Sources Finalized
- ✅ Data Dictionary Completed
- ✅ CSV/JSON Data Ingestion Workflow Established
- ✅ Dataset Profiling Completed
- ✅ Data Quality Assessment Completed
- ✅ GitHub Project Workflow Established

### In Progress / Next

- 🚧 Data Cleaning & Transformation
- ⏳ Processed Dataset Creation
- ⏳ SQLite Database Setup
- ⏳ Analytical KPI Development
- ⏳ Streamlit Dashboard Development
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
Data Cleaning & Transformation
      ↓
SQLite / Analytical Layer
      ↓
KPI & Metric Calculation
      ↓
Streamlit Dashboard
      ↓
Onboarding Insights & Bottleneck Identification
```

The intended outcome is to help stakeholders identify onboarding friction, monitor completion and productivity proxies, understand support and learning patterns, and identify operational factors that may delay new-hire productivity.
