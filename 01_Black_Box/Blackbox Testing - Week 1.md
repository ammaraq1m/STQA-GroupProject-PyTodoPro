# PyTodo Pro: Equivalence Partitioning Test Report

## Overview

| Item | Detail |
|---|---|
| Application under test | PyTodo Pro (`app.py`, `helpers.py`) |
| Technique | Equivalence partitioning with boundary value analysis |
| Test framework | pytest + Flask test client (temporary SQLite database) |
| Test files | `tests/test_helpers.py`, `tests/test_api.py` |
| Result | 42 test cases: **32 passed, 10 failed** |
| Defects found | 9 |

Expected results are taken from the specification in each function's docstring (and from the validation messages in `app.py`), not from the current behaviour of the code. A failing test therefore indicates a defect.

To run the tests:

```bash
pip install flask pytest
pytest tests -v
```

---

## 1. Equivalence Partitions

| Partition ID | Input | Type | Description | Representative value |
|---|---|---|---|---|
| UV1 | Username | Valid | 3-20 chars; letters, digits, underscore | `user_01` |
| UI1 | Username | Invalid | Fewer than 3 chars | `ab` |
| UI2 | Username | Invalid | More than 20 chars | 21 x `a` |
| UI3 | Username | Invalid | Contains illegal characters | `user name`, `user@name` |
| UI4 | Username | Invalid | Empty / whitespace only | `""`, `"   "` |
| UI5 | Username | Invalid | Not a string | `None` |
| PV1 | Password | Valid | 8 or more chars | `password123` |
| PI1 | Password | Invalid | 1-7 chars | `1234567` |
| PI2 | Password | Invalid | Empty | `""` |
| PI3 | Password | Invalid | Not a string | `None` |
| TV1 | Task title | Valid | Non-empty text | `Buy milk` |
| TI1 | Task title | Invalid | Empty string | `""` |
| TI2 | Task title | Invalid | Whitespace only | `"   "` |
| TI3 | Task title | Invalid | Field missing | `{}` |
| DV0 | Due date | Valid | No due date | `None` → "No due date" |
| DV1 | Due date | Valid | In the past | today − 1 → "Overdue" |
| DV2 | Due date | Valid | Today | today → "Due Today" |
| DV3 | Due date | Valid | 1-2 days away | today + 1, +2 → "Due Soon" |
| DV4 | Due date | Valid | 3+ days away | today + 3 → "Upcoming" |
| DI1 | Due date | Invalid | Wrong format | `28-10-2026` |
| CV1 | Completed at | Valid | Not completed | `None` → False |
| CV2 | Completed at | Valid | Within last 7 days (including now) | 1 hour ago → True |
| CV3 | Completed at | Valid | Exactly 7 days ago (inclusive) | 7 days ago → True |
| CI1 | Completed at | Invalid | Older than 7 days | 8 days ago → False |
| CI2 | Completed at | Invalid | In the future | tomorrow → False |
| SV1 | per_page | Valid | Positive integer | `2` |
| SI1 | per_page | Invalid | Negative | `-1` |
| SV2 | status | Valid | `done`, `open`, or empty | `done` |
| SI2 | status | Invalid | Any other value | `xyz` |

**Boundary values:**

- Username length: 2 / 3 / 20 / 21
- Password length: 7 / 8
- Due date offset: −1 / 0 / +1 / +2 / +3 days
- Completed at: exactly 7 days ago, and exactly `now`

---

## 2. Test Cases

| ID | Function / endpoint | Input | Partition | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC01 | `is_valid_username` | `abc` | UV1 (lower boundary) | True | True | Pass |
| TC02 | `is_valid_username` | 20 chars | UV1 (upper boundary) | True | True | Pass |
| TC03 | `is_valid_username` | `user_01` | UV1 | True | True | Pass |
| TC04 | `is_valid_username` | `ab` | UI1 | False | False | Pass |
| TC05 | `is_valid_username` | 21 chars | UI2 | False | False | Pass |
| TC06 | `is_valid_username` | `user name` / `user@name` / `user-name` | UI3 | False | False | Pass |
| TC07 | `is_valid_username` | `""` | UI4 | False | False | Pass |
| TC08 | `is_valid_username` | `None` | UI5 | False | False | Pass |
| TC09 | `is_valid_password` | `1234567` (7 chars) | PI1 (boundary) | False | False | Pass |
| TC10 | `is_valid_password` | `12345678` (8 chars) | PV1 (boundary) | True | **False** | **Fail** |
| TC11 | `is_valid_password` | `123456789` | PV1 | True | True | Pass |
| TC12 | `is_valid_password` | `""` | PI2 | False | False | Pass |
| TC13 | `is_valid_password` | `None` | PI3 | False | False | Pass |
| TC14 | `compute_urgency` | `None` / `""` | DV0 | "No due date" | "No due date" | Pass |
| TC15 | `compute_urgency` | today − 1 day | DV1 | "Overdue" | "Overdue" | Pass |
| TC16 | `compute_urgency` | today | DV2 | "Due Today" | **"Overdue"** | **Fail** |
| TC17 | `compute_urgency` | today + 1 day | DV3 | "Due Soon" | "Due Soon" | Pass |
| TC18 | `compute_urgency` | today + 2 days | DV3 (boundary) | "Due Soon" | "Due Soon" | Pass |
| TC19 | `compute_urgency` | today + 3 days | DV4 (boundary) | "Upcoming" | "Upcoming" | Pass |
| TC20 | `compute_urgency` | `28-10-2026` | DI1 | Error raised | `ValueError` | Pass |
| TC21 | `completed_in_last_n_days` | `None` | CV1 | False | False | Pass |
| TC22 | `completed_in_last_n_days` | 1 hour ago | CV2 | True | True | Pass |
| TC23 | `completed_in_last_n_days` | 6 days 23 h 59 m 59 s ago | CV2 (boundary) | True | True | Pass |
| TC24 | `completed_in_last_n_days` | exactly 7 days ago | CV3 | True | **False** | **Fail** |
| TC25 | `completed_in_last_n_days` | 8 days ago | CI1 | False | False | Pass |
| TC26 | `completed_in_last_n_days` | completed at exactly `now` | CV2 | True | **False** | **Fail** |
| TC27 | `completed_in_last_n_days` | tomorrow | CI2 | False | False | Pass |
| TC28 | `POST /api/register` | `validuser` / `12345678` | PV1 (boundary) | 201 | **400** | **Fail** |
| TC29 | `POST /api/register` | username 3 and 20 chars, valid password | UV1 | 201 | 201 | Pass |
| TC30 | `POST /api/register` | username `ab`, 21 chars, `user name!`, `"   "` | UI1-UI4 | 400 | 400 | Pass |
| TC31 | `POST /api/register` | password `1234567` and `""` | PI1, PI2 | 400 | 400 | Pass |
| TC32 | `POST /api/register` | same username registered twice | Duplicate | 400 or 409 | **201** | **Fail** |
| TC33 | `POST /api/tasks` | valid title, not logged in | Auth | 401 | 401 | Pass |
| TC34 | `POST /api/tasks` | title `Buy milk` | TV1 | 201, `done: false` | 201, `done: false` | Pass |
| TC35 | `POST /api/tasks` | title `""`, `"   "`, or missing | TI1-TI3 | 400 | 400 | Pass |
| TC36 | `GET /api/tasks` | `per_page=2&page=0`, 5 tasks | SV1 | 2 results | 2 results | Pass |
| TC37 | `GET /api/tasks` | `per_page=-1`, 15 tasks | SI1 | 400 or at most 10 results | **All 15 returned** | **Fail** |
| TC38 | `GET /api/tasks` | `status=done` / `status=open` | SV2 | Filtered correctly | Filtered correctly | Pass |
| TC39 | `GET /api/tasks` | `status=xyz` | SI2 | 200 or 400 | 200 | Pass |
| TC40 | `GET /api/tasks` | `q=zzz%' OR 1=1 --` | Security | 200, empty list | **500 `ProgrammingError`** | **Fail** |
| TC41 | `DELETE /api/tasks/<id>` | Bob deletes Alice's task | Security | Alice's task still exists | **Task deleted** | **Fail** |
| TC42 | `POST /api/tasks` | `due_date = "not-a-date"` | DI1 | 400 | **Saved, then `ValueError`** | **Fail** |

**Summary:** 42 test cases, 32 passed, 10 failed.

---

## 3. Defects Found

Severity ratings are suggestions; adjust them to your course's scale.

| Defect ID | Location | Description | Failed test | Expected (spec) | Actual | Severity |
|---|---|---|---|---|---|---|
| D01 | `helpers.is_valid_password` | Boundary error: uses `len > 8` instead of `>= 8` | TC10, TC28 | 8-char password accepted | 8-char password rejected | Medium |
| D02 | `helpers.compute_urgency` | `due <= today` treats today as overdue | TC16 | "Due Today" | "Overdue" | Medium |
| D03 | `helpers.completed_in_last_n_days` | `age.days < n` excludes exactly N days ago | TC24 | Counted (inclusive) | Not counted | Low |
| D04 | `helpers.completed_in_last_n_days` | `total_seconds() > 0` excludes a task completed at exactly `now` | TC26 | Counted | Not counted | Low |
| D05 | `app.py` `api_register` / `register_page` | No uniqueness check on username | TC32 | Duplicate rejected | Duplicate account created | Medium |
| D06 | `app.py` `api_list_tasks` | SQL injection: `q` is inserted into the SQL string | TC40 | Input treated as plain text | Query structure altered, server error | Critical |
| D07 | `app.py` `api_delete_task` | Delete isn't scoped to `session["user_id"]` | TC41 | Only the owner can delete | Any logged-in user can delete any task | High |
| D08 | `app.py` `api_list_tasks` | `per_page=-1` becomes `LIMIT -1` (no limit) | TC37 | Rejected or capped | All rows returned | Low |
| D09 | `app.py` `api_create_task` | `due_date` format isn't validated | TC42 | 400 error | Bad data stored; later reads crash with `ValueError` | Medium |

### Additional observations

- The web form at `/tasks/new` accepts an empty title, unlike the API (found by code review, no automated test written).
- TC20 passes because it documents current behaviour (an uncaught `ValueError` on a malformed date). It could be argued this should be handled more gracefully.
