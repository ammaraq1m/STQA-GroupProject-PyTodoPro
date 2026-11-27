# PyTodo Pro Software Test Plan

| Field | Detail |
| --- | --- |
| Plan | Week 7, revision 1.0 |
| Review date | 27 November 2026 |
| Evidence baseline | Repository snapshot `17f54e1` and historical evidence for Weeks 1–6 |
| Course | TEB3433 / TFB3433 Software Testing and Quality Assurance, September 2026 |
| Plan status | Proposed exit gates. Approval, gate owners and acceptance authority TBD. |
| Current assessment | Exit criteria unmet. Open application findings and outstanding verification. |

## Introduction and objectives

PyTodo Pro is a Flask and SQLite task manager. Users register and sign in, create categorized tasks, assign due dates, complete or reopen work, filter their lists and inspect dashboard totals. The HTML UI and JSON API share task state and authentication. The project brief assigns the team an independent quality evaluation of the supplied application.

The assessment verifies documented behavior, measures selected quality attributes, reproduces discrepancies with evidence, and preserves traceability from requirements to designs, executions and defects. Priority goes to unauthorized access, data corruption, blocked core workflows and misleading task or dashboard state. A secondary objective is to measure whether the regression suite preserves passing controls and continues to detect known defects.

## Scope and requirements

| Area | Included | Basis |
| --- | --- | --- |
| Identity | Registration, username/password boundaries, login, logout, session and isolation | F01–F07, F21–F22, F26 |
| Task lifecycle | CRUD, categories, title and date validation, search/filter, paging, urgency, completion and dashboards | F08–F25 |
| Browser quality | Required controls, workflow feedback, responsive layout, browser/profile variation and accessibility | N01–N05, N16–N17 |
| Security and reliability | Credential storage, cookie policy, parameter binding, ownership, signing configuration, audit, CSRF, rendering, TLS and persistence | N06–N13, N18 and F21 |
| Performance | Local paced reads with measured latency, throughput, errors and resource observations | N14–N15 |

The [RTM](Requirements%20Traceability%20Matrix.csv) records source, explicit or inferred classification and gaps. README and helper specifications take precedence for advertised behavior. Source and earlier test expectations support inferred rules, which require stakeholder confirmation where policy or thresholds are missing. Application development and fixes, uncontrolled penetration testing, broad production capacity certification, formal accessibility conformance certification, and exhaustive platform or source-path coverage are outside this course test scope. Physical devices, assistive technology, participant observations and production-like transport remain conditional on access and approved scope.

## Method and execution environments

Use the [Test Strategy](Test%20Strategy.md) to select techniques. Sequence smoke checks before deep integration, prioritize identity, isolation and valid writes, then test negative and boundary cases and verify persisted state. Run targeted defect confirmation and the related regression suite after an approved change. Preserve original verdicts and record later attempts as new executions.

| Layer | Environment and tools |
| --- | --- |
| Week 1 | Historical pytest and Flask test client on temporary SQLite. Exact versions and script files TBD. |
| Week 2 | Linux, Python 3.13.5, pytest 9.0.2, Coverage.py 7.13.3. Helper tests with injected clocks and default-clock cases. |
| Weeks 3–6 | Documented Ubuntu 24.04.5 LTS x86_64 and Python 3.14.2. Pinned Flask 3.0.3 for formal results. Flask test client for API/security, loopback Flask for browser/load. |
| Browser | Node 24.22.2 and Playwright 1.65.1. Chromium 159.0.8154.6, Firefox 159.0 and WebKit 27.2 in Week 3. Chromium desktop in Weeks 4 and 6. axe-core 4.14.1 for Week 3 selected rules. |
| Load | Locust 2.47.0, SQLite 3.45.1, psutil and Matplotlib for monitoring/plots. Pinned run uses Flask 3.0.3. Preliminary run uses Flask 3.1.3. |
| Evidence | Git revisions, pytest/JUnit, JSON/NDJSON, screenshots, browser and Flask logs, SQLite assertions and CSV monitoring. Future platform and device access TBD. |

## Test data management

Initialize disposable SQLite files and seed the four categories. Use an isolated file per Flask case and a temporary database with distinct accounts/cookies and fresh browser contexts for browser suites. Use owner and peer accounts for isolation, generated credentials, synthetic tasks, known category IDs, fixed far-future dates and deliberate invalid inputs. Freeze the exact dashboard time window in Week 6 and record UI timezone or API host clock for date-sensitive runs. Seed the load fixture with 25 users and 1,500 tasks. Record versions, dates, configuration, expected results and fixture identity. Omit secrets from captured evidence. Archive results before rerunning tools that refresh their output files and dispose of temporary databases after collection.

## Roles and responsibilities

The brief proposes four student coordination roles and expects shared participation. Names, rotations, availability and approvals remain TBD.

| Role | Responsibility | Assigned person |
| --- | --- | --- |
| QA/Test Lead | Scope, schedule, gate review and integrated QA reporting | TBD |
| Test Design Coordinator | Requirements, RTM, manual procedures, oracles and coverage gaps | TBD |
| Automation/Tool Coordinator | Fixtures, harness, API/UI runs, code coverage and raw evidence | TBD |
| Defect & Metrics Coordinator | Triage, deduplication, metrics, risk updates and tracking retests | TBD |
| Remediation owner and acceptance authority | Prioritize remediation and disposition residual risks | TBD |

## Schedule and milestones

| Milestone | Output and dependency |
| --- | --- |
| Week 1 | Feature exploration, black-box partitions, boundaries and initial findings |
| Week 2 | Selected helper control-flow analysis and measured coverage |
| Week 3 | GUI, browser matrix, usability, axe and emulated-device extension |
| Week 4 | Web and REST API results with shared-session and integrity checks |
| Week 5 | STRIDE, defensive checks and controlled read-only load baseline |
| Week 6 | Focused regression, initial harness recovery and final rerun |
| Week 7 | Formal plan, test strategy, linked registers and exit assessment |
| Following integration | Apply Week 8 quality evaluation and prepare final presentation by course Week 12. Exact dates, remediation and retest schedule TBD. |

## Entry, exit and completion criteria

| Gate | Proposed criterion | Evidence position |
| --- | --- | --- |
| Entry | Identify the build, requirements baseline, priority risks, oracles and intended configurations. | Historical evidence supports the supplied baseline. Inferred policies and deployment targets need approval. |
| Entry | Provision isolated data and tools, check browser/server launch and verify smoke flows. | Achieved for final Weeks 3–6 local runs. Physical and deployed configurations pending. |
| Entry | Assign testers, gain access for manual/device checks and confirm deployment/performance targets. | TBD. |
| Exit E1 | Every mandatory high-risk requirement has executed relevant coverage or an approved, documented exception. | Unmet. Untested conditions and incomplete platform/transport verification. |
| Exit E2 | No unresolved Critical or High defects and no P1 defects. Other open defects have a named owner and disposition. | Unmet. 1 Critical, 9 High and 3 P1 remain open. Owners and dispositions TBD. |
| Exit E3 | All cases in the agreed focused regression pass with zero infrastructure blocks. | Unmet. Final run has 20 assertion failures and zero infrastructure blocks. |
| Exit E4 | Agreed accessibility, compatibility and performance acceptance checks complete and meet approved thresholds. | Unmet. Native checks outstanding, layout failures observed and deployment targets TBD. |
| Exit E5 | RTM and logs reconcile; named reviewer signs off evidence, risks and exceptions. | Evidence consolidated. Sign-off TBD. |

Week 7 documentation completion requires all six requested deliverables, valid cross-references and count reconciliation. Product test completion requires all exit gates or approved documented exceptions. A passing confirmation on the relevant build plus related regression is required before defect closure.

## Risks, mitigation and limitations

| Risk | Mitigation and required evidence |
| --- | --- |
| Confidentiality, integrity or account compromise | Prioritize P1 query binding, owner-scoped delete and signing secret configuration. Review corrective controls and confirm on the target build. |
| Malformed writes damage state | Pair response assertions with SQLite state and subsequent readback. Include create and update paths and test time boundaries deterministically. |
| Narrow layout or accessibility barriers | Retest affected configurations and verify native devices, zoom, keyboard focus and screen readers. |
| Historical evidence gaps | Retain Week 1–2 reports and flag absent scripts/raw outputs. Preserve manual templates as Not Run. |
| Test harness failures and environment drift | Pin dependencies, smoke-test staging, record configuration and archive initial attempts. Reconcile initial and final runs independently. |
| Misreading structural or load metrics | Report helper-only coverage; treat paced loopback results as measurements with no approved SLO. |
| Weak usability generalization | Arrange consented participant sessions and record completion, errors and recovery observations. |
| Ownership or acceptance decisions outstanding | Confirm assignees, platform matrix, SLOs and exception authority at review. |

Remaining limitations include test-client/development-server behavior, short read-only performance intervals, limited response and role matrices, synthetic data, restricted assistive technology and no deployment evidence. A source finding can confirm missing controls while runtime verification remains pending.

## Deliverables

The [Week 7 index](README.md) links the plan, strategy, RTM, master cases, defect register, execution history and summary. Retain Weeks 1–6 as the evidence of record. [Course brief](../Group%20Project.pdf) · [Application overview](../README.md)
