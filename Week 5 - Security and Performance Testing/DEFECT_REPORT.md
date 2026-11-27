# PyTodo Pro · Week 5 defect report

| Classification | Count | Basis |
| --- | ---: | --- |
| Newly documented | 4 | Defensive runtime, source and schema checks in this run. |
| Previously recorded | 4 | Runtime reconfirmation of API type validation and page-size handling. Source reconfirmation of search construction and deletion scope. |

| ID | Finding | Severity | Evidence type | Status |
| --- | --- | --- | --- | --- |
| [D01](#d01) | Session cookie lacks Secure and explicit SameSite flags | Moderate | Runtime metadata against HTTPS deployment baseline | Confirmed |
| [D02](#d02) | Application assigns a literal session signing key | High | Source | Confirmed |
| [D03](#d03) | Task mutation lacks a persistent application audit trail | Moderate | Runtime fixture and source/schema review | Confirmed |
| [D04](#d04) | Web task mutation forms lack token markup and logout uses GET | High | Source | Confirmed |
| [R01](#r01) | Incorrect task title type returns HTML 500 | Major | Runtime | Reconfirmed |
| [R02](#r02) | Unsafe API search query construction | Critical | Source | Reconfirmed in source |
| [R03](#r03) | API deletion has no owner scope | High | Source | Reconfirmed in source |
| [R04](#r04) | Negative API page size is unbounded | Minor | Runtime | Reconfirmed |

### D01

| Item | Detail |
| --- | --- |
| How to verify | Register a disposable account with Flask's test client and inspect the resulting session cookie flags, with the value redacted. |
| Expected / actual | HTTPS deployment baseline requires Secure, HttpOnly and explicit SameSite. The app sets HttpOnly. Secure and explicit SameSite are absent in the tested configuration. |
| Recommendation | Set Secure in HTTPS deployment and declare a SameSite policy compatible with the app. Retain HttpOnly. |
| Evidence | S05–S06 in [security assertions](logs/security-evidence.ndjson). |

### D02

| Item | Detail |
| --- | --- |
| How to verify | Inspect the session configuration in app.py for the origin of the signing key. |
| Expected / actual | A deployment-specific secret comes from managed configuration. The application assigns a literal. The key value is omitted from evidence. |
| Recommendation | Generate a high-entropy deployment-specific key, supply it via a secrets provider, rotate the existing value and invalidate old sessions when migrating. |
| Evidence | S17 in [security assertions](logs/security-evidence.ndjson). |

### D03

| Item | Detail |
| --- | --- |
| How to verify | As the owner, delete one disposable task. Inspect the route and SQLite schema for a persistent event linking the actor, task, action and result. |
| Expected / actual | A durable audit event is available. Task deletion succeeded and no persistent audit event storage was present in the application schema and route reviewed. |
| Recommendation | Add append-only, access-controlled events for writes and sensitive authorization failures. Keep passwords and sessions out of the events. |
| Evidence | S18 in [security assertions](logs/security-evidence.ndjson). |

### D04

| Item | Detail |
| --- | --- |
| How to verify | Review task completion and deletion forms in the task-list template and the logout control in the shared navigation. Review the matching Flask routes. |
| Expected / actual | State changes use POST with CSRF protection. The sampled task forms contain no token markup or corresponding validation, and logout is a GET link. |
| Recommendation | Apply and validate CSRF tokens on state-changing web requests. Make logout use POST and retain appropriate cookie settings. |
| Evidence | S19 in [security assertions](logs/security-evidence.ndjson). Cross-site runtime verification was outside this check. |

### R01

| Item | Detail |
| --- | --- |
| Evidence | S12 sends a numeric task title and observes HTML 500 instead of a JSON validation error. SQLite stays unchanged. [Week 4 D01](../Week%204%20-%20Web%20and%20API%20Testing/DEFECT_REPORT.md#d01) |
| Recommendation | Validate JSON object and field types before field operations, using consistent JSON 400 errors. |

### R02

| Item | Detail |
| --- | --- |
| Evidence | S15 checks the query construction in source. Normal search passed S14. The prior adversarial runtime case remains Not Run. [Week 1 D06](../01_Black_Box/Blackbox%20Testing.md) · [Week 4 A31](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) |
| Recommendation | Use bound parameters for search input. |

### R03

| Item | Detail |
| --- | --- |
| Evidence | S16 checks the deletion route for session owner scoping. The prior non-owner deletion runtime case remains Not Run. [Week 1 D07](../01_Black_Box/Blackbox%20Testing.md) · [Week 4 A32](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) |
| Recommendation | Apply the authenticated owner constraint to delete and deny missing or inaccessible tasks. |

### R04

| Item | Detail |
| --- | --- |
| Evidence | S20 reproduces unbounded negative page size with 12 fixture rows. [Week 4 R06](../Week%204%20-%20Web%20and%20API%20Testing/DEFECT_REPORT.md#r06) |
| Recommendation | Enforce a positive page size and cap results at a documented maximum. |
