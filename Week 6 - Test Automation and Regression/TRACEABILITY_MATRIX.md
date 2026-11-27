# PyTodo Pro · Week 6 traceability matrix

Historical results are preserved. The archived manual GUI checklist contains procedures and expectations with Not run status. The executed Week 3 GUI evidence came from Playwright. No completed manual execution was evidenced for the selected workflows.

## Manual scenario to automated coverage

[Week 3 GUI checklist stored under Week 2](../Week%202%20-%20White%20Box%20Testing/Week%203%20GUI%2C%20Accesibility%2C%20Usability%20and%20Accesibility%20Testing/GUI_TESTING.md)

| Original manual ID | Workflow expectation | Source execution status | Automated equivalents selected in Week 6 |
| --- | --- | --- | --- |
| GUI-01 | Valid login | Not Run | W01, A09 |
| GUI-02 | Invalid login feedback | Not Run | W02, A10 |
| GUI-03 | Registration validation | Not Run | W02, W07, A07, A08 |
| GUI-04 | Task appears after creation | Not Run | W04, A13, I01 |
| GUI-05 | Missing title browser check | Not Run | W03, W08, A15 |
| GUI-06 | Edited title visible | Not Run | W04, A20, GAP06 |
| GUI-07 | Toggle completion and reopen | Not Run | W04, A20 |
| GUI-08 | Confirm or cancel delete | Not Run | W04, A20 |
| GUI-09 | Dashboard navigation | Not Run | W01, W06 |
| GUI-10 | Web logout | Not Run | W01, I04, A09 |
| GUI-11, GUI-12 | Visual labels and page consistency | Not Run | Deferred from focused run |

## Requirement to executable regression

| Case | Application requirement or test oracle | Origin | Executable selector | Source | Week 6 status |
| --- | --- | --- | --- | --- | --- |
| A01 | 201 with id and username, session created, stored password hashed | Week 4 A01 | test_api.py::test_A01_registration | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Pass |
| A07 | 201 and one user | Week 4 A07 | test_api.py::test_A07_password_boundary | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Fail |
| A08 | Second request returns 400 or 409, one user remains | Week 4 A08 | test_api.py::test_A08_duplicate | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Fail |
| A09 | 200 and shared session, 302 logout, then 401 and no cookie | Week 4 A09 | test_api.py::test_A09_session | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Pass |
| A10 | 401 invalid credentials, no session | Week 4 A10 | test_api.py::test_A10_invalid_login | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Pass |
| A12 | All six return 401 authentication required, no task writes | Week 4 A12 | test_api.py::test_A12_auth_matrix | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Pass |
| A13 | 201 and 200 with matching fields; trimmed title and correct owner in SQLite | Week 4 A13 | test_api.py::test_A13_create_get | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Pass |
| A15 | 400 title is required, no write | Week 4 A15 | test_api.py::test_create_validation[A15] | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Pass |
| A16 | 400 with JSON error, no write | Week 4 A16 | test_api.py::test_create_validation[A16] | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Fail |
| A18 | 400 with JSON error, no write | Week 4 A18 | test_api.py::test_create_validation[A18] | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Fail |
| A20 | 200 updates and delete, 404 on readback; completion fields and SQLite row consistent | Week 4 A20 | test_api.py::test_A20_update_reopen_delete | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Pass |
| A21 | 400 with JSON error, persisted title unchanged | Week 4 A21 | test_api.py::test_update_validation[A21] | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Fail |
| A22 | 400 with JSON error, task remains open | Week 4 A22 | test_api.py::test_update_validation[A22] | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Fail |
| A23 | 400 with JSON error, SQLite unchanged | Week 4 A23 | test_api.py::test_update_validation[A23] | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Fail |
| A26 | 200 with 10 newest, two nonoverlapping 2-item pages, then empty | Week 4 A26 | test_api.py::test_A26_pagination | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Pass |
| A27 | 400 or capped at default 10 | Week 4 A27 | test_api.py::test_A27_negative_page_size | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Fail |
| A28 | 200 with only matching rows, empty for no match | Week 4 A28 | test_api.py::test_A28_filter | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Pass |
| A29 | 200 with total/open/overdue/due soon/completed of 3/2/1/1/1 | Week 4 A29 | test_api.py::test_A29_dashboard | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Pass |
| A30 | 201 with Due Today urgency | Week 4 A30 | test_api.py::test_A30_due_today | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Fail |
| A33 | Both return 404 not found. Owner retains access and SQLite row stays unchanged. | Week 4 A33 | test_api.py::test_A33_peer_read_update_denied | [API script](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py) · [Report](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) | Pass |
| S04 | Distinct salted hashes verify the password. Plaintext absent. | Week 5 S04 | test_security.py::test_S04_password_hashes | [Security script](../Week%205%20-%20Security%20and%20Performance%20Testing/tests/test_security.py) · [Report](../Week%205%20-%20Security%20and%20Performance%20Testing/SECURITY_TESTING.md) | Pass |
| S05 | HttpOnly is present. | Week 5 S05 | test_security.py::test_S05_cookie_httponly | [Security script](../Week%205%20-%20Security%20and%20Performance%20Testing/tests/test_security.py) · [Report](../Week%205%20-%20Security%20and%20Performance%20Testing/SECURITY_TESTING.md) | Pass |
| S06 | Secure and explicit Lax or Strict SameSite. | Week 5 S06 | test_security.py::test_S06_cookie_deployment_flags | [Security script](../Week%205%20-%20Security%20and%20Performance%20Testing/tests/test_security.py) · [Report](../Week%205%20-%20Security%20and%20Performance%20Testing/SECURITY_TESTING.md) | Fail |
| S15 | User search data bound separately. | Week 5 S15 | test_security.py::test_S15_search_source_review | [Security script](../Week%205%20-%20Security%20and%20Performance%20Testing/tests/test_security.py) · [Report](../Week%205%20-%20Security%20and%20Performance%20Testing/SECURITY_TESTING.md) | Fail |
| S16 | Delete requires both task ID and the authenticated owner. | Week 5 S16 | test_security.py::test_S16_delete_source_review | [Security script](../Week%205%20-%20Security%20and%20Performance%20Testing/tests/test_security.py) · [Report](../Week%205%20-%20Security%20and%20Performance%20Testing/SECURITY_TESTING.md) | Fail |
| S17 | Key supplied through external configuration. | Week 5 S17 | test_security.py::test_S17_session_signing_configuration | [Security script](../Week%205%20-%20Security%20and%20Performance%20Testing/tests/test_security.py) · [Report](../Week%205%20-%20Security%20and%20Performance%20Testing/SECURITY_TESTING.md) | Fail |
| S19 | Mutation forms have anti-CSRF controls and logout uses POST. | Week 5 S19 | test_security.py::test_S19_web_mutation_form_source_review | [Security script](../Week%205%20-%20Security%20and%20Performance%20Testing/tests/test_security.py) · [Report](../Week%205%20-%20Security%20and%20Performance%20Testing/SECURITY_TESTING.md) | Fail |
| GAP01 | A task completed at the frozen reference instant counts in both dashboards. | Week 1 TC26 / Week 2 C03 | test_gaps.py::test_dashboard_completion_window[GAP01] | [Week 6 test gaps](tests/test_gaps.py) | Fail |
| GAP02 | A task completed exactly seven days before the frozen clock counts in both dashboards. | Week 1 TC24 / Week 2 C06 | test_gaps.py::test_dashboard_completion_window[GAP02] | [Week 6 test gaps](tests/test_gaps.py) | Fail |
| GAP03 | A task completed seven days and one second before the clock is excluded in both dashboards. | Week 2 C07 | test_gaps.py::test_dashboard_completion_window[GAP03] | [Week 6 test gaps](tests/test_gaps.py) | Pass |
| GAP04 | A task completed one second in the future is excluded in both dashboards. | Week 1 TC27 / Week 2 C02 | test_gaps.py::test_dashboard_completion_window[GAP04] | [Week 6 test gaps](tests/test_gaps.py) | Pass |
| GAP05 | Reject a malformed due-date update with JSON 400, leave the prior date in SQLite and keep detail readable. | Week 1 TC42 / Week 4 A18 (create precedent) | test_gaps.py::test_update_due_date_atomicity | [Week 6 test gaps](tests/test_gaps.py) | Fail |
| GAP06 | Peer GET and POST redirect from owner edit form. The owner retains form access and the row stays unchanged. | Week 4 A33 and Week 5 S08 (API ownership precedent) | test_gaps.py::test_web_peer_edit_denied | [Week 6 test gaps](tests/test_gaps.py) | Pass |
| W01 | Visitor redirects to login, valid registration signs in, valid login restores access after logout. | Week 3 G01, G03, G09, G11 | web.cjs::W01 | [Week 4 Playwright cases](../Week%204%20-%20Web%20and%20API%20Testing/tests/web.cjs) | Pass |
| W02 | Invalid username, short password and wrong login receive readable validation feedback. | Week 3 G02, G13 | web.cjs::W02 | [Week 4 Playwright cases](../Week%204%20-%20Web%20and%20API%20Testing/tests/web.cjs) | Pass |
| W03 | Browser prevents required-field submission. | Week 3 G12, G15 | web.cjs::W03 | [Week 4 Playwright cases](../Week%204%20-%20Web%20and%20API%20Testing/tests/web.cjs) | Pass |
| W04 | Create, edit, complete, reopen and delete a task. | Week 3 G04–G06, G10 | web.cjs::W04 | [Week 4 Playwright cases](../Week%204%20-%20Web%20and%20API%20Testing/tests/web.cjs) | Pass |
| W05 | Title search and combined category/status filters return only matching tasks. | Week 3 G07–G08 | web.cjs::W05 | [Week 4 Playwright cases](../Week%204%20-%20Web%20and%20API%20Testing/tests/web.cjs) | Pass |
| W06 | Dashboard counts task states and dates accurately and links back to Tasks. | Week 3 G09 | web.cjs::W06 | [Week 4 Playwright cases](../Week%204%20-%20Web%20and%20API%20Testing/tests/web.cjs) | Pass |
| W07 | Registration accepts passwords at the advertised eight-character minimum. | Week 2 P03 / Week 3 G14 | web.cjs::W07 | [Week 4 Playwright cases](../Week%204%20-%20Web%20and%20API%20Testing/tests/web.cjs) | Fail |
| W08 | The web server rejects a missing title even without the browser required check. | Week 1 web source observation / Week 3 D02 | web.cjs::W08 | [Week 4 Playwright cases](../Week%204%20-%20Web%20and%20API%20Testing/tests/web.cjs) | Fail |
| I01 | API registration and task creation are visible in the browser session. | Week 4 I01 | web.cjs::I01 | [Week 4 Playwright cases](../Week%204%20-%20Web%20and%20API%20Testing/tests/web.cjs) | Pass |
| I02 | Web create and complete appear in API list and dashboard. API update and deletion appear in the UI. | Week 4 I02 | web.cjs::I02 | [Week 4 Playwright cases](../Week%204%20-%20Web%20and%20API%20Testing/tests/web.cjs) | Pass |
| I03 | Web and API task creation both reject a whitespace-only title. | Week 3 G16 and Week 4 I03 | web.cjs::I03 | [Week 4 Playwright cases](../Week%204%20-%20Web%20and%20API%20Testing/tests/web.cjs) | Fail |
| I04 | Web logout clears the API session in the same browser context. | Week 4 I04 / A09 | web.cjs::I04 | [Week 4 Playwright cases](../Week%204%20-%20Web%20and%20API%20Testing/tests/web.cjs) | Pass |

Week 3 manual records C-M01–C-M03, U-M01–U-M02 and A-M01–A-M03 remain Not Run. Week 4 A31/A32 and their Week 5 equivalents N01/N02 remain deferred, counted once per scenario. Week 5 N03 and N04 also remain deferred. [Deferred cases](REGRESSION_TESTING.md#deferred-cases)
