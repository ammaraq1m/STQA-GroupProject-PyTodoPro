# PyTodo Pro · Week 6 focused regression

The final run used original Week 4 and Week 5 assertions plus six new cases. Pytest times come from JUnit and cover setup, assertion and teardown. Browser case time covers scenario execution and screenshot capture, with browser setup measured in the runner wall time.

| Case | Expected result | Actual result | Prior evidence | Current status | Seconds | Defect | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A01 | 201 with id and username, session created, stored password hashed | 4 checks matched. registration response = `{"id":1,"username":"qa_owner"}`. session cookie issued = `true` | Pass | Pass | 0.318 | — | [Assertions](logs/api-responses.ndjson) |
| A07 | 201 and one user | HTTP status = `400`. users written = `0` | Fail | Fail | 0.007 | [R01](DEFECT_REPORT.md#r01) | [Assertions](logs/api-responses.ndjson) |
| A08 | Second request returns 400 or 409, one user remains | Both requests returned 201. SQLite has two users. | Fail | Fail | 0.299 | [R02](DEFECT_REPORT.md#r02) | [Assertions](logs/api-responses.ndjson) |
| A09 | 200 and shared session, 302 logout, then 401 and no cookie | 6 checks matched. login response = `[200,{"id":1,"username":"qa_owner"}]`. session authorized = `[200,[]]` | Pass | Pass | 0.349 | — | [Assertions](logs/api-responses.ndjson) |
| A10 | 401 invalid credentials, no session | 3 checks matched. HTTP status = `401`. JSON error = `"invalid credentials"` | Pass | Pass | 0.284 | — | [Assertions](logs/api-responses.ndjson) |
| A12 | All six return 401 authentication required, no task writes | 13 checks matched. HTTP status = `401`. JSON error = `"authentication required"` | Pass | Pass | 0.008 | — | [Assertions](logs/api-responses.ndjson) |
| A13 | 201 and 200 with matching fields; trimmed title and correct owner in SQLite | 3 checks matched. detail equals creation = `[200,{"category":"Work","category_id":1,"completed_at":null,"created_at":"2026-11-27T11:51:18.753455","description":"Fixture","done":false,"due_date":"2099-04-10","id":1,"title":"Alpha planning","urgency":"Upcoming"}]`. task fields = `["Alpha planning","Work","Fixture","2099-04-10",false,"Upcoming",null]` | Pass | Pass | 0.132 | — | [Assertions](logs/api-responses.ndjson) |
| A15 | 400 title is required, no write | 3 checks matched. HTTP status = `400`. JSON error = `"title is required"` | Pass | Pass | 0.130 | — | [Assertions](logs/api-responses.ndjson) |
| A16 | 400 with JSON error, no write | HTTP status = `500`. JSON error = `null` | Fail | Fail | 0.128 | [R03](DEFECT_REPORT.md#r03) | [Assertions](logs/api-responses.ndjson) |
| A18 | 400 with JSON error, no write | HTTP status = `500`. JSON error = `null`. SQLite task title and date rows = `[["Invalid date fixture","not-a-date"]]` | Fail | Fail | 0.149 | [R04](DEFECT_REPORT.md#r04) | [Assertions](logs/api-responses.ndjson) |
| A20 | 200 updates and delete, 404 on readback; completion fields and SQLite row consistent | 7 checks matched. completion response = `[200,"Revision","Keep me",true,true]`. SQLite completion = `[["Revision",1,"2026-11-27 11:51:19"]]` | Pass | Pass | 0.155 | — | [Assertions](logs/api-responses.ndjson) |
| A21 | 400 with JSON error, persisted title unchanged | HTTP status = `200`. JSON error = `null`. SQLite unchanged = `[["   ",0,null]]` | Fail | Fail | 0.135 | [R06](DEFECT_REPORT.md#r06) | [Assertions](logs/api-responses.ndjson) |
| A22 | 400 with JSON error, task remains open | HTTP status = `200`. JSON error = `null`. SQLite unchanged = `[["Alpha planning",1,"2026-11-27 11:51:19"]]` | Fail | Fail | 0.130 | [R07](DEFECT_REPORT.md#r07) | [Assertions](logs/api-responses.ndjson) |
| A23 | 400 with JSON error, SQLite unchanged | HTTP status = `200`. JSON error = `null` | Fail | Fail | 0.132 | [R08](DEFECT_REPORT.md#r08) | [Assertions](logs/api-responses.ndjson) |
| A26 | 200 with 10 newest, two nonoverlapping 2-item pages, then empty | 4 checks matched. page status and titles = `[200,["Sample 11","Sample 10","Sample 9","Sample 8","Sample 7","Sample 6","Sample 5","Sample 4","Sample 3","Sample 2"]]`. page status and titles = `[200,["Sample 11","Sample 10"]]` | Pass | Pass | 0.162 | — | [Assertions](logs/api-responses.ndjson) |
| A27 | 400 or capped at default 10 | HTTP 200 with 12 rows, above the default cap of 10. | Fail | Fail | 0.183 | [R09](DEFECT_REPORT.md#r09) | [Assertions](logs/api-responses.ndjson) |
| A28 | 200 with only matching rows, empty for no match | 4 checks matched. q=Alpha = `[200,["Alpha home","Alpha planning"]]`. category=Work&status=open = `[200,["Beta planning"]]` | Pass | Pass | 0.167 | — | [Assertions](logs/api-responses.ndjson) |
| A29 | 200 with total/open/overdue/due soon/completed of 3/2/1/1/1 | 1 checks matched. dashboard counters = `[200,{"completed_this_week":1,"due_soon":1,"open":2,"overdue":1,"total":3}]` | Pass | Pass | 0.143 | — | [Assertions](logs/api-responses.ndjson) |
| A30 | 201 with Due Today urgency | urgency label = `"Overdue"` | Fail | Fail | 0.136 | [R10](DEFECT_REPORT.md#r10) | [Assertions](logs/api-responses.ndjson) |
| A33 | Both return 404 not found. Owner retains access and SQLite row stays unchanged. | 6 checks matched. HTTP status = `404`. JSON error = `"not found"` | Pass | Pass | 0.251 | — | [Assertions](logs/api-responses.ndjson) |
| S04 | Distinct salted hashes verify the password. Plaintext absent. | 1 checks matched. two distinct salted hashes verify and differ from plaintext = `true` | Pass | Pass | 0.562 | — | [Assertions](logs/security-evidence.ndjson) |
| S05 | HttpOnly is present. | 1 checks matched. session cookie HttpOnly = `true` | Pass | Pass | 0.136 | — | [Assertions](logs/security-evidence.ndjson) |
| S06 | Secure and explicit Lax or Strict SameSite. | Secure and explicit SameSite absent. | Fail | Fail | 0.132 | [R11](DEFECT_REPORT.md#r11) | [Assertions](logs/security-evidence.ndjson) |
| S15 | User search data bound separately. | Search term is interpolated in query construction. | Fail | Fail | 0.012 | [R12](DEFECT_REPORT.md#r12) | [Assertions](logs/security-evidence.ndjson) |
| S16 | Delete requires both task ID and the authenticated owner. | Source check found no session-owner scope in the delete handler. | Fail | Fail | 0.012 | [R13](DEFECT_REPORT.md#r13) | [Assertions](logs/security-evidence.ndjson) |
| S17 | Key supplied through external configuration. | A literal session-signing key assignment was found. Value omitted. | Fail | Fail | 0.011 | [R14](DEFECT_REPORT.md#r14) | [Assertions](logs/security-evidence.ndjson) |
| S19 | Mutation forms have anti-CSRF controls and logout uses POST. | No token markup on the sampled task forms and logout is a GET link. | Fail | Fail | 0.007 | [R15](DEFECT_REPORT.md#r15) | [Assertions](logs/security-evidence.ndjson) |
| GAP01 | A task completed at the frozen reference instant counts in both dashboards. | API completed-this-week count = `[200,0]`. HTML dashboard status and all five counters = `[200,["1","0","0","0","0"]]` | Week 2 C03 Fail at helper layer | Fail | 0.143 | [R16](DEFECT_REPORT.md#r16) | [Assertions](logs/api-responses.ndjson) |
| GAP02 | A task completed exactly seven days before the frozen clock counts in both dashboards. | API completed-this-week count = `[200,0]`. HTML dashboard status and all five counters = `[200,["1","0","0","0","0"]]` | Week 2 C06 Fail at helper layer | Fail | 0.176 | [R17](DEFECT_REPORT.md#r17) | [Assertions](logs/api-responses.ndjson) |
| GAP03 | A task completed seven days and one second before the clock is excluded in both dashboards. | 3 checks matched. seeded age in seconds = `604801.0`. API completed-this-week count = `[200,0]` | Week 2 C07 Pass at helper layer | Pass | 0.151 | — | [Assertions](logs/api-responses.ndjson) |
| GAP04 | A task completed one second in the future is excluded in both dashboards. | 3 checks matched. seeded age in seconds = `-1.0`. API completed-this-week count = `[200,0]` | Week 2 C02 Pass at helper layer | Pass | 0.145 | — | [Assertions](logs/api-responses.ndjson) |
| GAP05 | Reject a malformed due-date update with JSON 400, leave the prior date in SQLite and keep detail readable. | PUT returned HTML 500 and stored the invalid date. Subsequent owner GET returned 500. | PUT path first run in Week 6 | Fail | 0.175 | [R04](DEFECT_REPORT.md#r04) | [Assertions](logs/api-responses.ndjson) |
| GAP06 | Peer GET and POST redirect from owner edit form. The owner retains form access and the row stays unchanged. | 6 checks matched. peer receives redirect to own list = `[302,"/"]`. owner title absent from denial response = `false` | Web route first run in Week 6 | Pass | 0.272 | — | [Assertions](logs/api-responses.ndjson) |
| W01 | Visitor redirects to login, valid registration signs in, valid login restores access after logout. | `["/login","My Tasks","/login","Dashboard"]` | Pass | Pass | 1.079 | — | [PNG](screenshots/web/W01.png) |
| W02 | Invalid username, short password and wrong login receive readable validation feedback. | `["Username must be 3-20 characters (letters, numbers, underscore).","Password must be at least 8 characters.","Invalid username or password."]` | Pass | Pass | 1.211 | — | [PNG](screenshots/web/W02.png) |
| W03 | Browser prevents required-field submission. | `[true,0,true,0]` | Pass | Pass | 0.975 | — | [PNG](screenshots/web/W03.png) |
| W04 | Create, edit, complete, reopen and delete a task. | `["Revised","Done","Upcoming","Delete this task?",1,0]` | Pass | Pass | 1.544 | — | [PNG](screenshots/web/W04.png) |
| W05 | Title search and combined category/status filters return only matching tasks. | `[["Alpha home","Alpha plan"],["Alpha plan"],["Alpha plan"]]` | Pass | Pass | 1.446 | — | [PNG](screenshots/web/W05.png) |
| W06 | Dashboard counts task states and dates accurately and links back to Tasks. | `[["3","2","1","1","1"],"My Tasks"]` | Pass | Pass | 1.415 | — | [PNG](screenshots/web/W06.png) · [Checkpoint](screenshots/web/qa_w06-dashboard.png) |
| W07 | Registration accepts passwords at the advertised eight-character minimum. | `["Create an account",["Password must be at least 8 characters."]]` | Fail | Fail | 0.326 | [R01](DEFECT_REPORT.md#r01) | [PNG](screenshots/web/W07.png) |
| W08 | The web server rejects a missing title even without the browser required check. | `[false,1]` | Fail | Fail | 0.541 | [R05](DEFECT_REPORT.md#r05) | [PNG](screenshots/web/W08.png) |
| I01 | API registration and task creation are visible in the browser session. | `[201,201,"qa_i01",["API to UI"],"Work"]` | Pass | Pass | 0.337 | — | [PNG](screenshots/comparison/I01.png) |
| I02 | Web create and complete appear in API list and dashboard. API update and deletion appear in the UI. | `[200,"UI to API",true,200,1,200,"API revision","Upcoming",200,[]]` | Pass | Pass | 0.979 | — | [PNG](screenshots/comparison/I02.png) · [Checkpoint](screenshots/comparison/qa_i02-updated.png) |
| I03 | Web and API task creation both reject a whitespace-only title. | `[400,"title is required",1]` | Fail | Fail | 0.685 | [R05](DEFECT_REPORT.md#r05) | [PNG](screenshots/comparison/I03.png) |
| I04 | Web logout clears the API session in the same browser context. | `[200,401,"authentication required","/login"]` | Pass | Pass | 0.507 | — | [PNG](screenshots/comparison/I04.png) |

## Deferred cases

| Original ID | Scenario | Status | Reason |
| --- | --- | --- | --- |
| C-M01 | Physical iPhone and Safari verification | Not Run | Physical iPhone and Safari unavailable in this run. |
| C-M02 | Physical Android and Chrome verification | Not Run | Physical Android and Chrome unavailable in this run. |
| C-M03 | Physical tablet verification | Not Run | Physical tablet unavailable in this run. |
| U-M01 | Uncoached first-use participant workflow | Not Run | Participant observation requires people and consent. |
| U-M02 | Participant error recovery and filter understanding | Not Run | Participant error recovery and comprehension require human evaluation. |
| A-M01 | Screen reader names, landmarks and announcements | Not Run | Assistive technology announcement verification requires the native tools and human observation. |
| A-M02 | Native text zoom and visual keyboard inspection | Not Run | Native text zoom and visual focus verification were outside the focused automation run. |
| A-M03 | Manual completion glyph and boundary contrast | Not Run | Manual glyph and boundary contrast review was deferred. |
| A31 | Adversarial search runtime regression (Week 5 N01) | Not Run | Reused defensive source review S15 and ordinary search A28. |
| A32 | Non-owner deletion runtime regression (Week 5 N02) | Not Run | Reused defensive source review S16 and ordinary ownership checks A33 and GAP06. |
| N03 | Executable browser-content regression (Week 5) | Not Run | Runtime executable-content testing is outside the defensive regression run. |
| N04 | Deployed HTTPS and transport behaviour (Week 5) | Not Run | Local Flask and Chromium have no production HTTPS endpoint. |

## Execution evidence

[Merged results](logs/regression-results.json) · [Runner summary](logs/regression.log) · [pytest log](logs/pytest.log) · [JUnit](logs/pytest-junit.xml) · [Browser log](logs/browser.log) · [Browser HTTP results](logs/web-results.json) · [Flask log](logs/web-flask.log)

The [initial attempt](logs/initial-attempt/regression-results.json) had four source-check infrastructure errors and twelve browser cases without results because the staging tree did not mirror the source path layout. The corrected run completed all 45 selected cases. Initial attempt counts are excluded from the final totals.
