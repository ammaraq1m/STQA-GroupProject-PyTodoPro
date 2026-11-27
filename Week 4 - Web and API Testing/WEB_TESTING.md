# PyTodo Pro · Week 4 web testing

Playwright 1.65.1 ran Chromium 159.0.8154.6 headless at 1440 × 900, en-US and UTC. Each case used a fresh browser context. Protected routes were exercised with disposable users in a dedicated Flask database. [Web execution log](logs/web-execution.log) · [HTTP evidence](logs/web-results.json)

| ID | Procedure | Expected result | Actual observation | Status | Evidence | Defect |
| --- | --- | --- | --- | --- | --- | --- |
| W01 | Request Dashboard anonymously. Register, log out, log in and open Dashboard. | Visitor redirects to login, valid registration signs in, valid login restores access after logout. `["/login", "My Tasks", "/login", "Dashboard"]` | `["/login", "My Tasks", "/login", "Dashboard"]` | Pass | [Screenshot](screenshots/web/W01.png) | — |
| W02 | Submit a two-character username, then a seven-character password, then sign in with an incorrect password. | Invalid username, short password and wrong login receive readable validation feedback. `["Username must be 3-20 characters (letters, numbers, underscore).", "Password must be at least 8 characters.", "Invalid username or password."]` | `["Username must be 3-20 characters (letters, numbers, underscore).", "Password must be at least 8 characters.", "Invalid username or password."]` | Pass | [Screenshot](screenshots/web/W02.png) | — |
| W03 | On Register leave Username blank. On New Task leave Title blank. Click the submit controls and inspect validity and POST traffic. | Browser prevents required-field submission. `[true, 0, true, 0]` | `[true, 0, true, 0]` | Pass | [Screenshot](screenshots/web/W03.png) | — |
| W04 | Create an open task, edit its title, complete and reopen it, cancel deletion, then confirm deletion. | Create, edit, complete, reopen and delete a task. `["Revised", "Done", "Upcoming", "Delete this task?", 1, 0]` | `["Revised", "Done", "Upcoming", "Delete this task?", 1, 0]` | Pass | [Screenshot](screenshots/web/W04.png) | — |
| W05 | Create Work/Alpha plan and Personal/Alpha home, complete Alpha plan, search Alpha, then apply Work and Done. | Title search and combined category/status filters return only matching tasks. `[["Alpha home", "Alpha plan"], ["Alpha plan"], ["Alpha plan"]]` | `[["Alpha home", "Alpha plan"], ["Alpha plan"], ["Alpha plan"]]` | Pass | [Screenshot](screenshots/web/W05.png) | — |
| W06 | Create an overdue task, a task due tomorrow and a completed task, then review counters. | Dashboard counts task states and dates accurately and links back to Tasks. `[["3", "2", "1", "1", "1"], "My Tasks"]` | `[["3", "2", "1", "1", "1"], "My Tasks"]` | Pass | [Screenshot](screenshots/web/W06.png) · [Checkpoint](screenshots/web/qa_w06-dashboard.png) | — |
| W07 | Submit a fresh username with an eight-character password. | Registration accepts passwords at the advertised eight-character minimum. `["My Tasks", []]` | `["Create an account", ["Password must be at least 8 characters."]]` | Fail | [Screenshot](screenshots/web/W07.png) | [R01](DEFECT_REPORT.md#r01) |
| W08 | Sign in and submit a form request omitting Title. Inspect the resulting task list. | The web server rejects a missing title even without the browser required check. `[true, 0]` | `[false, 1]` | Fail | [Screenshot](screenshots/web/W08.png) | [R02](DEFECT_REPORT.md#r02) |

| Validation layer | Case | Observation |
| --- | --- | --- |
| Browser required check | W03 | Blank Username and Title set valueMissing and trigger zero POST requests. |
| Server authentication validation | W02, W07 | Forms reach the server and return visible validation feedback. The eight-character boundary is rejected. |
| Direct form submission | W08 | A missing Title posted to the web endpoint returns a redirect to Tasks and persists a blank row. |
