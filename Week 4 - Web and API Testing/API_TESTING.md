# PyTodo Pro · Week 4 REST API testing

Pytest used Flask’s test client with a separate initialized SQLite file per case and disposable accounts. Flask returned actual HTTP error responses for handled and unhandled failures. Requests sent Accept: application/json and used Content-Type: application/json for JSON bodies. Authenticated requests used test-client cookies without recording their values. [Request fixtures](test-data/FIXTURES.md)

## Endpoint inventory

| Method | Endpoint | Access | Input | Expected interface | Cases |
| --- | --- | --- | --- | --- | --- |
| POST | /api/register | Public | JSON username, password | 201 with id and username; session starts | A01–A08 |
| POST | /api/login | Public | JSON username, password | 200 with id and username or 401 | A09, A10 |
| GET | /api/categories | Public | None | 200 array of category IDs and names | A11 |
| GET | /api/tasks | Session | Query page, per_page, category, status, q | 200 task array, newest first, default page 0 and size 10 | A09, A12, A24, A26–A28 |
| POST | /api/tasks | Session | JSON title, optionally description, category_id, due_date | 201 task JSON or validation error | A12–A19, A30 |
| GET | /api/tasks/{id} | Session | Integer ID | 200 task JSON or 404 | A12, A13, A20, A25, A33 |
| PUT | /api/tasks/{id} | Session | Integer ID; JSON partial updates including done | 200 updated task JSON or 404 | A12, A20–A23, A25, A33 |
| DELETE | /api/tasks/{id} | Session | Integer ID | 200 result ok for owner deletion | A12, A20 |
| GET | /api/dashboard | Session | None | 200 total, open, overdue, due_soon, completed_this_week | A12, A24, A29 |
| GET | /logout | Web route shared by API session | None | 302 to /login and clears session | A09, I04 |

## Execution results

| ID | Method and endpoint | Test data and scenario | Expected | Actual | Status | Defect |
| --- | --- | --- | --- | --- | --- | --- |
| A01 | POST /api/register | Valid unique account | 201 with id and username, session created, stored password hashed | 201, matching account and session, hash distinct from supplied password | Pass | — |
| A02 | POST /api/register | Username omitted | 400 invalid username, no user | 400 invalid username, no user | Pass | — |
| A03 | POST /api/register | Username length 2 | 400 invalid username, no user | 400 invalid username, no user | Pass | — |
| A04 | POST /api/register | Username length 21 | 400 invalid username, no user | 400 invalid username, no user | Pass | — |
| A05 | POST /api/register | Password length 7 | 400 invalid password, no user | 400 invalid password, no user | Pass | — |
| A06 | POST /api/register | Numeric username | 400 with JSON error, no user | 500 HTML, no user | Fail | [D01](DEFECT_REPORT.md#d01) |
| A07 | POST /api/register | Password length 8 | 201 and one user | 400 invalid password, zero users | Fail | [R01](DEFECT_REPORT.md#r01) |
| A08 | POST /api/register | Same username in two clients | Second request returns 400 or 409, one user remains | 201 twice, two users | Fail | [R03](DEFECT_REPORT.md#r03) |
| A09 | POST /api/login; GET /logout; GET /api/tasks | Valid login in a fresh client, query tasks, then logout | 200 and shared session, 302 logout, then 401 and no cookie | 200, 302 and 401 as expected, cookie removed | Pass | — |
| A10 | POST /api/login | Existing username with incorrect password | 401 invalid credentials, no session | 401 invalid credentials, no session | Pass | — |
| A11 | GET /api/categories | Anonymous client | 200 with categories matching SQLite | 200, Personal/Study/Urgent/Work with matching IDs | Pass | — |
| A12 | GET/POST /api/tasks; GET/PUT/DELETE /api/tasks/1; GET /api/dashboard | No authenticated cookie | All six return 401 authentication required, no task writes | All six returned 401, zero task writes | Pass | — |
| A13 | POST /api/tasks; GET /api/tasks/{id} | Title with surrounding spaces, category, description and date | 201 and 200 with matching fields; trimmed title and correct owner in SQLite | 201 and 200, matching fields and owner row | Pass | — |
| A14 | POST /api/tasks | Empty JSON object | 400 title is required, no write | 400 title is required, no write | Pass | — |
| A15 | POST /api/tasks | Title of three spaces | 400 title is required, no write | 400 title is required, no write | Pass | — |
| A16 | POST /api/tasks | Numeric title | 400 with JSON error, no write | 500 HTML, no write | Fail | [D01](DEFECT_REPORT.md#d01) |
| A17 | POST /api/tasks | Truncated JSON object | 400 with JSON error, no write | 400 title is required, no write. The error names the field. | Pass | — |
| A18 | POST /api/tasks | Invalid due date string | 400 with JSON error, no write | 500 HTML. SQLite contains the task and invalid date. | Fail | [R05](DEFECT_REPORT.md#r05) |
| A19 | POST /api/tasks | JSON array instead of object | 400 with JSON error, no write | 500 HTML, no write | Fail | [D01](DEFECT_REPORT.md#d01) |
| A20 | PUT/DELETE/GET /api/tasks/{id} | Owner completes, reopens, deletes and fetches task | 200 updates and delete, 404 on readback; completion fields and SQLite row consistent | 200/200/200/404, expected completion state, zero rows after delete | Pass | — |
| A21 | PUT /api/tasks/{id} | Title of three spaces | 400 with JSON error, persisted title unchanged | 200, persisted title becomes three spaces | Fail | [D02](DEFECT_REPORT.md#d02) |
| A22 | PUT /api/tasks/{id} | String false supplied for done | 400 with JSON error, task remains open | 200, task completed and timestamp set | Fail | [D03](DEFECT_REPORT.md#d03) |
| A23 | PUT /api/tasks/{id} | Truncated JSON object | 400 with JSON error, SQLite unchanged | 200 with current task JSON, SQLite unchanged | Fail | [D04](DEFECT_REPORT.md#d04) |
| A24 | POST /api/register; GET /api/tasks; GET /api/dashboard | Two sessions, one task per account | 200 list/dashboard scoped to each session; distinct owner IDs | Both lists show only their own task, each dashboard totals one, owner IDs match | Pass | — |
| A25 | GET/PUT /api/tasks/999 | Nonexistent ID | 404 not found for both, no write | 404 both, zero rows | Pass | — |
| A26 | GET /api/tasks | 12 records; default, pages 0 and 1 of size 2, page beyond end | 200 with 10 newest, two nonoverlapping 2-item pages, then empty | 200 with expected ordering and counts 10, 2, 2 and 0 | Pass | — |
| A27 | GET /api/tasks | 12 records; per_page = −1 | 400 or capped at default 10 | 200 with all 12 items | Fail | [R06](DEFECT_REPORT.md#r06) |
| A28 | GET /api/tasks | Title substring, category and status alone or combined, no match | 200 with only matching rows, empty for no match | 200 with expected ordered titles and empty result | Pass | — |
| A29 | GET /api/dashboard | One overdue, one due soon and one completed | 200 with total/open/overdue/due soon/completed of 3/2/1/1/1 | 200 and counters 3/2/1/1/1 | Pass | — |
| A30 | POST /api/tasks | Due today | 201 with Due Today urgency | 201 with Overdue urgency | Fail | [R04](DEFECT_REPORT.md#r04) |
| A33 | GET/PUT /api/tasks/{id} | A second disposable session reads and attempts to rename an owner fixture | Both return 404 not found. Owner retains access and SQLite row stays unchanged. | Both returned 404. Owner read the original task and SQLite owner and title were unchanged. | Pass | — |

The [NDJSON evidence](logs/api-responses.ndjson) contains one line per case with full redacted requests, response statuses and JSON, and expected and actual assertions including selected SQLite facts. The [pytest log](logs/api-execution.log) and [JUnit XML](logs/api-junit.xml) contain case outcomes.

## Not Run

| ID | Case | Status | Basis |
| --- | --- | --- | --- |
| A31 | Known adversarial search input regression | Not Run | Prior Week 1 D06. Week 4 exercised ordinary search and combined filters. |
| A32 | Known non-owner deletion regression | Not Run | Prior Week 1 D07. Week 4 checked two disposable sessions for list and dashboard isolation, owner deletion and anonymous rejection. |
