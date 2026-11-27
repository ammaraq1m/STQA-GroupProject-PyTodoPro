# Week 1 retrospective application analysis and test scope

This analysis was prepared during finalisation from the supplied PyTodo Pro application, the project brief, the historical Week 1 report and later traceability records. It sets out a retrospective initial scope and risk assessment. The original Week 1 test results remain in the historical report. [Project brief, p. 2](../Group%20Project.pdf) · [Historical Week 1 report](Blackbox%20Testing.md) · [Week 7 RTM](../Week%207/Requirements%20Traceability%20Matrix.csv)

## Overview and intended users

PyTodo Pro is a Flask and SQLite task manager with a browser interface and a JSON REST API. An account owner can organise tasks, record due dates, mark work complete, find tasks by filters and review totals on a dashboard. The web and API interfaces share application data and session state. The evaluation uses a local build, disposable accounts and an isolated data store. [Application README](../README.md) · [Application routes](../app.py) · [UI/API comparison](../Week%204%20-%20Web%20and%20API%20Testing/UI_API_COMPARISON.md)

| Intended user | Main objectives and access |
| --- | --- |
| Anonymous visitor | Create an account or sign in. Protected task and dashboard pages direct the visitor to sign in. The API category list is public. |
| Registered task owner | Create, edit, complete, reopen, find and delete personal tasks. Review personal dashboard totals and sign out. |
| API client acting for an account owner | Use registration or login to obtain a session, then access JSON task and dashboard operations under that account. |

Task ownership is the expected isolation boundary. Week 7 distinguishes explicit application requirements from inferred policies, including username uniqueness, unknown category handling and some API error contracts. The inventory retains that distinction. [Week 7 test plan](../Week%207/Software%20Test%20Plan.md#scope-and-requirements) · [Week 7 RTM](../Week%207/Requirements%20Traceability%20Matrix.csv)

## Feature inventory and test-scope matrix

| Feature and requirement IDs | Expected black-box behaviour | Historical or later evidence | Supplementary scope |
| --- | --- | --- | --- |
| Registration and validation, F01–F04 and F26 | Accept a username of 3–20 alphanumeric or underscore characters and a password of at least eight characters. Create a usable session after successful registration. Username uniqueness is an inferred policy and remains a separate concern. | Week 1 TC01–TC13 and TC28–TC32. Week 3 G01 and G12–G14. | Manual web partition, boundary and decision-table cases M01–M05. |
| Login, logout and protected access, F05–F07 | Valid credentials establish or restore a session. Invalid credentials are rejected. Logout clears the session. Protected web requests redirect anonymous users and protected API operations respond with HTTP 401. | Week 3 G02, G03 and G11. Week 4 A09, A10, A12 and W01. | Use controlled signed-in and anonymous preconditions. Later evidence covers the dedicated session checks. |
| Create, read and edit tasks, F08–F12, F23 and F25 | Store suitable task details, retain changes and return the intended task to its owner. Required-title behaviour, consistent API validation and rejecting invalid dates before persistence are documented or inferred oracles. | Week 1 TC33–TC35 and TC42. Week 3 G04/G05 and G15–G17. Week 4 A13–A19, A21–A25. | Create an owned task and check a stale Edit link in M07–M09. Retain earlier evidence for malformed requests and invalid dates. |
| Categories, search, status and pagination, F16–F18 | Return owner task matches using the intersection of active filters. Expose the seeded category set. API paging is expected to use a bounded positive size under the inferred paging contract. | Week 1 TC36–TC39. Week 3 G07/G08. Week 4 A11, A26–A28 and W05. | Manual combination of title and status with All categories in M06. API pagination and category discovery use existing evidence. |
| Urgency and dashboard totals, F13, F19 and F20 | Classify tasks by due date and completion state. Total, open, overdue, due-soon and recent-completion counters represent the owner's tasks. The exact seven-day completion boundary is inclusive. | Week 1 TC14–TC27. Week 3 G09/G18. Week 4 A29/A30. Week 6 GAP01–GAP04. | Check completion state in M07. Retain deterministic clock evidence for date and dashboard boundaries. |
| Complete, reopen and delete tasks, F14 and F15 | An open task can become Done and can be reopened. Cancel Delete preserves the row. Confirmation removes the owned task. | Week 3 G06/G10. Week 4 W04, A20 and I02. | Manual lifecycle and delete transitions M07–M09. |
| Ownership and shared state, F21, F22 and F24 | Only owners can use private task operations. The web and API represent consistent task and session state. The RTM records sampled controls and residual ownership gaps. | Week 4 A24, A33 and I01–I04. Week 5 S07/S08 and defensive source review. | Use only the tester's own disposable tasks. Retain existing isolation and interface evidence and record residual gaps. |

Weeks 3–6 hold the dedicated compatibility, accessibility, load and defensive security evidence. The supplementary Week 1 session uses a single browser and focuses on observable functional behaviour. [Week 3 report](../Week%203%20-%20GUI%20Compatibility%20Usability%20Accessibility%20Testing/WEEK_3_TEST_REPORT.md) · [Week 4 web and API report](../Week%204%20-%20Web%20and%20API%20Testing/WEEK_4_TEST_REPORT.md) · [Week 5 report](../Week%205%20-%20Security%20and%20Performance%20Testing/WEEK_5_TEST_REPORT.md) · [Week 6 regression report](../Week%206%20-%20Test%20Automation%20and%20Regression/WEEK_6_TEST_REPORT.md)

## Initial risk assessment and testing priorities

These retrospective planning scores assess plausible user impact and exposure. Impact and likelihood are each rated 1–3, with higher values indicating greater concern. The product determines priority. Scores 6–9 are High, 3–4 Medium and 1–2 Low. The scores are qualitative judgments for this course scope.

| Risk | Impact | Likelihood | Score and priority | Early checking priority |
| --- | ---: | ---: | --- | --- |
| Unauthorised access to a private task or an unintended destructive action | 3 | 3 | 9 High | Prioritise ownership and destructive-action evidence. Retain later defensive findings and verify cancellation and deletion of the tester's own data. |
| Invalid writes or unwanted state changes make task data incorrect or unreadable | 3 | 3 | 9 High | Compare observable state after valid writes and rejection. Prioritise task state transitions and retain API persistence evidence. |
| Registration, login or session failures block onboarding and access | 3 | 2 | 6 High | Cover valid controls, validation combinations and the advertised password boundary first. |
| Completion, date and dashboard boundaries give users a misleading status or count | 2 | 3 | 6 High | Cover task completion and reopening. Keep deterministic due-date and completion-window checks linked to the original cases. |
| Search, category, status or paging returns an incomplete or misleading list | 2 | 2 | 4 Medium | Use matching and nonmatching fixtures and combine active filters. Keep later API paging evidence linked. |

The practical order is registration, combined filtering, task lifecycle and deletion. This confirms a usable account before creating the fixtures for subsequent checks. [Manual execution suite](SUPPLEMENTARY_MANUAL_TESTING.md)

## Historical evidence and limitations

The historical report records 42 cases, with 32 Pass, 10 Fail and nine reported defects, using pytest and the Flask test client. The available Git history retains the report and its previous filename. The original Week 1 scripts and raw execution artifacts remain unavailable. The Week 2 supplementary helper script and the Week 4 API script are later suites with their own provenance. [Historical Week 1 report](Blackbox%20Testing.md) · [Week 2 supplementary verification](../Week%202%20-%20White%20Box%20Testing/RECOVERED_EVIDENCE.md) · [Week 4 API suite](../Week%204%20-%20Web%20and%20API%20Testing/tests/test_api.py)
