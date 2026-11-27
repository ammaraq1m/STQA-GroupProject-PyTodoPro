# PyTodo Pro · Week 3 usability testing

These scripted observations use Chromium desktop and record observable behaviour against usability expectations. User comprehension, perceived ease and satisfaction require participant sessions.

| ID | Procedure and test data | Expected result | Actual result | Status | Evidence | Defect |
| --- | --- | --- | --- | --- | --- | --- |
| U01 | Register a fresh user and inspect the empty state. | An empty task list gives a first-use explanation and visible creation action. | `["No tasks match your filters.", true]` | Fail | [Screenshot](screenshots/usability/chromium-desktop-U01.png) · [Run record](logs/results.json) | [D04](DEFECT_REPORT.md#d04) |
| U02 | Create Feedback sample and inspect the task list for a success message. | Creating a task gives explicit confirmation plus a visible new row. | `[1, 0]` | Fail | [Screenshot](screenshots/usability/chromium-desktop-U02.png) · [Run record](logs/results.json) | [D05](DEFECT_REPORT.md#d05) |
| U03 | Click Dashboard and inspect the active nav link for aria-current or distinctive styling. | Navigation identifies the active location beyond the page heading. | `[["Tasks", null, "400", "none", "rgb(207, 226, 247)"], ["Dashboard", null, "400", "none", "rgb(207, 226, 247)"], ["Log out", null, "400", "none", "rgb(207, 226, 247)"]]` | Fail | [Screenshot](screenshots/usability/chromium-desktop-U03.png) · [Run record](logs/results.json) | [D06](DEFECT_REPORT.md#d06) |

| Heuristic | Automated observation | Recommendation | Evidence |
| --- | --- | --- | --- |
| Navigation | Tasks and Dashboard share consistent links, colours and heading size. The Dashboard link lacks an active indicator. | Use a visible current-page cue and aria-current. | [G19 and U03](logs/results.json) |
| Feedback | Invalid credentials display a direct explanation. A new task appears with no separate confirmation. | Add a concise creation message near the heading. | [Login evidence](screenshots/gui/chromium-desktop-G02.png) |
| Error prevention | Delete requires confirmation and cancellation keeps the row. A title of three spaces is accepted on create and edit. | Retain confirmation and validate the trimmed title before saving. | [GUI cases G10, G16, G17](GUI_TESTING.md) |
| Understandability | A fresh account shows a filter-related empty message before any filters are selected. The creation link is visible. | Use distinct first-use and filtered-empty messages. | [Empty state evidence](screenshots/usability/chromium-desktop-U01.png) |

## Participant evaluation

| ID | Human evaluation task | Expected observation | Actual result | Status |
| --- | --- | --- | --- | --- |
| U-M01 | Ask first-time users to create, find, complete and delete a sample task without prompting. | Users discover the actions and understand the completion symbol and delete confirmation. | No participant sessions. | Not Run |
| U-M02 | Ask users to recover from invalid registration and find a task via combined filters. | Users can explain the error and the active filters, then recover independently. | No participant sessions. | Not Run |
