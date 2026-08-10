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
| Tech Stack | Python · Pandas · NumPy · SQLite · Streamlit · Plotly · Git · GitHub |

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

Built as an enterprise-style onboarding analytics platform using **Python, Pandas, NumPy, SQLite, Streamlit, and Plotly**, the system transforms fragmented onboarding data into actionable operational insights. The platform provides:

* A consolidated onboarding dataset that integrates employee records, onboarding tasks, learning progress, internal tool usage, and support ticket history.

* Executive, HR, and department-level dashboards for monitoring onboarding health, productivity trends, completion rates, and operational bottlenecks.

* Automated KPI calculations including onboarding completion rate, average onboarding duration, time-to-productivity, **Productivity Score**, **Friction Score**, and **Onboarding Health Score**.

* Interactive analytics that identify bottlenecks by department, role, manager, onboarding stage, location, and support issue category.

* A rule-based recommendation engine that detects at-risk employees, highlights operational friction points, and provides transparent, evidence-based recommendations supported by the underlying data.

* Downloadable executive reports in PDF and CSV formats, enabling faster leadership reviews, standardized operational reporting, and data-driven decision-making.

The MVP focuses on **analytics and decision support rather than workflow automation**. It imports governed CSV datasets, performs automated validation, data cleaning, schema harmonization, integration, KPI generation, and rule-based analysis before presenting actionable insights through an interactive **Streamlit** dashboard. To keep the scope achievable within the 20-day sprint, the platform intentionally excludes authentication, employee self-service, live HRIS integrations, real-time data streaming, and predictive machine learning, while providing a modular architecture that can support these enterprise capabilities in future releases.

# 2\. Business Problem

## 2.1 Context

For a growing startup, the first month of employment is a critical period. New hires must complete mandatory paperwork, obtain equipment and system access, meet their manager and team, complete training, understand priorities, and begin contributing. The organization already records much of this activity, but the evidence is fragmented. HR may own the employee roster and checklist, IT owns access and hardware tickets, Learning and Development owns course completion, department managers track role readiness, and collaboration platforms contain indirect signals of adoption.

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

The employee dataset is the master dimension for new-hire analysis. It defines the employee identifier used to relate records across all analytical datasets and provides organizational attributes required for segmentation and cohort analysis. The raw HR dataset contains additional employee information; however, only MVP-approved, de-identified fields are retained in the processed analytical layer. Sensitive personal information such as employee names, salary, demographic attributes, and other non-essential HR fields are excluded during preprocessing to support privacy-conscious analytics.

| Field | Type | Description | Validation |
| --- | --- | --- | --- |
| employee_id | VARCHAR(50) | Unique employee identifier | Required; unique; non-null |
| department | VARCHAR(100) | Organizational department | Required; mapped to controlled list |
| manager_id | VARCHAR(50) | Direct manager identifier | Required where applicable; valid reference |
| joining_date | DATE | Employee hiring date | Required; valid date; not future-dated |
| role | VARCHAR(100) | Employee job position or role | Required; normalized label |
| location | VARCHAR(100) | Employee work location (state/region) | Required; normalized label |
| employment_status | VARCHAR(30) | Current employment status (e.g., Active, Leave of Absence, Voluntarily Terminated, Terminated for Cause) | Required; controlled values |
| onboarding_cohort | VARCHAR(20) | Joining-month cohort used for trend analysis | Derived from joining_date |

**Owner:** HR Operations

**Refresh Frequency:** Weekly or event-based

**Data Quality Checks:**
- Unique and non-null employee identifiers.
- Valid department and role mappings.
- Non-null and valid hiring dates.
- Standardized location values.
- Controlled employment-status values.
- Referential integrity for manager IDs where applicable.
- Derivation and validation of onboarding cohorts from hiring dates.

**Preprocessing Note:**  
The source HR dataset includes additional attributes such as employee name, salary, demographic information, recruitment source, performance metrics, and termination details. These fields are intentionally excluded from the processed employee dataset because they are outside the scope of the MVP and are not required for onboarding analytics. The processed employee dataset retains only the fields necessary for data integration, cohort analysis, and dashboard reporting.

## 6.2 Onboarding Progress Dataset

The Onboarding Progress Dataset captures structured onboarding checklist tasks and stage progression for employees in the eligible onboarding cohort. A single employee can have multiple task records. The dataset is synthetically generated for the MVP using the finalized Employee Dataset as the employee master, ensuring that `employee_id` values can be integrated across sources.

The dataset is maintained at task level so that the analytical pipeline can calculate employee-level completion, stage progression, overdue tasks, blocked tasks, and onboarding bottlenecks while retaining the underlying task-level detail.

**Source:** Synthetic CSV dataset generated for the MVP using the finalized Employee Dataset as the employee reference.

**Record grain:** One onboarding task assigned to one employee.

**Approximate dataset size:** 4,222 task records across 311 employees.

| Field | Type | Description | Validation |
| --- | --- | --- | --- |
| onboarding_task_id | VARCHAR(50) | Unique onboarding checklist task record | Required; unique; non-null |
| employee_id | VARCHAR(50) | Employee identifier linked to Employee Dataset | Required; valid foreign key |
| task_name | VARCHAR(150) | Human-readable onboarding task title | Required; non-null |
| task_category | VARCHAR(80) | HR, IT, Manager, Compliance, or Role-specific task category | Required; controlled values |
| current_stage | VARCHAR(50) | Preboarding, Setup, Orientation, Enablement, or Productive stage | Required; controlled sequence |
| task_status | VARCHAR(30) | Not Started, In Progress, Complete, Blocked, or Overdue | Required; controlled values |
| due_date | DATE | Expected task completion date | Required; valid date |
| completed_date | DATE | Actual completion date | Required when task is Complete; null otherwise |
| completion_percentage | DECIMAL(5,2) | Percentage of task completion | Required; value between 0 and 100 |

Owner: People Operations. Refresh frequency: Daily in the target MVP operating model. The current implementation uses a synthetic static CSV to represent the source.

Data quality checks include unique onboarding task IDs, valid employee foreign keys, valid task categories and stages, valid status values, completion percentages between 0 and 100, completed tasks having a completion date, incomplete tasks not having a completion date, and completion dates not preceding the employee joining date.

The dataset will be retained in the raw layer without modification. Validation, standardization, and derived employee-level onboarding metrics will be performed during processing.

---

## 6.3 Internal Tool Usage Dataset

The Internal Tool Usage Dataset provides privacy-conscious aggregate indicators of employee adoption of required internal tools during the onboarding period. The MVP does not collect message content, document content, source-code content, or other detailed surveillance information. Only aggregate activity counts are retained.

The dataset is synthetically generated for the MVP using the finalized Employee Dataset as the employee reference. Activity patterns are role- and department-aware so that tools that are not relevant to a particular role can have lower or zero activity.

**Source:** Synthetic CSV dataset generated for the MVP using the finalized Employee Dataset as the employee reference. The dataset represents aggregated daily activity indicators rather than actual production employee surveillance data.

**Record grain:** One employee per usage date.

**Approximate dataset size:** 13,995 daily usage records covering 311 employees across a 45-day onboarding activity window.

| Field | Type | Description | Validation |
| --- | --- | --- | --- |
| usage_id | VARCHAR(50) | Unique daily usage record | Required; unique; non-null |
| employee_id | VARCHAR(50) | Employee identifier linked to Employee Dataset | Required; valid foreign key |
| usage_date | DATE | Date on which tool activity was recorded | Required; valid date |
| slack_activity_count | INTEGER | Aggregate Slack collaboration activity indicator | Required; non-negative |
| jira_usage_count | INTEGER | Aggregate Jira issue/project activity indicator | Required; non-negative |
| github_activity_count | INTEGER | Aggregate GitHub repository/code activity indicator where role-appropriate | Required; non-negative |
| teams_activity_count | INTEGER | Aggregate Microsoft Teams activity indicator | Required; non-negative |
| workspace_activity_count | INTEGER | Aggregate Google Workspace activity indicator | Required; non-negative |
| daily_active_usage | BOOLEAN | Indicates whether the employee met the defined daily tool-adoption threshold | Required; TRUE or FALSE |

Owner: IT / Platform Operations. Refresh frequency: Daily in the target MVP operating model. The current implementation uses a synthetic static CSV to represent the source.

Data quality checks include unique usage IDs, valid employee foreign keys, valid usage dates, non-negative activity counts, one record per employee per usage date, and valid boolean values for `daily_active_usage`.

Tool activity will be interpreted only as a productivity-readiness proxy and will not be treated as a direct employee performance measure. Role-aware tool requirements will be applied during processing so that the absence of activity on a tool that is not required for a particular role does not incorrectly reduce an employee's adoption score.

The dataset will be retained in the raw layer without modification. Cleaning, validation, role-aware standardization, and derived adoption metrics will be performed during processing.

---

## 6.4 Support Ticket Dataset

The Support Ticket Dataset captures structured support friction encountered by employees during onboarding. It covers issues such as account access, hardware provisioning, payroll setup, HR policy questions, learning access, and other onboarding-related support requests.

The MVP does not retain ticket body text or other unstructured message content. Only structured ticket metadata required for onboarding friction analysis is included.

The dataset is synthetically generated for the MVP using the finalized Employee Dataset as the employee reference. Its structure and support-ticket categories are based on the public **Help Desk Tickets** dataset published through Mendeley Data, which provides a reference structure for help-desk ticket categories, priorities, assignment information, and resolution data.

**Reference source:** Public Help Desk Tickets dataset, Mendeley Data, used as a structural and categorical reference.

**MVP source:** Synthetic employee-linked CSV dataset generated using the finalized Employee Dataset and the reference help-desk structure.

**Record grain:** One support ticket associated with one employee.

**Approximate dataset size:** 1,048 support tickets across 311 employees.

| Field | Type | Description | Validation |
| --- | --- | --- | --- |
| ticket_id | VARCHAR(50) | Unique support ticket identifier | Required; unique; non-null |
| employee_id | VARCHAR(50) | Requester or affected employee linked to Employee Dataset | Required; valid foreign key |
| created_date | DATETIME | Timestamp when the support ticket was created | Required; valid timestamp |
| issue_category | VARCHAR(80) | Access, Hardware, Payroll, HR policy, Learning, or Other | Required; controlled values |
| priority | VARCHAR(20) | Low, Medium, High, or Critical | Required; controlled values |
| resolution_time_hours | DECIMAL(10,2) | Hours from ticket creation to resolution | Non-negative when resolved; null when unresolved |
| assigned_team | VARCHAR(100) | Responsible support team | Required; non-null |
| status | VARCHAR(30) | Open, In Progress, Resolved, or Closed | Required; controlled values |

Owner: IT Service Desk / HR Support. Refresh frequency: Daily in the target MVP operating model. The current implementation uses a synthetic static CSV to represent the source.

Data quality checks include unique ticket IDs, valid employee foreign keys, valid ticket timestamps, controlled issue categories and priorities, non-negative resolution durations, consistency between ticket status and resolution time, and valid assigned-team values.

Ticket body text is intentionally excluded from the MVP to reduce privacy risk and keep the analysis focused on structured operational friction.

The dataset will be retained in the raw layer without modification. Validation, category standardization, resolution-time checks, and derived support-friction metrics will be performed during processing.

---

## 6.5 Learning Management Dataset

The Learning Management Dataset captures employee learning assignments and completion progress for mandatory compliance, orientation, role-specific enablement, and optional professional development activities.

The dataset is synthetically generated for the MVP using the finalized Employee Dataset as the employee reference. Each employee can have multiple learning records, allowing the analytical pipeline to calculate course completion, overdue learning, assessment performance, and learning progress alongside onboarding and tool-adoption metrics.

**Source:** Synthetic CSV dataset generated for the MVP using the finalized Employee Dataset as the employee reference.

**Record grain:** One learning assignment for one employee.

**Approximate dataset size:** 3,192 learning records across 311 employees.

| Field | Type | Description | Validation |
| --- | --- | --- | --- |
| learning_record_id | VARCHAR(50) | Unique learning assignment record | Required; unique; non-null |
| employee_id | VARCHAR(50) | Employee identifier linked to Employee Dataset | Required; valid foreign key |
| course_name | VARCHAR(150) | Assigned course or learning activity title | Required; non-null |
| course_type | VARCHAR(50) | Compliance, Orientation, Role-specific, or Optional | Required; controlled values |
| assigned_date | DATE | Date the learning activity was assigned | Required; valid date |
| completed_date | DATE | Date the learning activity was completed | Required when Completed; null otherwise |
| assessment_score | DECIMAL(5,2) | Assessment result where applicable | Null when not assessed; otherwise 0–100 |
| completion_time_hours | DECIMAL(10,2) | Time taken to complete the learning assignment | Non-negative when completed; null when incomplete |
| course_status | VARCHAR(30) | Assigned, In Progress, Completed, or Overdue | Required; controlled values |

Owner: Learning and Development. Refresh frequency: Daily in the target MVP operating model. The current implementation uses a synthetic static CSV to represent the source.

Data quality checks include unique learning record IDs, valid employee foreign keys, valid course types and statuses, valid assignment and completion dates, completed courses having completion dates, incomplete courses not having completion dates, assessment scores within the 0–100 range, and non-negative completion times.

Course status must remain consistent with completion information. For example, a record with `course_status = Completed` must contain a valid `completed_date`, while Assigned, In Progress, and Overdue records must not contain a completion date.

The dataset will be retained in the raw layer without modification. Cleaning, validation, duplicate detection, status standardization, and derived learning-completion metrics will be performed during processing.

---

## 6.6 Cross-Source Data Quality and Integration Rules

All five source datasets must be validated against the schema contracts defined in Appendix B before entering the processed analytical layer. The Employee Dataset acts as the master employee dimension and provides the primary integration key for all other datasets.

The integration model is:

```text
Employee Dataset
       |
       +--------------------+
       |                    |
       v                    v
Onboarding Progress     Tool Usage
       |                    |
       v                    v
Support Tickets        Learning Management

```

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

# 10\. User Stories

## Epic 1 — Executive Dashboard

### US-101

As an Executive Leader, I want to view a company-level onboarding health summary, so that I can understand whether new-hire readiness is improving and where leadership attention is required.

Acceptance Criteria:

* The view displays active new hires, completion rate, median completion time, productivity-readiness score, and high-risk count for the selected period.
* The view displays a monthly trend for completion and readiness.
* The view identifies the departments with the highest risk or largest negative variance.
* Each KPI displays a clear definition or tooltip and reflects the active filters.

### US-102

As an Executive Leader, I want to compare onboarding performance across departments, so that I can prioritize cross-functional operational investment.

Acceptance Criteria:

* A comparison table shows department, eligible hires, completion rate, median completion days, high-risk count, and support-delay indicator.
* The user can sort the table and select a department for drill-down.
* Variance from the company benchmark is displayed.

### US-103

As an Executive Leader, I want to see concise risk alerts with contributing factors, so that I can ask the appropriate leader to take action.

Acceptance Criteria:

* Alerts identify severity, affected department or cohort, affected employee count, and top contributing factor.
* Persistent issues are distinguishable from newly detected issues.
* Alerts link to the relevant HR or manager analysis view.

## Epic 2 — HR Dashboard

### US-201

As an HR Manager, I want to see an onboarding funnel by stage, so that I can identify where employees stop progressing.

Acceptance Criteria:

* The funnel shows counts and conversion rates across Preboarding, Setup, Orientation, Enablement, and Productive stages.
* The selected date range and organization filters are applied.
* The system highlights the stage with the largest drop-off or longest median duration.

### US-202

As an HR Manager, I want to view employees with incomplete or overdue mandatory tasks, so that I can coordinate timely follow-up.

Acceptance Criteria:

* A detail table shows employee, department, manager, current stage, overdue task count, due date, and risk band.
* The table can be filtered by task category and risk band.
* The user can export the filtered list to CSV.

### US-203

As an HR Manager, I want to analyze training completion and assessment outcomes, so that I can identify whether learning requirements are delaying readiness.

Acceptance Criteria:

* The dashboard shows course completion rate, overdue courses, average assessment score, and completion time.
* Results can be filtered by course type, department, and cohort.
* Overdue mandatory learning is visible in employee drill-down data.

### US-204

As an HR Manager, I want to see support issues associated with new hires, so that I can work with IT and HR support to remove recurring barriers.

Acceptance Criteria:

* The dashboard displays ticket volume, median resolution time, open-ticket count, and category distribution.
* The view identifies issue categories with the strongest association to delayed completion.
* No ticket body text or sensitive free-form content is displayed.

## Epic 3 — Manager Dashboard

### US-301

As a Department Manager, I want to see my team’s onboarding progress, so that I can ensure each new hire receives timely support.

Acceptance Criteria:

* The view defaults to the manager’s selected team in the demonstration workflow.
* It shows each new hire’s completion percentage, stage, readiness score, pending tasks, and open support tickets.
* Employees are sortable by risk and overdue actions.

### US-302

As a Department Manager, I want a prioritized list of actions assigned to me or my team, so that I can remove blockers before they affect productivity.

Acceptance Criteria:

* The action list identifies owner, employee, action type, due date, status, and impact rationale.
* Actions include manager check-ins, role-specific task completion, and escalation of blocked dependencies where supported by data.
* The list clearly distinguishes inferred recommendations from source-system task status.

### US-303

As a Department Manager, I want to compare my team’s onboarding outcomes with the company benchmark, so that I can understand whether my process needs improvement.

Acceptance Criteria:

* The dashboard compares completion time, readiness, overdue-task rate, and ticket-resolution time with company values.
* Comparisons include sample-size context to prevent misleading interpretation.
* The dashboard does not rank individual employees against peers.

## Epic 4 — Analytics and KPI Exploration

### US-401

As an HR Operations Analyst, I want to filter onboarding metrics by cohort, department, role, location, and employment type, so that I can investigate meaningful operational differences.

Acceptance Criteria:

* All supported filters are visible and their active state is clear.
* Filters update KPI cards, charts, tables, and exports consistently.
* Empty-result states explain that no records match the selected filters.

### US-402

As an HR Operations Analyst, I want to analyze the relationship between support delays and onboarding outcomes, so that I can make evidence-based process recommendations.

Acceptance Criteria:

* The platform displays a correlation or grouped comparison between ticket-resolution time and completion or readiness outcomes.
* The analysis clearly states that correlation does not prove causation.
* Users can inspect the underlying aggregated data.

### US-403

As an HR Operations Analyst, I want to use heatmaps and trends to locate recurring bottlenecks, so that I can prioritize process improvements.

Acceptance Criteria:

* Heatmaps can show completion rate or median duration by department and onboarding stage.
* Trend charts show relevant daily, weekly, or monthly metric changes.
* The selected metric and calculation period are labeled.

### US-404

As an HR Operations Analyst, I want to export validated analytical results, so that I can prepare further analysis and stakeholder reports without rebuilding calculations.

Acceptance Criteria:

* CSV exports preserve the active filters and visible metric definitions.
* Exported files use stable column names.
* Generated files contain no source credentials or restricted fields.

## Epic 5 — Machine Learning and Recommendations

### US-501

As an HR Manager, I want to see an onboarding risk score and key drivers for each at-risk employee, so that I can intervene appropriately.

Acceptance Criteria:

* High-risk employees display risk band, probability or score, and up to three interpretable contributing factors.
* Factors are derived from approved features such as overdue tasks, unresolved tickets, training status, and stage duration.
* The interface states that the prediction supports review and does not make automated employment decisions.

### US-502

As an HR Operations Analyst, I want the system to predict likely onboarding delays, so that I can assess which cohorts require proactive support.

Acceptance Criteria:

* The model produces predictions for eligible employees with sufficient input data.
* Performance metrics are available for the selected trained model.
* Missing features result in a clear unavailable or lower-confidence state rather than an unsupported prediction.

### US-503

As an HR Manager, I want to identify unusual onboarding patterns, so that I can investigate process failures that standard threshold rules may miss.

Acceptance Criteria:

* The anomaly view identifies the employee, cohort, or process area, anomaly date or period, and explanation fields.
* Examples include unusually long stage duration, abnormal ticket concentration, or low adoption relative to comparable role peers.
* Anomalies can be filtered and reviewed alongside underlying records.

### US-504

As a Department Manager, I want targeted recommendations for high-risk onboarding cases, so that I know the next best action rather than only seeing a score.

Acceptance Criteria:

* Recommendations are rule-based and linked to identified operational evidence.
* Each recommendation includes a suggested owner and rationale.
* Recommendations do not automatically modify HR or ticketing systems in the MVP.

## Epic 6 — Reporting

### US-601

As an Executive Leader, I want a downloadable monthly onboarding summary, so that I can use consistent information in an operating review.

Acceptance Criteria:

* The report includes company KPIs, departmental variance, major bottlenecks, risk summary, and recommended focus areas.
* The report is generated from the same processed data as the dashboard.
* The reporting period and data freshness timestamp are included.

### US-602

As an HR Manager, I want a department health report, so that I can review performance with department leaders.

Acceptance Criteria:

* The report includes completion, readiness, task, learning, and support indicators.
* It identifies the most material bottleneck and risk cohort.
* The report can be exported in CSV or Markdown/PDF-ready format.

### US-603

As an HR Operations Analyst, I want Power BI-compatible output tables, so that the organization can reuse the project data in existing reporting workflows.

Acceptance Criteria:

* Export tables have documented schemas and stable metric columns.
* The export includes refresh timestamp and source lineage fields.
* Sample instructions describe how to import the output into Power BI.

## Epic 7 — Data Pipeline and Quality

### US-701

As a Data Engineer, I want to run the end-to-end pipeline with one command, so that I can refresh all analytical outputs reliably.

Acceptance Criteria:

* A documented command executes ingestion, validation, cleaning, integration, KPI generation, and scoring in the correct dependency order.
* The run produces status logs and output locations.
* A failure prevents downstream publication and provides a descriptive error.

### US-702

As a Data Engineer, I want schema and quality validation before analytics runs, so that dashboard outputs are trustworthy.

Acceptance Criteria:

* Required-field, type, uniqueness, range, and referential-integrity checks execute for each source.
* Invalid records are quarantined with reason codes.
* A quality summary is saved for every run.

### US-703

As a Data Engineer, I want automated CI checks on each code change, so that regressions are detected before demonstration deployment.

Acceptance Criteria:

* GitHub Actions runs linting, unit tests, and validation checks on pushes and pull requests.
* A failed check is visible in the repository and blocks a protected merge workflow where configured.
* Dependencies are pinned or constrained for reproducibility.

# 11\. Dashboard Pages & User Experience

## 11.1 Entry Point and First-Time User Experience

The Streamlit application opens on a concise platform landing page. It explains the purpose of the platform, displays the last successful data-refresh time, and provides navigation to Executive, HR, Manager, and Analytics dashboards. A short onboarding panel defines the productivity-readiness score, risk bands, data limitations, and the fact that the data is anonymized or simulated for the MVP. The product should not require a user to understand the underlying pipeline before interpreting the dashboard.

Users select a reporting period and relevant organization filters in a persistent filter area. The interface must show which filters are active and provide a reset option. If data is unavailable, stale, or filtered to an empty cohort, the product displays a clear state with next-step guidance rather than blank charts.

## 11.2 Executive Dashboard

The Executive Dashboard is designed for a two-minute operational review. It presents a Company Overview with active new hires, onboarding completion rate, median completion time, productivity-readiness score, first-30-day completion, and count of high-risk employees. Each KPI includes comparison with the prior period where data is available.

Monthly Trends visualize completion rate, time-to-productivity proxy, risk count, and support-delay trends. A department comparison ranks or groups departments against the organizational benchmark. Risk Alerts summarize material exceptions, including persistent task bottlenecks, rising support resolution time, or a department cohort with elevated predicted delay risk. The dashboard includes a short insight panel that translates data into action-oriented language, such as: “New hires in Engineering show a higher-than-baseline setup-stage duration; unresolved access tickets are the leading associated factor.”

## 11.3 HR Dashboard

The HR Dashboard supports operational management. The Onboarding Funnel displays progression from preboarding through productive status, including count, conversion, and median duration at each stage. Department Comparison allows HR to identify uneven outcomes and investigate whether variation is driven by role mix, support delays, learning completion, or manager-owned tasks.

Task Completion shows completion rates by category and identifies pending, blocked, and overdue requirements. Pending Employees is a prioritized table with employee identifier, department, manager, stage, overdue task count, open-ticket count, readiness score, and risk band. Training Analytics includes course completion, overdue learning, assessment performance, and completion duration. Support analytics show ticket volume, category, priority, resolution time, and likely impact on onboarding delay.

## 11.4 Manager Dashboard

The Manager Dashboard focuses on a manager’s immediate responsibilities. Team Progress shows current new hires and their stage, completion percentage, readiness indicator, open blockers, and pending manager actions. Employee Performance is intentionally framed as onboarding readiness rather than performance evaluation; it provides transparent operational signals and does not make individual employment judgments.

Completion Status supports drill-down to tasks, learning assignments, and ticket metadata. Pending Actions places the most time-sensitive and impactful follow-ups first. The manager can review why a case is high risk, including specific overdue onboarding activities or unresolved access issues, then export the list for a weekly check-in. The interface must state when information is inferred from analytics rather than directly reported by a source system.

## 11.5 Analytics Dashboard

The Analytics Dashboard is intended for HR Operations and data-oriented stakeholders. Trend Analysis provides time-series views of completion, readiness, support resolution, and active-risk indicators. Correlation Charts allow analysts to compare aggregated support resolution time, task completion, learning outcomes, and tool adoption with onboarding outcomes. Heatmaps reveal stage duration or completion rate by department, role family, cohort, or location.

Department Comparison provides a structured table for benchmarking. Support Analytics links ticket categories and resolution-time bands to completion outcomes. The dashboard must make calculations and denominators clear, support download of visible data, and avoid causal claims from correlation alone.

## 11.6 Advanced Features and Edge Cases

* Employees with a joining date inside the selected range but insufficient elapsed time are identified as in-progress and excluded from final-completion denominators where appropriate.
* Employees whose role does not require GitHub or Jira are not penalized for low use of those tools; role-aware eligibility rules apply.
* A completed checklist with unresolved high-priority support tickets remains visible as a potential operational concern, not a contradiction.
* Missing source data produces a data-quality warning and suppresses unreliable derived scores where essential features are absent.
* Small cohort sizes are labeled to discourage overinterpretation of percentage changes.
* Model scoring is unavailable when minimum data completeness rules are not met.

## 11.7 UI/UX Highlights

* Use clear risk labels: Low, Medium, High; pair colors with icons and text.
* Use consistent date and percentage formats across all pages.
* Keep primary executive cards concise; place detail in drill-down tables and tooltips.
* Provide plain-language metric definitions adjacent to complex scores.
* Ensure keyboard-friendly navigation, readable contrast, responsive layout, and accessible chart alternatives.

# 12\. MVP Scope

The MVP validates the core proposition: reliable onboarding data can be consolidated to expose bottlenecks, identify at-risk new hires, and support more timely operational intervention. It prioritizes data quality, transparent KPIs, and useful dashboards over integrations and automation.

## Included in MVP

| Feature | Rationale |
| --- | --- |
| CSV ingestion for employee, onboarding, tool-usage, ticket, and learning datasets | Establishes the required analytical foundation without live-system dependencies. |
| Schema validation, rejected-record logs, and quality summaries | Ensures dashboard outputs are credible and auditable. |
| Cleaning, standardization, and unified analytical tables | Enables consistent cross-source analysis. |
| KPI engine for completion, stage duration, task, learning, support, and tool-adoption measures | Delivers the core decision-support value. |
| Executive, HR, Manager, and Analytics Streamlit dashboards | Provides persona-specific access to validated insights. |
| Baseline risk scoring and delay prediction | Demonstrates predictive analytics using explainable, feasible models. |
| Rule-based recommendations | Translates observed risk drivers into next-step guidance without unsupported automation. |
| CSV and Power BI-compatible exports | Allows evaluation and downstream reporting. |
| GitHub Actions CI, tests, and project documentation | Provides a professional, reproducible engineering baseline. |
| Synthetic or anonymized sample datasets | Enables safe, repeatable capstone demonstration. |

## Explicitly Excluded from MVP

| Feature | Reason for Deferral |
| --- | --- |
| Authentication and login | Not required for controlled capstone evaluation; production access controls require separate design and review. |
| Live HRIS, LMS, ticketing, or collaboration-tool APIs | Adds credential management, rate limits, privacy review, and integration complexity beyond MVP validation. |
| Transactional onboarding workflows | The product is an analytics platform, not a replacement for HR task-management tools. |
| Real-time streaming analytics | Daily refresh is sufficient for initial onboarding operational decisions. |
| Automated notifications by email or Slack | Requires external integration and escalation governance; suitable for Phase 2. |
| Production employee data | The capstone uses synthetic or approved anonymized datasets only. |
| Automated employment actions | Risk scores support human review and must not trigger personnel decisions. |
| Full Power BI live integration | Stable exports demonstrate interoperability without workspace configuration. |

# 13\. Future Scope

## Phase 2 — Intelligence and Operational Alerts

| Feature | Description |
| --- | --- |
| Real-Time Analytics | Add event- or API-based ingestion for more frequent refreshes of onboarding and support signals. |
| Email and Collaboration Alerts | Send governed alerts to HR or manager channels when high-risk thresholds, critical ticket aging, or stalled stages are detected. |
| Role-Based Authentication | Introduce secure role-aware access so managers see their teams, HR sees permitted organizational data, and executives see aggregate views. |
| Power BI Integration | Publish modeled tables or a managed semantic layer for Power BI reporting. |
| LLM-Generated HR Summaries | Generate reviewed, evidence-grounded monthly summaries from approved metrics and risk data. |
| Intervention Outcome Tracking | Capture whether recommended follow-up occurred and whether it improved the observed outcome. |

## Phase 3 — Platform Scale and Automation

| Feature | Description |
| --- | --- |
| Cloud Deployment | Containerize and deploy the platform to a managed cloud environment with monitoring and governed storage. |
| API Layer | Provide documented APIs for validated metrics, risk results, and dashboard integrations. |
| Advanced Forecasting | Evaluate gradient boosting and time-series methods for readiness and capacity forecasting when sufficient historical data exists. |
| Automated Workflow Recommendations | Integrate with approved workflow systems to draft or route recommended actions for human approval. |
| Chatbot Assistant | Provide a governed natural-language interface that retrieves approved onboarding metrics and report summaries. |
| Data Warehouse Integration | Replace CSV-only processing with managed warehouse tables and scheduled transformation jobs. |

# 14\. Risks and Assumptions

## 14.1 Risks

| \# | Risk | Probability | Impact | Mitigation |
| --- | --- | --- | --- | --- |
| R1 | Synthetic data may not reflect the complexity or missingness of real HR operational data. | Medium | High | Base schemas on realistic exports, create varied scenarios, and document simulation limitations. |
| R2 | Limited labeled historical outcomes may reduce model accuracy or make ML evaluation unstable. | High | Medium | Use simple baselines, cross-validation where appropriate, transparent metrics, and rule-based fallback recommendations. |
| R3 | Productivity proxies may be misunderstood as employee-performance measures. | Medium | High | Use careful terminology, document limitations, show operational drivers, and prohibit automated personnel decisions. |
| R4 | Employee identifiers and department labels may not match across sources. | High | High | Enforce mapping tables, referential-integrity checks, and visible data-quality reports. |
| R5 | Tool-usage data may introduce privacy concerns. | Medium | High | Use anonymized aggregate counts only; exclude content and document privacy principles. |
| R6 | Streamlit performance may decline with large detail tables. | Medium | Medium | Cache processed data, aggregate before rendering, and paginate or limit drill-down tables. |
| R7 | Scope creep may introduce live integrations, authentication, or transactional workflows before the core analytics value is validated. | High | High | Maintain strict MVP boundaries and record deferred work in the roadmap. |
| R8 | Correlation findings may be interpreted as causation. | Medium | Medium | Use explanatory language, show methodology, and frame insights as hypotheses for operational review. |
| R9 | Inconsistent model training data may create unfair risk signals across roles or departments. | Medium | High | Evaluate segmented performance, use approved operational features, and include human-review guidance. |
| R10 | CI or environment inconsistencies may delay demonstration readiness. | Low | Medium | Pin dependencies, use requirements.txt, test clean setup, and validate GitHub Actions early. |

## 14.2 Assumptions

| \# | Assumption |
| --- | --- |
| A1 | MVP source data is available as CSV files with the schema contracts defined in this document. |
| A2 | Datasets use anonymized or synthetic employee IDs and do not contain production credentials or sensitive free-form content. |
| A3 | Employee ID can be used as the primary integration key across the five required datasets. |
| A4 | The organization has defined mandatory onboarding tasks and target completion windows for the modeled scenario. |
| A5 | Role-aware eligibility rules can identify which tools and learning assignments are relevant to an employee. |
| A6 | A productivity-readiness proxy is acceptable for analytical demonstration when clearly documented and not used as a performance rating. |
| A7 | Python 3.10+ is available in the development and demonstration environment. |
| A8 | Streamlit is the primary MVP dashboard surface; Power BI is supported through stable export tables. |
| A9 | GitHub and GitHub Actions are available for version control and continuous integration. |
| A10 | The capstone team can generate or obtain enough sample history to demonstrate trends and baseline ML evaluation. |
| A11 | Stakeholders will review model recommendations as decision support rather than automated policy. |
| A12 | Daily refresh frequency is sufficient for MVP reporting and risk detection. |

# 15\. Acceptance Criteria

The following criteria define the minimum bar for the Employee Onboarding Analytics Platform MVP to be considered complete and ready for capstone evaluation.

## AC-1 — Data Pipeline

* All five datasets are ingested through a documented command.
* Each dataset passes required schema validation before records are admitted to the processed layer.
* Invalid records are isolated with source, row identifier, and reason code; the pipeline does not silently drop them.
* The pipeline produces employee, onboarding fact, and supporting analytical tables with documented output locations.
* The pipeline completes within five minutes for the defined one-year sample workload.

## AC-2 — Data Quality and Integration

* Processed employee IDs have no unintended duplicates.
* Referential-integrity failures are reported and excluded from dependent calculations according to documented rules.
* Department, role, category, status, and date fields are standardized consistently.
* A quality report includes source counts, accepted records, rejected records, duplicates removed, null rates, and execution timestamp.
* Dashboard metrics can be traced to documented processed tables and source fields.

## AC-3 — Analytics Engine

* Completion rate, completion time, task completion, overdue-task rate, learning completion, ticket metrics, and tool-adoption indicators match expected test calculations.
* Metrics can be segmented by at least department, cohort, manager, and date range where source data allows.
* Bottleneck analysis identifies stages, tasks, or support categories using transparent calculation rules.
* Productivity-readiness scoring is documented, reproducible, and clearly presented as a proxy.

## AC-4 — Machine Learning

* A baseline completion-risk or delay-prediction model trains and scores eligible records end-to-end without errors.
* The selected model achieves the documented target or reports its observed performance transparently on held-out/simulated evaluation data.
* Risk outputs include Low, Medium, and High bands plus interpretable drivers or explanation fields.
* Model metadata and artifacts are saved and reloadable without retraining.
* Recommendation outputs are evidence-based, rule-driven, and do not trigger automated employment decisions.

## AC-5 — Dashboard

* Executive, HR, Manager, and Analytics views render without unhandled errors.
* All required KPI cards, tables, and charts respond correctly to applicable filters.
* The HR Dashboard includes funnel, department comparison, task completion, pending employees, training analytics, and support insights.
* The Manager Dashboard includes team progress, employee readiness, completion status, and pending actions.
* The Analytics Dashboard includes trends, correlations or grouped comparisons, heatmaps, department comparison, and support analytics.
* The dashboard loads within three seconds for the standard sample dataset and displays data freshness.

## AC-6 — Reporting and Export

* Users can export visible summary and detail data as CSV.
* The system produces an executive summary and manager-action report containing the required period and data-refresh timestamp.
* Power BI-compatible exports use stable schema names and include data lineage fields.
* Exported data reflects active dashboard filters and contains no prohibited sensitive fields.

## AC-7 — Code Quality and DevOps

* Core Python files pass configured linting checks.
* Unit-test coverage is at least 80% for core modules.
* GitHub Actions runs linting, unit tests, and validation checks on relevant branch activity.
* README documentation enables a reviewer to install dependencies, run the pipeline, launch the dashboard, and locate outputs.

## AC-8 — Documentation

* This PRD is version-controlled in the repository.
* Data schemas, metric definitions, assumptions, and model limitations are documented.
* The architecture diagram or architecture explanation identifies raw, processing, analytics, ML, and dashboard layers.
* Source modules contain meaningful documentation and configuration instructions are complete.

# Appendices

## Appendix A — Glossary

| Term | Definition |
| --- | --- |
| Onboarding | The structured process that helps a new employee become administratively, culturally, and operationally ready to work. |
| Time-to-Productivity | The elapsed time from joining date until a defined productivity-readiness threshold is reached. |
| Productivity-Readiness Score | A documented composite proxy based on approved onboarding, learning, tool-adoption, and support signals; not an employee performance rating. |
| Onboarding Funnel | A staged view showing how employees progress through predefined onboarding phases. |
| Bottleneck | A task, stage, dependency, or issue category associated with disproportionate delay or drop-off. |
| Cohort | A group of employees analyzed together, usually by joining month, department, role, or location. |
| KPI | Key Performance Indicator used to measure progress toward an operational objective. |
| Data Freshness | How recently a dataset or dashboard was successfully refreshed. |
| Data Lineage | The traceable path from a metric or output back through transformations to source data. |
| Schema Contract | A documented agreement defining required fields, types, allowed values, and validation rules for a dataset. |
| Referential Integrity | The condition in which a foreign key, such as employee_id in a ticket record, maps to a valid parent record. |
| Risk Score | A model- or rule-derived estimate of the likelihood of an operational outcome such as delayed onboarding completion. |
| Anomaly Detection | Identification of patterns that are meaningfully different from expected values or comparable cohorts. |
| Classification Model | A machine learning model that assigns records to categories or estimates the likelihood of a categorical outcome. |
| Random Forest | An ensemble machine learning method using multiple decision trees for classification or regression. |
| Logistic Regression | An interpretable statistical classification model often used as a baseline for probability estimation. |
| XGBoost | A gradient-boosting method that may be evaluated in future scope for structured prediction tasks. |
| Isolation Forest | An anomaly-detection algorithm that identifies observations that are easier to isolate than normal patterns. |
| MAPE | Mean Absolute Percentage Error, a commonly used measure of forecasting accuracy. |
| CI | Continuous Integration: automated checks that run when code changes are submitted. |

## Appendix B — Data Schema Contracts

### B.1 Employee Dataset

```text
employee_id       : VARCHAR(50)   required, unique
Department        : VARCHAR(100)  required, controlled mapping
manager_id        : VARCHAR(50)   required where applicable
joining_date      : DATE          required, YYYY-MM-DD
role              : VARCHAR(100)  required
location          : VARCHAR(100)  required
employment_type   : VARCHAR(30)   required, full_time | part_time | contractor | intern
onboarding_cohort : VARCHAR(20)   derived, YYYY-MM

```

### B.2 Onboarding Progress Dataset

```text
onboarding_task_id     : VARCHAR(50)  required, unique
employee_id            : VARCHAR(50)  required, foreign key to employee
Task_name              : VARCHAR(150) required
task_category          : VARCHAR(80)  required
current_stage          : VARCHAR(50)  preboarding | setup | orientation | enablement | productive
task_status            : VARCHAR(30)  not_started | in_progress | complete | blocked | overdue
due_date               : DATE         required for mandatory tasks
completed_date         : DATE         nullable until complete
completion_percentage  : DECIMAL(5,2) range 0–100

```

### B.3 Internal Tool Usage Dataset

```text
usage_id                : VARCHAR(50) required, unique
employee_id             : VARCHAR(50) required, foreign key to employee
usage_date              : DATE        required
slack_activity_count    : INTEGER     non-negative
jira_usage_count        : INTEGER     non-negative
github_activity_count   : INTEGER     non-negative
teams_activity_count    : INTEGER     non-negative
workspace_activity_count: INTEGER     non-negative
daily_active_usage      : BOOLEAN     required

```

### B.4 Support Ticket Dataset

```text
ticket_id               : VARCHAR(50)  required, unique
employee_id             : VARCHAR(50)  required, foreign key to employee
created_date            : DATETIME     required
issue_category          : VARCHAR(80)  access | hardware | payroll | hr_policy | learning | other
priority                : VARCHAR(20)  low | medium | high | critical
resolution_time_hours   : DECIMAL(10,2) nullable until resolved, non-negative
assigned_team           : VARCHAR(100) required
status                  : VARCHAR(30)  open | in_progress | resolved | closed

```

### B.5 Learning Management Dataset

```text
learning_record_id      : VARCHAR(50)  required, unique
employee_id             : VARCHAR(50)  required, foreign key to employee
course_name             : VARCHAR(150) required
course_type             : VARCHAR(50)  compliance | orientation | role_specific | optional
assigned_date           : DATE         required
completed_date          : DATE         nullable until complete
assessment_score        : DECIMAL(5,2) nullable, range 0–100
completion_time_hours   : DECIMAL(10,2) nullable until complete, non-negative
course_status           : VARCHAR(30)  assigned | in_progress | completed | overdue

```

## Appendix C — Technology Stack

| Technology | Role in MVP |
| --- | --- |
| Python | Primary language for data processing, analytics, model training, and application orchestration. |
| Pandas | Data loading, cleaning, transformation, aggregation, and export. |
| NumPy | Numerical calculations and feature-engineering support. |
| SQL | Reproducible analytical queries and KPI calculations against processed data. |
| Scikit-learn | Baseline classification, clustering, anomaly detection, preprocessing, and evaluation. |
| Streamlit | Interactive dashboard and demonstration interface. |
| Power BI | Secondary reporting target through compatible exports and optional visualization review. |
| GitHub | Source control, collaboration, version history, and documentation hosting. |
| GitHub Actions | Automated linting, test execution, and validation checks. |

## Appendix D — Project Architecture

The architecture is intentionally layered so that ingestion and business logic can be maintained independently from presentation.

### D.1 Raw Data Layer

The raw layer contains immutable or source-faithful CSV inputs for employee, onboarding progress, internal tool usage, support tickets, and learning records. Source files are stored separately from processed outputs. The raw layer is treated as input evidence and is never overwritten by transformation logic.

### D.2 Processing Layer

The processing layer performs schema validation, duplicate handling, standardization, missing-value treatment, referential-integrity checks, and source mapping. It writes rejected records and data-quality reports alongside cleaned outputs. This layer creates trusted, normalized intermediate tables that preserve employee IDs and source lineage.

### D.3 Analytics Layer

The analytics layer creates employee-level onboarding snapshots and supporting detail tables. SQL and Pandas calculations generate KPIs for completion, stage duration, learning, support, tool adoption, cohorts, and bottlenecks. Metric definitions are centralized so the dashboard and exports use the same logic.

### D.4 Machine Learning Layer

The machine learning layer reads approved analytical features, prepares train/test datasets, trains baseline models such as Logistic Regression or Random Forest, and evaluates performance. Isolation Forest may be used for anomaly detection where appropriate. Serialized artifacts, model metadata, and evaluation outputs are saved in a dedicated model output location. All outputs remain advisory and interpretable.

### D.5 Dashboard Layer

The Streamlit dashboard reads processed analytical tables and model outputs rather than raw CSV files. It provides Executive, HR, Manager, and Analytics pages with global filters, accessible visualizations, exports, data freshness indicators, and explicit limitations. Power BI-compatible exports are generated from the validated analytics layer, preserving consistency across reporting surfaces.

### D.6 Delivery and Quality Layer

GitHub stores source code, schemas, documentation, sample data generators, and tests. GitHub Actions validates code quality and selected data contracts on change. A documented requirements file and configuration approach allow a reviewer to reproduce the pipeline and dashboard in a clean environment.

