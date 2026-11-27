# PyTodo Pro · Final QA evaluation report

**Release recommendation: withhold approval for a multi-user deployment.** PyTodo Pro supported the sampled happy paths for registration, authentication, task management and dashboard access. The evidence also shows unresolved task isolation and data-integrity defects, accessibility barriers and incomplete deployment assurance. The final focused regression had 20 failures. Four of the five Week 7 exit gates are unmet and the fifth awaits formal review and sign-off. [Week 7 test plan](../Week%207/Software%20Test%20Plan.md) · [Final regression](../Week%206%20-%20Test%20Automation%20and%20Regression/REGRESSION_TESTING.md)

## Scope and evidence

This is the Week 8 quality evaluation for TEB3433 / TFB3433. It covers the supplied Flask application, SQLite persistence, HTML interface, JSON API, templates and styles. The [Week 7 baseline](../Week%207/README.md#evidence-baseline) consolidates Weeks 1–6 at repository revision `17f54e1`. Week 8 compared the source and user-facing expectations with the project brief, application README and original weekly records. Application source, templates, CSS and the application dependency file match the Week 7 baseline. Week 8 outcomes reflect evidence reconciliation and source review, with no new product test executions. [Project brief](../Group%20Project.pdf) · [Application README](../README.md)

| Verification layer | Reconciliation |
| --- | --- |
| Week 1 and 2 | Compared all 68 historical verdict IDs and statuses with the source report rows. Raw logs, test files and the raw structural report are absent from the checkout. |
| Week 3 | Matched all 245 case/configuration/status observations to the engine and device JSON. Reviewed eight deferred manual cases and 33 historical checklist designs against the documented records. The sandbox incident had no case-level results. |
| Weeks 4 and 5 | Matched case verdicts to API/security JUnit and web result JSON. Checked deferred records against source tables. Matched eight measurement observations to the original stage metadata and performance CSVs. |
| Week 6 | Matched initial and final regression records to merged JSON, pytest JUnit and browser JSON. Reconciled initial infrastructure failures and unlaunched browser checks with the runner's classification. |
| Week 7 integrity | Checked test, execution and defect IDs, reconciled RTM counts against 594 requirement-execution links, and verified 690 distinct evidence path/locator combinations and reconciled the six charts with their CSV data. |

## Metrics summary

| Measure | Result |
| --- | --- |
| Baseline and final verdict records | 480 planned, 421 executed, 325 passed, 96 failed, zero blocked and 59 Not Run |
| Execution, pass and failure rates | 87.71% execution (421/480), 77.20% pass (325/421), 22.80% fail (96/421) |
| Unique test designs | 225 including four measurement designs. 174 with a verdict, four measured and 47 unexecuted |
| Requirement coverage | 39/44 mapped (88.64%), 35/44 with a verdict or measurement (79.55%), including 23 with failures and nine with no execution evidence |
| Automation coverage | 106/225 repository assertion designs (47.11%), 110/225 with load (48.89%), 178/225 including historical report-only automation and load (79.11%) |
| Structural coverage | Reported helper statements 31/31 and branches 18/18. Four helper tests failed |
| Defects | 29 open. 1 Critical, 9 High, 14 Medium and 5 Low. 3 P1, 7 P2, 14 P3 and 5 P4 |
| Focused regression | 25 pass / 45 executed (55.56%), 20 fail, 12 Not Run, zero final infrastructure blocks. 39/39 reused verdicts stable, of which 17 still fail |
| Local performance | 0 failures / 2,460 timed requests per run. Pinned aggregate P95 120 ms at 25 paced users |

Browser configurations and reused regression cases contribute observations without creating new designs. The archived initial attempt accounts for 16 blocks, including four source-check infrastructure errors and 12 browser checks that could not start. Both workload runs count separately from verdicts. [Formulas, evidence and charts](SOFTWARE_QUALITY_METRICS.md)

## Integrated product assessment

| Quality attribute | Verified finding and impact | Confidence boundary |
| --- | --- | --- |
| Functionality | Valid login, CRUD, filtering, shared session/state and ordinary counters passed in Weeks 1, 3 and 4. Password and date boundaries fail, duplicate accounts can be created, and the HTML and API write paths apply inconsistent validation. Week 6 reproduced both completion counter errors across dashboards. | Core flows work for sampled inputs. Uniqueness policy, web path confirmation, category handling and other inferred rules need explicit acceptance. |
| Reliability | Week 4 create and Week 6 update can commit a malformed date before returning 500. The Week 6 owner detail read then returned 500. Wrong types and malformed JSON also cause inconsistent errors or apparent success. | Persistent bad data and incorrect state are observed. Restart, recovery, concurrent writes and duration-based reliability have limited or no evidence. |
| Usability | Visible task creation and delete confirmation help the sampled workflow. Week 3 found misleading first-use text, no distinct creation confirmation and no active navigation cue. | Observation comes from scripted heuristics. First-use success, comprehension and satisfaction remain to be assessed with participants. |
| Accessibility | Week 3 found unassociated labels, unnamed selects, weak contrast, small targets, a missing landmark, reflow defects and a glyph-only toggle name. The sampled login keyboard and focus checks passed. | Barriers are documented. Native assistive technology, native zoom and some contrast checks remain open. The evidence covers selected page states and criteria. |
| Compatibility | Core task workflows passed across sampled engine and emulated-device contexts. Layout failures were frequent on narrow or mobile profiles, including at least one control falling outside the view under larger text. | Native Safari/iOS, Android, tablets and broader OS configurations lack physical confirmation. |
| Security | Sampled credential storage, authentication and owner read/update controls passed. Historical peer deletion and later owner-scope source evidence establish a serious isolation problem. API search binding, a literal signing key, CSRF/logout, cookie options, rendering and audit gaps remain open. | Week 1 reported a search error. Disclosure, runtime rendering impact and the actual deployment security posture remain unverified. Source observations support remediation and limits on release readiness. |
| Performance | The Week 5 paced read workload completed at 1–25 users without timed request errors. P95 increased with the tested load. | A shared-host loopback experiment with synthetic data and short stages cannot establish production capacity, write contention or an SLA. No deployment acceptance target is approved. |

Detailed weekly evidence includes the difference between Week 1 black-box and Week 2 structural results, Week 3 GUI and manual gaps, Week 4 API integration, Week 5 security/load, Week 6 repeatability and Week 7 traceability. [Weekly findings and limitations](QUALITY_FINDINGS_AND_LIMITATIONS.md)

## Preventive software quality assurance

Testing detected product behaviours. Quality control uses those results to triage defects and evaluate the build at a release gate. Quality assurance improves the process that supplies requirements, code and evidence so the same classes of defects are less likely to recur.

| QA activity | Finding that motivates it | Preventive practice and evidence of adoption |
| --- | --- | --- |
| Requirements reviews | Advertised password and urgency bounds disagreed with behaviour. Weeks 2 and 6 show completion boundary errors. Many RTM expectations are inferred. | Approve boundary tables, role/method permissions and API validation/error contracts before implementation. Record stakeholder approval against requirement IDs and observable acceptance checks. |
| Code reviews | Search and delete handlers omit expected data binding and owner scoping. Due dates can be written before effective validation. | Require reviewer evidence for query binding, invariants, transaction boundaries, render escaping and consistency across web/API writes. Link approval to specific changes and tests. |
| Coding standards | Web and API title checks diverge, and API update coerces a string to a completed state. | Establish common typed validation, shared error contracts and explicit transaction rules. Review exceptions explicitly. |
| Static code analysis | Source review identified unsafe query construction, a literal signing key and disabled template escaping. | Scan for risky SQL construction, secrets and escaping overrides. Triage findings with targeted human review and tracked closures. |
| CI and automated regression | The initial Week 6 harness blocked 16 records. The recovered run reproduced 17 earlier failures. | Pin dependencies and verify fixture/port setup. Run helper/API checks and browser smoke tests on changes, publish evidence keyed to build, and report assertion failures, infrastructure blocks and deferrals distinctly. |
| Security reviews | STRIDE and source checks show isolation and session weaknesses, while deployed TLS remains unverified. | Review threats and controls for sessions, mutations, queries and rendering at change and deployment boundaries. Agree on configuration acceptance and require reviewer sign-off. |
| Accessibility reviews | Week 3 found missing labels, focus/navigation context gaps and mobile reflow failures. | Require semantic component review, keyboard walkthroughs and axe checks in review. Schedule native assistive technology, zoom and device checks before release. |
| Defect root cause analysis | DEF-009 affected create and update. DEF-003/004 affect both dashboards via a shared helper. | Confirm systemic causes such as validation order or shared boundary logic, record impacted paths, and require corrective evidence for every surface before closure. |
| Test planning and traceability | Nine requirements lack executed evidence and approvals/owners remain TBD. | Assign owners to requirements, tests, defects and release gates. Review traceability before execution, resolve or document exceptions and archive original evidence with build and environment. |

## Exit criteria and readiness

| Gate | Week 7 criterion | Week 8 decision |
| --- | --- | --- |
| E1 | Every mandatory high-risk requirement has executed relevant coverage or approved exceptions. | **Unmet.** Security, physical compatibility and accessibility gaps remain. No approved exceptions appear in the evidence. |
| E2 | No unresolved Critical/High or P1 defects. Other open defects have owners and dispositions. | **Unmet.** 1 Critical, 9 High and 3 P1 remain open, with overlap across severity and priority. Owners and dispositions are pending. |
| E3 | Agreed focused regression passes with zero infrastructure blocks. | **Unmet.** Zero final infrastructure blocks but 20 final failures. Twelve cases were deferred. |
| E4 | Agreed accessibility, compatibility and performance checks meet approved thresholds. | **Unmet.** Layout and accessibility failures remain, native/manual checks are pending and production performance targets lack approval. |
| E5 | RTM and logs reconcile, with a named reviewer approving evidence, risks and exceptions. | **Pending sign-off.** Counts and links reconcile. Named approval is unavailable. |

Verified behaviours support a controlled course demonstration of sampled workflows. The multi-user release recommendation rests on verified isolation, integrity and access barriers and on the unmet exit criteria. It assumes independently owned tasks and ordinary deployment confidentiality expectations. Risk scores, the primary-module breakdown and the release decision are QA judgments. No production incident rate or deployment footprint is inferred. [Risk register](RESIDUAL_RISK_ASSESSMENT.md) · [Corrective actions and future testing](RECOMMENDATIONS_AND_FUTURE_TESTING.md)

Finite tests exercise selected data, configurations, timing and paths. A passing assertion establishes the observed condition within that scope. Full measured helper coverage remains compatible with incorrect answers at tested boundaries, and it leaves routes, SQL, templates and deployment behaviour outside the structural result. The existing positive controls are a foundation for repair and verification. They provide insufficient assurance for release with the current open findings.

## Deliverables

- [Software quality metrics and charts](SOFTWARE_QUALITY_METRICS.md)
- [Residual risk assessment](RESIDUAL_RISK_ASSESSMENT.md)
- [Quality findings and limitations](QUALITY_FINDINGS_AND_LIMITATIONS.md)
- [Prioritised recommendations and future testing](RECOMMENDATIONS_AND_FUTURE_TESTING.md)
- [Documentation compliance review](DOCUMENTATION_COMPLIANCE.md)
- [Master test cases](MASTER_TEST_CASES.csv) · [Master defect register](MASTER_DEFECT_REGISTER.csv) · [RTM template view](RTM_TEMPLATE_VIEW.csv)
