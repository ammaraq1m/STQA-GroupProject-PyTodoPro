# PyTodo Pro · Week 4 UI and API comparison

The Playwright browser and API request client shared cookies within each case. Separate cases started with fresh contexts and disposable users. [Requests and responses](logs/web-results.json)

| ID | Procedure | Expected result | Actual observation | Status | Evidence | Defect |
| --- | --- | --- | --- | --- | --- | --- |
| I01 | Register and create a Work task through the API in the browser context. Open My Tasks. | API registration and task creation are visible in the browser session. `[201, 201, "qa_i01", ["API to UI"], "Work"]` | `[201, 201, "qa_i01", ["API to UI"], "Work"]` | Pass | [Screenshot](screenshots/comparison/I01.png) | — |
| I02 | Create and complete UI to API in the browser. Read API list/dashboard, reopen and rename via API, reload, then delete through the API. | Web create and complete appear in API list and dashboard. API update and deletion appear in the UI. `[200, "UI to API", true, 200, 1, 200, "API revision", "Upcoming", 200, []]` | `[200, "UI to API", true, 200, 1, 200, "API revision", "Upcoming", 200, []]` | Pass | [Screenshot](screenshots/comparison/I02.png) · [Checkpoint](screenshots/comparison/qa_i02-updated.png) | — |
| I03 | Enter three spaces in the web form, then send the same title in an API create request. Inspect the list and API error. | Web and API task creation both reject a whitespace-only title. `[400, "title is required", 0]` | `[400, "title is required", 1]` | Fail | [Screenshot](screenshots/comparison/I03.png) | [R02](DEFECT_REPORT.md#r02) |
| I04 | Register through the web, query API tasks, log out through the web and query the API again. | Web logout clears the API session in the same browser context. `[200, 401, "authentication required", "/login"]` | `[200, 401, "authentication required", "/login"]` | Pass | [Screenshot](screenshots/comparison/I04.png) | — |

| Behaviour | Web interface | REST API | Interpretation |
| --- | --- | --- | --- |
| Missing task title | Required attribute blocks normal submission. A direct form POST saved a blank title (W03, W08). | POST returned 400 with title is required and left the task table empty (A14). | Web server validation differs from API create. |
| Whitespace-only title | Browser accepts three spaces. Web server trims the title and saves a blank row (I03). | POST returns 400. PUT returns 200 and stores the supplied spaces (A15, A21). | Title validation also differs across API create and update. |
| Eight-character password | Registration stays on the form and displays the minimum length error (W07). | Registration returns 400 and creates no user (A07). | Shared server rule rejects the documented boundary. |
| Shared task state | Tasks and badges reflect API create, update and deletion after loading the page (I01, I02). | Web create and completion appear in list JSON and dashboard counters (I02). | Round trips reflect persisted state in both interfaces. |
| Shared session | API registration opens an authenticated browser session. Web logout ends that session (I01, I04). | The same API request returns 200 before web logout and 401 afterward (I04). | Session lifetime is shared across surfaces. |
