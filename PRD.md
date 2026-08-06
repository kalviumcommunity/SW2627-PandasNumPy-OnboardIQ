# Employee Onboarding Analytics Platform — Product Requirements Document (PRD)

---

# Product Requirements Document (PRD)

# OnboardIQ - Employee Onboarding Analytics Platform

Problem statement — A rapidly scaling startup stores employee onboarding progress, internal tool usage, and support request history separately, but leadership has no visibility into which operational friction points slow down new-hire productivity during their first month.

| Field | Detail |
| --- | --- |
| Version | 1.0.0 |
| Status | Waiting for Approval – Ready for Development |
| Created | 2026-08-04 |
| Last Updated | 2026-08-06 |
| Document Type | Product Requirements Document |
| Project | OnboardIQ - Employee Onboarding Analytics Platform |
| Tech Stack | Python · Pandas · NumPy · SQL · Streamlit · GitHub · GitHub Actions |

## Table of Contents

1. Executive Summary
2. Business Problem
3. User Personas
4. User Pain Points
5. Project Goals
6. Dataset & Data Source Documentation
7. Success Metrics
8. Functional Requirements
9. Non-Functional Requirements
10. User Stories
11. Dashboard Pages & User Experience
12. MVP Scope
13. Future Scope
14. Risks and Assumptions
15. Acceptance Criteria  



---



# 1\. Executive Summary

OnboardIQ Employee Onboarding Analytics Platform is a unified analytics product that transforms disconnected onboarding, learning, collaboration-tool usage, and HR/IT support data into actionable insight about a new employee’s first 30 days. It enables HR managers, department managers, HR Operations analysts, and executive leaders to understand how quickly employees complete required onboarding, where progress is delayed, whether key internal tools are being adopted, and which operational issues correlate with slow time-to-productivity.

Scaling organizations frequently operate onboarding through a combination of HR information systems, learning platforms, task trackers, collaboration tools, ticketing systems, and spreadsheets. Each system can report on its own activity, but none explains the full experience of a new hire. A task may appear overdue in an onboarding tracker, while the underlying cause is an unresolved laptop-access ticket, a delayed manager approval, or incomplete role-specific training. In the absence of a shared analytical view, HR and managers rely on manual follow-up and retrospective reporting rather than early intervention.

Built as a data product using Python, SQL, machine learning, Streamlit, and Power BI-compatible exports, the platform provides:

* A consolidated onboarding record that joins employee, task, learning, tool-adoption, and support-ticket data.
* Role- and department-level dashboards for monitoring onboarding health, completion, productivity proxies, and outstanding actions.
* KPI calculations for completion time, time-to-productivity, task completion, training completion, tool adoption, and support resolution.
* Analytics that identify bottlenecks by stage, department, manager, location, and issue category.
* Machine learning features that estimate completion risk, predict likely delays, segment onboarding experiences, identify anomalies, and suggest targeted interventions.
* Exportable reports that make executive reviews and HR Operations reporting faster, more consistent, and evidence-based.

The MVP is deliberately analytical rather than transactional. It accepts governed CSV datasets, performs repeatable validation and transformation, and delivers a demonstrable decision-support experience without introducing employee self-service workflows, authentication, or live HR-system integrations. This document defines the requirements, boundaries, measures of success, and acceptance criteria needed to deliver the capstone project as a credible enterprise-style SaaS analytics product.

# 2\. Business Problem

## 2.1 Context

For a growing startup, the first month of employment is a critical period. New hires must complete mandatory paperwork, obtain equipment and system access, meet their manager and team, complete training, understand priorities, and begin contributing. The organization already records much of this activity, but the evidence is fragmented. HR may own the employee roster and checklist; IT owns access and hardware tickets; Learning and Development owns course completion; department managers track role readiness; and collaboration platforms contain indirect signals of adoption.

This fragmentation makes it difficult to distinguish normal variation from operational failure. For example, a new engineer who has not completed security training may be blocked by an unresolved identity-management ticket rather than lack of engagement. A manager may incorrectly perceive poor onboarding performance because no shared view exposes the dependency. Conversely, an apparently completed checklist may conceal weak adoption of the tools required for effective work.

Current reporting is commonly manual, delayed, and narrowly scoped. HR Operations analysts extract files from multiple systems, reconcile employee IDs and dates, clean inconsistent department labels, and prepare periodic spreadsheets. By the time a report reaches leadership, the affected employees may have spent weeks experiencing avoidable friction. The organization lacks a reliable way to ask: Which onboarding stages create the most delay? Which departments or locations have higher risk? What support issues are most strongly associated with low productivity? Which managers need an early intervention list?

## 2.2 The Core Gap

There is no unified intelligence layer that connects the operational evidence required to understand onboarding outcomes.

| Data Source | What it tells the organization | What is missing without integration |
| --- | --- | --- |
| Employee dataset | Who joined, their role, department, manager, and start date | Context for comparing cohorts and ownership |
| Onboarding progress | Which tasks and stages are complete or overdue | Why work is blocked and how delays affect readiness |
| Internal tool usage | Whether essential tools are being adopted | Early behavioral signals of productivity readiness |
| Support tickets | What access, equipment, HR, or IT problems employees encounter | The operational root cause behind incomplete work |
| Learning management data | Whether required and role-specific learning is complete | Whether skills and compliance readiness are progressing |

Without connecting these data sources, leadership can measure individual activities but cannot explain their relationship to onboarding effectiveness. The company knows that a task is pending, but not whether the employee lacks access, whether their cohort is affected, whether the manager has a bottleneck, or whether completion delay is likely to extend beyond the target window.

## 2.3 Business Impact

The absence of unified onboarding analytics affects employees and the business in measurable ways:

* HR teams spend substantial time compiling recurring reports instead of improving processes and supporting high-risk employees.
* Managers receive incomplete information and intervene too late, often after deadlines or early productivity targets have been missed.
* IT and HR support teams cannot quantify which issue categories create the greatest onboarding friction or prioritize fixes by organizational impact.
* Executives lack a consistent onboarding health indicator for workforce planning, retention risk discussions, and operating reviews.
* New employees may experience delayed access, duplicated requests, unclear expectations, and reduced confidence during their most formative period.
* The organization cannot establish a credible baseline for reducing time-to-productivity or evaluating whether process changes improve onboarding outcomes.

## 2.4 Opportunity

A focused analytics platform can turn onboarding from a set of disconnected administrative tasks into a measurable operational system. By joining records at the employee and cohort level, the platform can surface leading indicators before a first-month outcome becomes a retention or performance concern. The initial opportunity is to reduce manual reporting effort, identify bottlenecks earlier, and make manager and HR interventions more specific. Over time, the same governed data foundation can support real-time integrations, workflow recommendations, and benchmarking across departments.

# 3\. User Personas

## 3.1 Persona 1 — The HR Manager

Name: Maya Patel | Role: HR Manager

Background: Maya manages employee lifecycle programs for a rapidly growing organization with approximately 300 employees and 15–25 new hires per month. She is responsible for ensuring that the onboarding experience is consistent, compliant, and welcoming across departments and locations. She currently receives status updates from multiple systems and follows up manually with managers when required tasks remain incomplete.

| Attribute | Detail |
| --- | --- |
| Responsibilities | Own onboarding policy, monitor completion, coordinate HR and IT dependencies, improve employee experience, and report program health to leadership. |
| Primary Goals | Identify employees at risk before deadlines are missed; improve overall completion rates; understand process bottlenecks; ensure mandatory activities are completed. |
| Frustrations | Cannot see the full employee journey in one place; spends time reconciling reports; cannot easily tell whether delay is employee-, manager-, or system-driven. |
| Technical Comfort | Medium. Comfortable with dashboards, spreadsheets, filters, and exports; does not require SQL or model-level detail. |
| Success Metrics | Onboarding completion rate; average completion time; percentage of new hires requiring escalation; manager satisfaction; first-30-day employee feedback. |

## 3.2 Persona 2 — The Department Manager

Name: Daniel Kim | Role: Engineering Department Manager

Background: Daniel leads a team of 18 employees and receives several new hires each quarter. He is accountable for helping new employees become productive, assigning role-specific onboarding activities, and resolving blockers in partnership with HR and IT. He needs a concise view of team progress rather than a company-wide administrative report.

| Attribute | Detail |
| --- | --- |
| Responsibilities | Set role expectations, complete manager-owned tasks, monitor new-hire readiness, assign mentors, and remove team-specific blockers. |
| Primary Goals | Know which team members need action this week; understand which tasks or access issues are delaying readiness; compare team progress against organizational expectations. |
| Frustrations | Learns about incomplete onboarding late; has no clear list of pending manager actions; cannot differentiate normal ramp-up from an employee at risk. |
| Technical Comfort | Medium. Uses operational tools regularly and values concise charts, drill-down details, and actionable lists. |
| Success Metrics | Median time-to-productivity for team hires; overdue manager actions; completion of role-specific training; new-hire pulse feedback. |

## 3.3 Persona 3 — The HR Operations Analyst

Name: Sofia Ramirez | Role: HR Operations Analyst

Background: Sofia prepares recurring onboarding reports and maintains operational data quality. She extracts data from HR, ticketing, and learning tools, normalizes records, identifies exceptions, and supports leaders with analysis. Her role is central to ensuring that process changes are based on reliable evidence.

| Attribute | Detail |
| --- | --- |
| Responsibilities | Maintain reporting datasets, reconcile records, validate KPIs, investigate anomalies, prepare executive reporting, and document process performance. |
| Primary Goals | Automate report generation; trust data lineage and definitions; compare cohorts and departments; perform deeper analysis without repeated data preparation. |
| Frustrations | Manual data cleaning is repetitive; employee identifiers do not always match across sources; metric definitions vary between stakeholders. |
| Technical Comfort | High. Comfortable with Excel, Power BI, SQL concepts, data-quality checks, and structured exports. |
| Success Metrics | Reporting cycle time; data-quality pass rate; percentage of reports generated without manual reconciliation; stakeholder confidence in metrics. |

## 3.4 Persona 4 — Executive Leadership

Name: Aisha Thompson | Role: Chief Operating Officer

Background: Aisha is accountable for organizational operating health, workforce readiness, and scaling processes as headcount grows. She does not need task-level detail during routine review, but she requires a trustworthy high-level narrative: whether onboarding is healthy, what is changing, where risks concentrate, and what leadership action is required.

| Attribute | Detail |
| --- | --- |
| Responsibilities | Review organizational performance, allocate operational resources, sponsor cross-functional improvements, and assess people-program outcomes. |
| Primary Goals | Receive a clear onboarding health summary; see trends and department variance; understand material risks and recommended action; assess whether investments improve outcomes. |
| Frustrations | Existing reports are backward-looking, overly detailed, and inconsistent; leadership discussions focus on anecdotes rather than comparable metrics. |
| Technical Comfort | Low to medium. Expects intuitive dashboards, plain-language insight, and concise downloadable reports. |
| Success Metrics | First-month retention; company onboarding health score; reduction in high-risk cohorts; leadership report preparation time; manager satisfaction. |

## 3.5 Persona 5 — The Data Analyst / Data Engineer

Name: Ethan Brooks | Role: People Data Analyst / Data Engineer

Background: Ethan builds and maintains the analytical workflow underlying HR reporting. He is responsible for ingestion reliability, dataset contracts, transformation logic, and repeatable model training. For the capstone MVP, he uses CSV-based sources and a local or hosted analytical environment.

| Attribute | Detail |
| --- | --- |
| Responsibilities | Maintain pipelines, enforce schema rules, implement transformations, monitor quality, publish processed datasets, and validate model outputs. |
| Primary Goals | Run the pipeline reliably; diagnose bad source data; ensure calculations are reproducible; make the architecture easy to extend. |
| Frustrations | Source schemas evolve without warning; missing or duplicate records create inconsistent dashboards; manual steps make results difficult to audit. |
| Technical Comfort | Very high. Proficient with Python, SQL, Pandas, testing, Git, and CI workflows. |
| Success Metrics | Pipeline success rate; validation pass rate; processing time; test coverage; number of manual interventions required. |

# 4\. User Pain Points

| \# | Persona | Pain Point | Severity |
| --- | --- | --- | --- |
| P1 | HR Manager | No unified view shows each new hire’s progress, support dependencies, learning status, and tool adoption together. | Critical |
| P2 | Department Manager | Managers do not know which onboarding stage or owner is responsible when a new hire falls behind. | Critical |
| P3 | HR Operations Analyst | Recurring reports require manual extraction, cleaning, matching, and consolidation across disconnected files. | Critical |
| P4 | Executive Leadership | Leadership cannot see whether onboarding performance is improving, deteriorating, or varying materially by department. | High |
| P5 | HR Manager | Employees can remain stuck in a stage for days before the problem becomes visible to the right owner. | Critical |
| P6 | Department Manager | There is no practical productivity-readiness signal beyond subjective manager feedback. | High |
| P7 | HR Operations Analyst | KPI definitions and department labels are inconsistent, undermining trust in reports. | High |
| P8 | All Personas | Separate HR, learning, support, and collaboration tools create multiple versions of the truth. | Critical |
| P9 | Executive Leadership | Executive reporting is difficult to prepare and lacks concise risk explanations or recommended action. | High |
| P10 | HR Manager | Support-ticket volume is visible, but its connection to delayed onboarding is not measurable. | High |
| P11 | Department Manager | Managers lack a prioritized list of pending actions and cannot identify employees likely to miss completion targets. | High |
| P12 | HR Operations Analyst | There is no predictive analytics capability to identify at-risk employees or unusual process failure patterns. | Medium |

# 5\. Project Goals

## 5.1 Primary Goals

| Goal | Description |
| --- | --- |
| G1 — Unified Onboarding Analytics | Create a governed analytical view that joins core employee, onboarding, learning, tool-usage, and support-ticket records using documented keys and transformation rules. |
| G2 — Onboarding Progress Visibility | Give HR and managers timely visibility into completion status, current stage, overdue tasks, and pending dependencies at employee, cohort, and department level. |
| G3 — Bottleneck Identification | Quantify where onboarding delays occur and connect delay patterns to task types, support categories, managers, departments, locations, and employment types. |
| G4 — Productivity Tracking | Establish explainable productivity proxies, such as required tool adoption, training readiness, checklist completion, and manager-confirmed readiness, to measure time-to-productivity. |
| G5 — KPI Reporting | Provide consistent, exportable KPIs for onboarding completion, completion time, task completion, training performance, support resolution, and risk distribution. |
| G6 — Predictive Onboarding Analysis | Use appropriate baseline machine learning models to predict delayed completion, calculate risk scores, and identify unusual onboarding patterns. |
| G7 — Data-Driven HR Decisions | Replace spreadsheet-driven periodic reporting with repeatable dashboards and evidence-based intervention lists. |

## 5.2 Secondary Goals

| Goal | Description |
| --- | --- |
| G8 — Executive Reporting | Provide an executive-ready overview with trend direction, departmental comparison, risk alerts, and concise recommendations. |
| G9 — Reusable Analytics Architecture | Build modular ingestion, cleaning, integration, KPI, analytics, and ML components that can be extended to live sources later. |
| G10 — Better Employee Experience | Help operational owners detect and remove friction earlier, reducing uncertainty and avoidable delays for new hires. |
| G11 — Faster Onboarding Cycles | Establish a measurement baseline and identify the highest-impact opportunities to reduce time-to-productivity. |
| G12 — Scalable Reporting | Produce CSV and Power BI-compatible outputs so stakeholders can reuse validated data without recreating business logic. |

## 5.3 Non-Goals

The MVP will not replace an HRIS, learning management system, ticketing system, or onboarding workflow tool. It does not create, assign, approve, or complete employee tasks. The MVP also excludes authentication and role-based access control, because it is designed for controlled capstone demonstration data rather than production employee access. Finally, the product does not attempt to make employment, promotion, compensation, or disciplinary decisions; model outputs are operational signals that require human review.

# 6\. Dataset & Data Source Documentation

The MVP assumes anonymized or synthetic CSV datasets. Each source is validated before it enters the processed layer. Records that fail validation are isolated in an error output with a reason code; they are not silently discarded or allowed to corrupt KPI calculations.

| Data Source | Owner | Purpose | Refresh Rate |
| --- | --- | --- | --- |
| Employee Dataset | HR Operations | Employee and organizational context | Weekly or on hiring-event update |
| Onboarding Progress Dataset | HR / People Operations | Task, stage, due-date, and completion progress | Daily |
| Internal Tool Usage Dataset | IT / Platform Operations | Adoption signals for required internal tools | Daily |
| Support Ticket Dataset | IT Service Desk / HR Support | Access and support friction indicators | Daily |
| Learning Management Dataset | Learning & Development | Mandatory and role-specific learning progress | Daily |

## 6.1 Employee Dataset

The employee dataset is the master dimension for new-hire analysis. It defines the employee identifier used to relate records and supplies cohort dimensions needed for fair comparison. It must contain only MVP-approved, de-identified fields and should not include compensation, protected characteristics, or sensitive personal details.

| Field | Type | Description | Validation |
| --- | --- | --- | --- |
| employee_id | VARCHAR(50) | Unique employee identifier | Required; unique; non-null |
| department | VARCHAR(100) | Organizational department | Required; mapped to controlled list |
| manager_id | VARCHAR(50) | Direct manager identifier | Required where applicable |
| joining_date | DATE | Employee start date | Required; valid date; not future-dated beyond approved data window |
| role | VARCHAR(100) | Job role or role family | Required; normalized label |
| location | VARCHAR(100) | Work location or region | Required; normalized label |
| employment_type | VARCHAR(30) | Full-time, part-time, contractor, intern | Required; controlled values |
| onboarding_cohort | VARCHAR(20) | Derived joining-month cohort | Derived from joining_date |

Owner: HR Operations. Refresh frequency: weekly or event-based. Data quality checks include unique employee IDs, valid organizational mappings, non-null joining date, and referential integrity for manager IDs when a manager record is supplied.

## 6.2 Onboarding Progress Dataset

This dataset captures the structured onboarding checklist and stage progression. A single employee can have many task records. The pipeline aggregates task-level records into employee-level completion and stage metrics while retaining task-level detail for bottleneck analysis.

| Field | Type | Description | Validation |
| --- | --- | --- | --- |
| onboarding_task_id | VARCHAR(50) | Unique checklist task record | Required; unique |
| employee_id | VARCHAR(50) | Link to employee dataset | Required; must match employee dimension |
| task_name | VARCHAR(150) | Human-readable task title | Required |
| task_category | VARCHAR(80) | HR, IT, manager, compliance, role-specific | Required; controlled values |
| current_stage | VARCHAR(50) | Preboarding, setup, orientation, enablement, productive | Required; controlled sequence |
| task_status | VARCHAR(30) | Not Started, In Progress, Complete, Blocked, Overdue | Required; controlled values |
| due_date | DATE | Expected completion date | Required for mandatory tasks |
| completed_date | DATE | Actual completion date | Null only when incomplete |
| completion_percentage | DECIMAL(5,2) | Employee or task completion indicator | Must be 0–100 |

Owner: People Operations. Refresh frequency: daily. Data quality checks include valid status transitions, completion dates not preceding joining dates, completed tasks having a completion date, and percentage values within range.

## 6.3 Internal Tool Usage Dataset

Tool-usage data provides a limited, privacy-conscious adoption signal. The MVP uses aggregate daily activity indicators rather than message content, file content, or individual surveillance. Usage is interpreted as a productivity proxy only in combination with task, training, and support data.

| Field | Type | Description | Validation |
| --- | --- | --- | --- |
| usage_id | VARCHAR(50) | Unique daily usage record | Required; unique |
| employee_id | VARCHAR(50) | Link to employee dataset | Required; valid foreign key |
| usage_date | DATE | Activity date | Required; valid date |
| slack_activity_count | INTEGER | Aggregate collaboration interactions | Non-negative |
| jira_usage_count | INTEGER | Aggregate issue/project activity | Non-negative |
| github_activity_count | INTEGER | Aggregate code/repository activity where role-appropriate | Non-negative |
| teams_activity_count | INTEGER | Aggregate Microsoft Teams interactions | Non-negative |
| workspace_activity_count | INTEGER | Aggregate Google Workspace activity | Non-negative |
| daily_active_usage | BOOLEAN | Whether minimum tool-adoption threshold was met | Required |

Owner: IT / Platform Operations. Refresh frequency: daily. Data quality checks include non-negative counts, one record per employee per date per source grain, role-aware handling of tools not required for all employees, and an approved retention approach for de-identified analytics data.

## 6.4 Support Ticket Dataset

Support-ticket data explains friction encountered during onboarding, including account provisioning, equipment, access, HR policy, and learning issues. The dataset must not include ticket body text in the MVP; only structured metadata is required.

| Field | Type | Description | Validation |
| --- | --- | --- | --- |
| ticket_id | VARCHAR(50) | Unique support ticket ID | Required; unique |
| employee_id | VARCHAR(50) | Requester / affected employee | Required; valid foreign key |
| created_date | DATETIME | Ticket creation timestamp | Required; valid timestamp |
| issue_category | VARCHAR(80) | Access, hardware, payroll, HR policy, learning, other | Required; controlled values |
| priority | VARCHAR(20) | Low, Medium, High, Critical | Required; controlled values |
| resolution_time_hours | DECIMAL(10,2) | Hours from creation to resolution | Non-negative if resolved |
| assigned_team | VARCHAR(100) | Responsible support team | Required |
| status | VARCHAR(30) | Open, In Progress, Resolved, Closed | Required; controlled values |

Owner: IT Service Desk / HR Support. Refresh frequency: daily. Quality checks include valid lifecycle timestamps, no negative resolution durations, required category and priority, and association with an employee included in the eligible onboarding cohort.

## 6.5 Learning Management Dataset

Learning data establishes whether mandatory compliance and role-specific enablement are complete. It supports comparisons between learning completion, assessment performance, onboarding stage, and time-to-productivity.

| Field | Type | Description | Validation |
| --- | --- | --- | --- |
| learning_record_id | VARCHAR(50) | Unique learning assignment record | Required; unique |
| employee_id | VARCHAR(50) | Link to employee dataset | Required; valid foreign key |
| course_name | VARCHAR(150) | Course title | Required |
| course_type | VARCHAR(50) | Compliance, orientation, role-specific, optional | Required; controlled values |
| assigned_date | DATE | Date assigned | Required |
| completed_date | DATE | Completion date | Null until completed |
| assessment_score | DECIMAL(5,2) | Assessment result where applicable | 0–100 or null when not assessed |
| completion_time_hours | DECIMAL(10,2) | Time to complete assignment | Non-negative when complete |
| course_status | VARCHAR(30) | Assigned, In Progress, Completed, Overdue | Required; controlled values |

Owner: Learning and Development. Refresh frequency: daily. Quality checks include valid assignment/completion order, course-status consistency, scores in range, and removal of duplicate assignment records.

## 6.6 Cross-Source Data Quality and Integration Rules

All sources must be validated against the schema contracts in Appendix B. Employee ID is the primary integration key. The analytical pipeline must create a data-quality report showing record counts, rejected-record counts, duplicate counts, null rates for critical fields, and referential-integrity failures. Department, role, location, task category, and support category values will be standardized through reference mappings. The processed analytical layer will retain source lineage and refresh timestamp so a stakeholder can identify the source and run that produced a metric.

# 7\. Success Metrics

## 7.1 Product Metrics (KPIs)

| Metric | Target | Measurement Method |
| --- | --- | --- |
| Average onboarding completion time | Establish baseline in MVP; demonstrate ability to measure by cohort and department | Days from joining date to mandatory-task completion |
| Average time-to-productivity | Establish baseline; show role/department comparison | Days until defined productivity-readiness threshold is met |
| Onboarding completion rate | ≥ 90% of eligible employees complete mandatory tasks within target window in sample scenario | Completed mandatory tasks / eligible employees |
| At-risk employee identification precision | ≥ 75% on labeled or simulated holdout data | Precision of high-risk classification |
| Dashboard load time | < 3 seconds for standard sample dataset | Timed functional test |
| Data freshness | Daily processed output with < 1% rejected records due to non-source errors | Pipeline log and quality report |
| Insight generation time | < 10 seconds for filtered bottleneck or risk view | UI performance test |

## 7.2 Business Metrics

| Metric | Target | Measurement Method |
| --- | --- | --- |
| Reduction in manual reporting effort | ≥ 60% reduction against documented baseline | HR Operations time study |
| Reduction in avoidable onboarding delays | ≥ 20% improvement target after process intervention; MVP establishes baseline | Cohort comparison after intervention |
| Manager satisfaction with onboarding visibility | ≥ 4.0/5 in evaluation survey | Post-demo or pilot survey |
| First-30-day onboarding completion | ≥ 90% in modeled target state | Completion dashboard |
| Support-related delay resolution | ≥ 15% reduction target in median time to resolve onboarding-critical tickets | Ticket analytics |

## 7.3 Technical Metrics

| Metric | Target | Measurement Method |
| --- | --- | --- |
| Pipeline success rate | ≥ 95% across scheduled/demo runs | Pipeline run logs |
| Schema validation pass rate | 100% for records admitted to processed layer | Validation report |
| Model performance | Delay model F1 ≥ 0.75 where labeled data supports evaluation | Held-out evaluation dataset |
| Code coverage | ≥ 80% for core pipeline, KPI, and utility modules | pytest coverage report |
| CI success rate | ≥ 95% on protected branch builds | GitHub Actions history |
| Dashboard error rate | 0 unhandled errors in acceptance test scenarios | Test script and logs |

# 8\. Functional Requirements

## 8.1 Data Ingestion Module

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-01 | The system SHALL ingest the employee dataset from a configured CSV file and validate the required employee fields before processing. | Must Have |
| FR-02 | The system SHALL ingest onboarding progress records from CSV and retain task-level identifiers for traceability. | Must Have |
| FR-03 | The system SHALL ingest daily internal tool-usage records from CSV. | Must Have |
| FR-04 | The system SHALL ingest structured support-ticket records from CSV. | Must Have |
| FR-05 | The system SHALL ingest learning management records from CSV. | Must Have |
| FR-06 | The system SHALL validate headers, data types, required fields, controlled values, and primary-key uniqueness for each source. | Must Have |
| FR-07 | The system SHALL produce a rejected-record log containing source, row identifier, validation reason, and pipeline-run timestamp. | Must Have |
| FR-08 | The system SHALL record ingestion counts, accepted counts, rejected counts, and execution status for each dataset. | Must Have |

## 8.2 Data Cleaning and Integration Module

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-09 | The system SHALL standardize date formats, department labels, role labels, task categories, support categories, and status values using documented mappings. | Must Have |
| FR-10 | The system SHALL detect and remove duplicate source records using dataset-specific primary keys. | Must Have |
| FR-11 | The system SHALL apply documented missing-value handling rules without fabricating values for critical identifiers or dates. | Must Have |
| FR-12 | The system SHALL verify referential integrity between each operational dataset and the employee dimension. | Must Have |
| FR-13 | The system SHALL create a unified employee onboarding fact table at employee-date or employee-snapshot grain. | Must Have |
| FR-14 | The system SHALL create supporting task-, ticket-, learning-, and tool-usage-level analytical tables for drill-down analysis. | Must Have |
| FR-15 | The system SHALL calculate a data-quality summary for each pipeline run. | Must Have |
| FR-16 | The system SHALL write processed datasets and quality outputs to configured output paths. | Must Have |

## 8.3 KPI and Analytics Engine

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-17 | The system SHALL calculate onboarding completion percentage for each eligible employee. | Must Have |
| FR-18 | The system SHALL calculate average and median onboarding completion time by cohort, department, manager, role, location, and employment type. | Must Have |
| FR-19 | The system SHALL calculate mandatory-task completion, overdue-task rate, and blocked-task rate. | Must Have |
| FR-20 | The system SHALL calculate training completion, average assessment score, and average learning completion time. | Must Have |
| FR-21 | The system SHALL calculate support-ticket volume, median resolution time, open-ticket rate, and issue-category distribution for new hires. | Must Have |
| FR-22 | The system SHALL calculate role-aware internal tool-adoption and daily-active-usage indicators. | Must Have |
| FR-23 | The system SHALL calculate a documented productivity-readiness score from approved completion, learning, tool-adoption, and support signals. | Should Have |
| FR-24 | The system SHALL calculate week-over-week and month-over-month changes for major onboarding KPIs. | Must Have |
| FR-25 | The system SHALL identify the top bottleneck stages, tasks, and support categories by delay impact. | Must Have |
| FR-26 | The system SHALL support SQL-powered cohort, department, manager, and date-range analysis against processed data. | Must Have |

## 8.4 Machine Learning Module

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-27 | The system SHALL train a baseline onboarding-completion prediction model using eligible historical or simulated employee records. | Must Have |
| FR-28 | The system SHALL produce an employee-level risk score indicating likelihood of delayed onboarding completion. | Must Have |
| FR-29 | The system SHALL classify risk into Low, Medium, and High bands using documented thresholds. | Must Have |
| FR-30 | The system SHALL train a delay-prediction model estimating the likelihood that an employee will miss a target completion date. | Should Have |
| FR-31 | The system SHALL segment employees or cohorts into analytically meaningful onboarding patterns using clustering where data supports it. | Could Have |
| FR-32 | The system SHALL detect anomalous onboarding patterns, such as unusual ticket volume, stalled progression, or low tool adoption relative to comparable peers. | Should Have |
| FR-33 | The system SHALL forecast department-level productivity-readiness trends over a short planning horizon when sufficient history is available. | Could Have |
| FR-34 | The system SHALL generate rule-based intervention recommendations using identified risk drivers and bottlenecks. | Must Have |
| FR-35 | The system SHALL store model type, training date, features, evaluation metrics, and serialized artifact location for each trained model. | Must Have |
| FR-36 | The system SHALL display model confidence or explanation fields appropriate to the selected baseline model. | Should Have |

## 8.5 Dashboard Module

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-37 | The dashboard SHALL provide a landing page that summarizes data freshness, company onboarding health, and available views. | Must Have |
| FR-38 | The dashboard SHALL provide an Executive Dashboard with company-level KPIs, trends, department comparison, and risk alerts. | Must Have |
| FR-39 | The dashboard SHALL provide an HR Dashboard with funnel, task, training, pending-employee, and support analytics. | Must Have |
| FR-40 | The dashboard SHALL provide a Manager Dashboard with team progress, employee-level status, pending actions, and risk prioritization. | Must Have |
| FR-41 | The dashboard SHALL provide an Analytics Dashboard with trend, correlation, heatmap, department-comparison, and support views. | Must Have |
| FR-42 | The dashboard SHALL support date range, department, manager, location, role, employment type, and onboarding-cohort filters where applicable. | Must Have |
| FR-43 | The dashboard SHALL apply global filters consistently to charts, tables, KPI cards, and exports within a view. | Must Have |
| FR-44 | The dashboard SHALL allow drill-down from aggregate metrics to the relevant employee, task, ticket, or course detail table. | Should Have |
| FR-45 | The dashboard SHALL display data freshness and last successful pipeline-run timestamp. | Must Have |
| FR-46 | The dashboard SHALL visually distinguish high-risk employees, overdue tasks, and persistent support issues without relying on color alone. | Must Have |

## 8.6 Reporting, Export, and Notifications Module

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-47 | The system SHALL generate a downloadable CSV export for displayed summary and detail tables. | Must Have |
| FR-48 | The system SHALL generate an executive onboarding summary report in Markdown or PDF-ready format. | Should Have |
| FR-49 | The system SHALL produce Power BI-compatible processed exports with stable column names and documented metric definitions. | Should Have |
| FR-50 | The system SHALL generate a department onboarding health report containing KPIs, risk distribution, and top bottlenecks. | Should Have |
| FR-51 | The system SHALL generate a manager action report listing high-risk employees, overdue actions, and associated reasons. | Must Have |
| FR-52 | The system SHALL support a simulated in-app notification list for new high-risk employees or threshold breaches. | Could Have |

## 8.7 Administration and Observability Module

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-53 | The system SHALL run ingestion, cleaning, integration, KPI generation, and model scoring through a single documented pipeline command. | Must Have |
| FR-54 | The system SHALL log pipeline start time, completion time, module status, record counts, and errors. | Must Have |
| FR-55 | The system SHALL expose configuration for file paths, target thresholds, and output locations without source-code modification. | Must Have |
| FR-56 | The system SHALL retain versioned metric definitions and transformation assumptions in repository documentation. | Must Have |
| FR-57 | The system SHALL provide automated unit tests for critical transformations, metric calculations, and schema validations. | Must Have |
| FR-58 | The system SHALL execute linting, tests, and validation checks through GitHub Actions on pushes and pull requests. | Must Have |

# 9\. Non-Functional Requirements

## 9.1 Performance

| ID | Requirement |
| --- | --- |
| NFR-01 | The dashboard must load an initial view within 3 seconds on a standard laptop using the reference sample dataset. |
| NFR-02 | A filtered dashboard interaction must update visible components within 2 seconds for the reference dataset. |
| NFR-03 | The complete pipeline must process one year of daily sample records within 5 minutes. |
| NFR-04 | Model inference for a selected employee or cohort must return within 2 seconds after processed data is available. |

## 9.2 Reliability

| ID | Requirement |
| --- | --- |
| NFR-05 | Malformed records must be quarantined and logged without causing the entire ingestion pipeline to fail. |
| NFR-06 | Pipeline failures must produce descriptive logs that identify the failing module and actionable reason. |
| NFR-07 | The system must avoid publishing partially processed datasets as a successful run. |
| NFR-08 | The demo deployment must maintain 99% availability during planned evaluation windows, excluding announced maintenance. |

## 9.3 Scalability

| ID | Requirement |
| --- | --- |
| NFR-09 | The data model must support at least 10,000 employees and 24 months of daily aggregated records without redesign. |
| NFR-10 | Processing components must be modular so CSV ingestion can later be replaced or supplemented by API and cloud-storage connectors. |
| NFR-11 | Dashboard tables must use aggregation, filtering, or pagination to avoid rendering unbounded detail rows. |

## 9.4 Maintainability

| ID | Requirement |
| --- | --- |
| NFR-12 | Python code must follow PEP 8 conventions and use clear module boundaries for ingestion, transformation, analytics, modeling, and presentation. |
| NFR-13 | Public functions and modules must include docstrings describing purpose, inputs, outputs, and error behavior. |
| NFR-14 | Core modules must achieve at least 80% unit-test coverage. |
| NFR-15 | GitHub Actions must run linting, unit tests, and schema-validation checks on pushes and pull requests. |

## 9.5 Availability and Portability

| ID | Requirement |
| --- | --- |
| NFR-16 | The application must run on a machine with Python 3.10+ using dependencies specified in requirements.txt. |
| NFR-17 | File paths, thresholds, and environment-specific settings must be configurable through a configuration file or environment variables. |
| NFR-18 | The project must provide reproducible setup and execution instructions in README documentation. |

## 9.6 Security and Privacy

| ID | Requirement |
| --- | --- |
| NFR-19 | The repository must not contain real employee PII, credentials, secrets, or production exports. |
| NFR-20 | The MVP must use anonymized or synthetic identifiers and aggregate tool-usage signals only. |
| NFR-21 | Sensitive configuration must use environment variables or excluded .env files rather than source control. |
| NFR-22 | Model outputs must be presented as operational decision-support signals and must not be used for automated employment decisions. |

## 9.7 Usability and Accessibility

| ID | Requirement |
| --- | --- |
| NFR-23 | A non-technical HR or executive user must be able to understand primary KPIs and filter a dashboard without training. |
| NFR-24 | Every chart must include a descriptive title, labeled axes where applicable, readable legends, and tooltips or accessible accompanying tables. |
| NFR-25 | Status must not be communicated by color alone; icons, labels, or text must accompany risk colors. |
| NFR-26 | The dashboard must use responsive layouts suitable for standard laptop and tablet-width viewing. |

## 9.8 Compliance

| ID | Requirement |
| --- | --- |
| NFR-27 | The MVP documentation must state data purpose, source ownership, retention assumptions, and limitations of productivity proxies. |
| NFR-28 | Access-control and legal-review requirements for production data are explicitly deferred and documented as prerequisites for production deployment. |
| NFR-29 | Data-processing logic must preserve auditable lineage from dashboard metrics to processed source records. |

