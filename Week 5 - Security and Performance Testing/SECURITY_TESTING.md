# PyTodo Pro · Week 5 security testing

Pytest used Flask 3.0.3 and Werkzeug 3.1.9 with the application in test mode and an initialized SQLite file per case. Flask exception propagation was disabled to inspect ordinary HTTP error responses. Passwords were generated at runtime. Evidence contains response facts and assertions, with passwords, hash values, cookie contents and signing keys excluded.

| ID | Threat | Method / procedure | Expected | Actual | Status |
| --- | --- | --- | --- | --- | --- |
| S01 | T01 | Submit one invalid login for an existing account and one for an unknown account. | Same generic 401, no session. | Both returned 401 invalid credentials and no session. Timing was outside this check. | Pass |
| S02 | T05, T07 | Request six protected API operations and the web Dashboard without a session. | JSON 401 for API, redirect for web. | All API calls returned 401 and Dashboard redirected to Log in. | Pass |
| S03 | T01 | Sign in with disposable credentials, log out, then request API tasks using the same client. | Session created and cleared. Protected lookup ends with 401. | Login 200 and cookie present, logout 302 and cookie absent, tasks 401. | Pass |
| S04 | T01 | Register two accounts with the same generated password and verify their stored digests in memory. | Distinct salted hashes verify the password. Plaintext absent. | Both verification checks succeeded and the stored digests differ. | Pass |
| S05 | T01 | Inspect cookie metadata after registration. | HttpOnly is present. | HttpOnly present. | Pass |
| S06 | T01 | Inspect default cookie metadata against HTTPS deployment hardening expectations. | Secure and explicit Lax or Strict SameSite. | Secure absent. No explicit SameSite attribute. [D01](DEFECT_REPORT.md#d01) | Fail |
| S07 | T05 | Create one task each in two separate sessions. Read both lists and dashboards. | Each lists its own task and reports one total. | Both lists and counters scoped correctly. | Pass |
| S08 | T05, T07 | Use the peer client to read and rename a disposable owner task. Check the database. | Both requests return 404 and row remains unchanged. | Both returned JSON 404. Original owner and title remained. | Pass |
| S09 | T07 | Delete a disposable task through its owner session. | HTTP 200 and task removed. | HTTP 200 with result ok; no remaining row. | Pass |
| S10 | T05 | Scan login and task detail bodies for the generated password, digest and hash field. | No credential material in sampled bodies. | None of the checked values or field name appeared. | Pass |
| S11 | T02 | Submit a task title of three spaces. | JSON 400 and no write. | 400 title is required; no task persisted. | Pass |
| S12 | T02, T06 | Submit a numeric task title. | JSON 400 with no write. | HTML 500; no task persisted. [R01](DEFECT_REPORT.md#r01) | Fail |
| S13 | T05 | Inspect the S12-style error body with debugger disabled. | Body does not contain secret, trace or debugger. | Sampled HTML 500 excluded each checked marker. | Pass |
| S14 | T02 | Search for a normal title substring with two tasks owned by the session. | Only the matching owner task returned. | HTTP 200 with Invoice planning only. | Pass |
| S15 | T02 | Parse the API list handler and review how the search term reaches the query. | User search data bound separately. | Source review found search input interpolated in query construction. [R02](DEFECT_REPORT.md#r02) | Fail |
| S16 | T07 | Inspect the authenticated API deletion handler for owner scoping. | Delete requires both task ID and the authenticated owner. | Source review found no owner check in the handler. [R03](DEFECT_REPORT.md#r03) | Fail |
| S17 | T01 | Inspect the session signing configuration without recording the value. | Key supplied through external configuration. | App assigns a literal signing key. [D02](DEFECT_REPORT.md#d02) | Fail |
| S18 | T04 | Delete an owned fixture and inspect application SQLite schema and handler. | Persistent audit record available for actor, target and result. | Delete succeeded. Schema and route review did not show persistent task mutation audit storage. [D03](DEFECT_REPORT.md#d03) | Fail |
| S19 | T03 | Inspect task-list mutation forms and logout markup. | Mutation forms have anti-CSRF controls and logout uses POST. | No token markup was found for the sampled forms. Logout is a GET link. [D04](DEFECT_REPORT.md#d04) | Fail |
| S20 | T06 | Request a negative page size against 12 fixture rows. | 400 or bounded response. | 200 returned all 12 rows with no data change. [R04](DEFECT_REPORT.md#r04) | Fail |

| ID | Unexecuted runtime case | Expected control | Status and justification |
| --- | --- | --- | --- |
| N01 | Adversarial search regression (Week 4 A31) | Input handled as data by the query builder. | Not Run. Defensive source review S15 and ordinary search S14 supplied current evidence. |
| N02 | Destructive non-owner delete regression (Week 4 A32) | Denial and owner data retained. | Not Run. Used source review S16, non-owner read/update S08 and owner-only deletion S09. |
| N03 | Browser execution of untrusted title content | Title rendered as literal text. | Not Run. Template source was inspected. Runtime executable-content testing was outside the defensive checks. |
| N04 | Deployed HTTPS and transport settings | TLS and production cookie configuration enforced. | Not Run. Test client and loopback run had no production TLS endpoint. |

| Outcome | Count |
| --- | ---: |
| Pass | 12 |
| Fail | 8 |
| Not Run | 4 |
| Total | 24 |

[Test fixture data](test-data/SECURITY_FIXTURES.md). Evidence includes [pytest execution](logs/security-execution.log), [JUnit results](logs/security-junit.xml) and [per-case requests and assertions](logs/security-evidence.ndjson). Static cases assert properties of this revision and should be reviewed if the app architecture changes.
