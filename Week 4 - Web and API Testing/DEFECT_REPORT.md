# PyTodo Pro · Week 4 defect report

| Classification | Meaning |
| --- | --- |
| New | Behaviour first recorded in the inspected deliverables during this Week 4 run. |
| Regression | A prior finding confirmed through the current API or web checks. New evidence stays linked to the original defect. |
| Severity | Major indicates failed requests or unintended persisted state with significant impact. Moderate indicates a material validation or workflow issue with a workaround. Minor indicates a limited issue in the exercised configuration. |
| Environment | Flask 3.0.3 with isolated SQLite, pytest 9.2.0 for the API and Chromium headless for web and integration. Use the fixtures and case references to reproduce. |

## New findings

### D01

| Field | Detail |
| --- | --- |
| Title | API accepts unexpected JSON types into string and object operations, returning HTTP 500 |
| Severity / status | Major / confirmed |
| Reproduction | 1. Send numeric username in a JSON registration object. 2. In a separate authenticated client, send a numeric title in a task creation object. 3. Send a nonempty JSON array as the create body. |
| Expected | Each request returns a 400 JSON validation error without writing an account or task. |
| Actual | All three return HTML 500 responses. SQLite row checks show no writes in these cases. |
| Recommendation | Require an object body and validate types before field operations. Use a consistent JSON error response. |
| Evidence | A06, A16 and A19. [Full request and SQLite evidence](logs/api-responses.ndjson) |

### D02

| Field | Detail |
| --- | --- |
| Title | API update persists whitespace-only titles |
| Severity / status | Moderate / confirmed |
| Reproduction | 1. Register a test account and create a named task. 2. Update its title to three spaces. 3. Inspect the response and stored title. |
| Expected | API returns 400 and retains the previous title, consistent with the create contract. |
| Actual | Update returns 200 and SQLite stores three spaces. API create rejects the same title with 400. |
| Recommendation | Reuse normalized, nonempty title validation in both API write paths. |
| Evidence | A15 and A21. Related web defect [Week 3 D02](../Week%203%20-%20GUI%20Compatibility%20Usability%20Accessibility%20Testing/DEFECT_REPORT.md#d02). [Full request evidence](logs/api-responses.ndjson) |

### D03

| Field | Detail |
| --- | --- |
| Title | String-valued completion input marks an open task completed |
| Severity / status | Major / confirmed |
| Reproduction | 1. Create an open task. 2. Send a partial update with the JSON string "false" as done. 3. Inspect the response and stored completion fields. |
| Expected | A non-boolean done value receives 400 and leaves the task open. |
| Actual | PUT returns 200 with done true, and SQLite receives done = 1 and a completion timestamp. |
| Recommendation | Require a JSON boolean for done and reject invalid values before calculating timestamps or writing state. |
| Evidence | A22. [Full request and SQLite evidence](logs/api-responses.ndjson) |

### D04

| Field | Detail |
| --- | --- |
| Title | API update reports success for malformed JSON |
| Severity / status | Moderate / confirmed |
| Reproduction | 1. Create a task. 2. Submit an update with Content-Type application/json and a truncated JSON object. 3. Inspect status, body and stored state. |
| Expected | 400 with a JSON error. Persisted fields remain unchanged. |
| Actual | 200 with the original task JSON. Checked SQLite fields are unchanged. |
| Recommendation | Distinguish parse failure from an intentional empty update and return a consistent JSON parse error. |
| Evidence | A23. [Full request evidence](logs/api-responses.ndjson) |

## Previously reported defects confirmed in Week 4

### R01

| Field | Detail |
| --- | --- |
| Severity | Moderate |
| Reproduction and observation | Register in the UI or API using a unique username and exactly eight password characters. The account should be created. The UI displays the minimum-length error and the API returns 400. |
| Recommendation | Apply an inclusive eight-character minimum consistently. |
| Evidence and history | W07, A07 · [Web screenshot](screenshots/web/W07.png) · [Week 3 D01](../Week%203%20-%20GUI%20Compatibility%20Usability%20Accessibility%20Testing/DEFECT_REPORT.md#d01) · [Week 2 P03](../Week%202%20-%20White%20Box%20Testing/White-Box-Testing.md) |

### R02

| Field | Detail |
| --- | --- |
| Severity | Moderate |
| Reproduction and observation | Submit the web create form with a missing title via a direct form request, or enter three spaces through the browser. Both should be rejected with feedback. Both save a blank row, while API POST rejects the missing or spaces-only title. |
| Recommendation | Validate the trimmed title at the web endpoint before writing, and associate the error with the title control. |
| Evidence and history | W08, I03, A14, A15 · [Missing title screenshot](screenshots/web/W08.png) · [Spaces screenshot](screenshots/comparison/I03.png) · [Week 3 D02](../Week%203%20-%20GUI%20Compatibility%20Usability%20Accessibility%20Testing/DEFECT_REPORT.md#d02) · [Week 1 web source observation](../01_Black_Box/Blackbox%20Testing.md) |

### R03

| Field | Detail |
| --- | --- |
| Severity | Moderate |
| Reproduction and observation | Submit API registration twice with the same username in separate clients. The second request should fail. Both return 201 and SQLite contains two users. |
| Recommendation | Enforce username uniqueness in storage and return a validated duplicate-account response. |
| Evidence and history | A08 · [Week 1 D05](../01_Black_Box/Blackbox%20Testing.md) |

### R04

| Field | Detail |
| --- | --- |
| Severity | Moderate |
| Reproduction and observation | Create a task via API with today's date. The response should show Due Today. It returns 201 with Overdue. |
| Recommendation | Handle due-date equality as Due Today before classifying dates in the past. |
| Evidence and history | A30 · [Week 3 D03](../Week%203%20-%20GUI%20Compatibility%20Usability%20Accessibility%20Testing/DEFECT_REPORT.md#d03) · [Week 2 U03](../Week%202%20-%20White%20Box%20Testing/White-Box-Testing.md) |

### R05

| Field | Detail |
| --- | --- |
| Severity | Major |
| Reproduction and observation | Submit a task create request with an invalid date string. The server should return 400 with no stored row. It returns HTML 500 after persisting the invalid date. |
| Recommendation | Validate and normalize date fields before any commit. |
| Evidence and history | A18 · [Week 1 D09](../01_Black_Box/Blackbox%20Testing.md) |

### R06

| Field | Detail |
| --- | --- |
| Severity | Minor |
| Reproduction and observation | With 12 fixture tasks request a negative page size. A validation error or capped result is expected. The response is 200 with all 12 tasks. |
| Recommendation | Validate page and page-size ranges and enforce an upper limit. |
| Evidence and history | A27 · [Week 1 D08](../01_Black_Box/Blackbox%20Testing.md) |

## Prior findings outside runtime retest

| Prior finding | Week 4 case | Status | Coverage in current run |
| --- | --- | --- | --- |
| Week 1 D06, unsafe API search query construction | A31 | Not Run | Ordinary search, category and status filtering executed in A28. |
| Week 1 D07, non-owner task deletion | A32 | Not Run | Owner deletion, anonymous rejection, account isolation, and non-owner read/update checks executed in A12, A20, A24 and A33. |

[Week 1 defect records](../01_Black_Box/Blackbox%20Testing.md)
