# PyTodo Pro · Prioritised recommendations and future testing

## Immediate · Before release approval

| Order | Corrective action | Verification and evidence |
| --- | --- | --- |
| 1 | Resolve P1 DEF-006, DEF-007 and DEF-026. Bind API search input, enforce owner scope for deletion and move signing material to managed configuration with rotation. | Review query construction, method-by-method authorisation and configuration. Verify safe search acceptance, owner isolation and correct session behaviour in the corrected build. [Security results](../Week%205%20-%20Security%20and%20Performance%20Testing/SECURITY_TESTING.md) |
| 2 | Resolve High/P2 data integrity and API consistency defects DEF-009, DEF-021 and DEF-023. Validate before commit and remediate stored malformed data. | Verify create/update rejection, transactional state, subsequent reads and web/API compatibility against controlled fixtures. [Regression evidence](../Week%206%20-%20Test%20Automation%20and%20Regression/REGRESSION_TESTING.md) |
| 3 | Resolve High/P2 accessibility, layout and browser mutation findings DEF-014, DEF-019, DEF-020 and DEF-028. Address output escaping and cookie configuration in the same release review (DEF-029, DEF-025). | Recheck control labels, state, core task journeys, real devices, native assistive technology and deployed security policy. Require signed dispositions and explicit test ownership before reconsidering the gate. [Week 3 findings](QUALITY_FINDINGS_AND_LIMITATIONS.md) · [Risk register](RESIDUAL_RISK_ASSESSMENT.md) |

## Short term · Next remediation and verification cycle

- Align registration rules and enforce a database uniqueness policy once approved (DEF-001 and DEF-005). Exercise duplicate registration on both interfaces, including independent concurrent requests and case/normalisation rules.
- Centralise title, date, category and request-shape validation (DEF-010, DEF-022, DEF-024 and related High findings). Cover invalid optional fields, wrong body shape, unknown category IDs, bounded paging and atomic rejection. Resolve DEF-008 and verify safe page/index limits.
- Fix urgency and dashboard boundaries (DEF-002–004). Add decision tables and state-transition tests for due date, task state, user scope and clock boundaries with documented time-zone policy.
- Resolve DEF-015–018 and review remaining Week 3 usability issues DEF-011–013. Verify contrast, control spacing, semantics, keyboard and native zoom. Run the three physical-device and two participant protocols, the three native/manual accessibility protocols, and disposition historical checklist overlap explicitly.
- Add durable mutation auditing (DEF-027), restart persistence checks and dedicated peer web toggle/delete verification. Use approved deployment fixtures for TLS and cookie checks. [Open defect details](MASTER_DEFECT_REGISTER.csv) · [Coverage gaps](requirement_coverage.csv) · [Outstanding tests](outstanding_tests.csv)

## Long term · Sustain quality across releases

- Establish change-based CI with deterministic helpers and API tests on pull requests, Chromium smoke/integration jobs, and scheduled browser matrix and accessibility runs. Publish build, fixture versions, JUnit and screenshots. Keep harness errors and deferred work visible in the release review.
- Expand coverage measurement to Flask decisions, database failures and rendered journeys alongside helper coverage. Target risk and meaningful oracles such as failed-write atomicity and permissions per method.
- Approve representative performance objectives. Use separate load generation and longer mixed read/write workloads, increasing load and soak stages, and measure error rates, latency distribution, saturation and recovery against approved thresholds. Retain both local baseline runs for comparison under their documented conditions.
- Review new requirements, exceptions, unresolved defects and historical traceability at each release gate. Use escaped titles, labels, state exposure and responsive layout reviews as repeatable component acceptance criteria. [Week 7 gates](../Week%207/Software%20Test%20Plan.md#entry-exit-and-completion-criteria) · [Performance workload](../Week%205%20-%20Security%20and%20Performance%20Testing/PERFORMANCE_TESTING.md)
