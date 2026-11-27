# PyTodo Pro · Week 3 defect report

| Item | Detail |
| --- | --- |
| Execution baseline | Ubuntu 24.04.5 LTS x86_64, Playwright headless. Chromium desktop at 1440 × 900 unless a narrower configuration is specified. Browser versions appear in the [matrix](COMPATIBILITY_TESTING.md). |
| Severity | Major means a significant barrier to a core workflow or a substantial access barrier. Moderate means a material problem with a workaround. Minor means a limited clarity or feedback issue. |
| Status | Confirmed means observed in this run and open for remediation. Usability heuristic gaps are confirmed as UI behaviour, with user impact pending participant evaluation. |

| ID | Feature and title | Severity | Priority | Status | Cases |
| --- | --- | --- | --- | --- | --- |
| [D01](#d01) | Registration rejects the advertised minimum password length | Moderate | Medium | Confirmed | G14 |
| [D02](#d02) | Create and edit accept spaces-only task titles | Moderate | Medium | Confirmed | G16, G17 |
| [D03](#d03) | A task due today is marked Overdue | Moderate | Medium | Confirmed | G18 |
| [D04](#d04) | First-use task list displays a filter message | Minor | Low | Confirmed | U01 |
| [D05](#d05) | Creation lacks explicit success feedback | Minor | Low | Confirmed | U02 |
| [D06](#d06) | Navigation lacks a current-page indicator | Minor | Low | Confirmed | U03 |
| [D07](#d07) | Auth and task form controls lack programmatically associated names | Major | High | Confirmed | A-axe-login, register, new-task, edit-task |
| [D08](#d08) | Category and status filters lack accessible names | Moderate | Medium | Confirmed | A-axe-empty-tasks, populated-tasks |
| [D09](#d09) | Empty and completed task text has insufficient contrast | Moderate | Medium | Confirmed | A-axe-empty-tasks, populated-tasks |
| [D10](#d10) | Edit and Delete are small and closely spaced | Moderate | Medium | Confirmed | A-axe-populated-tasks |
| [D11](#d11) | Task content lacks a main landmark | Minor | Low | Confirmed | A10 |
| [D12](#d12) | Mobile layouts scale down or overflow and enlarged text pushes controls offscreen | Major | High | Confirmed | C01, C02, A11, A12 |
| [D13](#d13) | Completion control exposes a glyph as its name | Major | High | Confirmed | A13 |

## D01

| Field | Detail |
| --- | --- |
| Preconditions | Use a unique valid username on Register. |
| Reproduce | 1. Enter the username. 2. Enter `12345678`. 3. Click Register. |
| Expected | The account is created because the password meets the displayed minimum. |
| Actual | The form remains open with “Password must be at least 8 characters.” |
| Recommendation | Apply the stated inclusive lower bound and retain a GUI boundary test for passwords of length 7, 8 and 9. |
| Evidence | [Screenshot](screenshots/gui/chromium-desktop-G14.png) · [Week 2 case P03](../Week%202%20-%20White%20Box%20Testing/White-Box-Testing.md) |

## D02

| Field | Detail |
| --- | --- |
| Preconditions | Log in. To test editing, create any named task. |
| Reproduce | 1. Open New Task or Edit. 2. Enter three spaces as the title. 3. Click Create Task or Save Changes. |
| Expected | Form stays open, identifies the invalid title and preserves user input. |
| Actual | The app returns to My Tasks with a blank title row and no validation message. Editing also replaces a usable title with a blank one. |
| Recommendation | Validate the trimmed title before writing on both paths and show an error associated with Title. |
| Evidence | [New](screenshots/gui/chromium-desktop-G16.png) · [Edit](screenshots/gui/chromium-desktop-G17.png) |

## D03

| Field | Detail |
| --- | --- |
| Preconditions | Log in. On the execution date, both server and browser used UTC. |
| Reproduce | 1. Create a task with the current date as its due date. 2. Inspect the task's urgency badge. |
| Expected | Due Today. |
| Actual | Overdue. |
| Recommendation | Classify exact date equality as Due Today and past dates as Overdue. Verify dashboard counters with the same boundary data. |
| Evidence | [Screenshot](screenshots/gui/chromium-desktop-G18.png) · [Week 1 case TC16](../01_Black_Box/Blackbox%20Testing.md) · [Week 2 case U03](../Week%202%20-%20White%20Box%20Testing/White-Box-Testing.md) |

## D04

| Field | Detail |
| --- | --- |
| Preconditions | Fresh account, no tasks and no filters set. |
| Reproduce | 1. Register a new account. 2. Read the empty row on My Tasks. |
| Expected | A first-use message states that there are no tasks yet and the creation action is visible. |
| Actual | “No tasks match your filters.” appears and the + New Task link is visible. |
| Recommendation | Provide separate first-use and filtered-empty messages. |
| Evidence | [Screenshot](screenshots/usability/chromium-desktop-U01.png) |

## D05

| Field | Detail |
| --- | --- |
| Preconditions | Log in. |
| Reproduce | 1. Create Feedback sample. 2. Inspect the task list on return. |
| Expected | A newly created row and an explicit success message appear. |
| Actual | The row appears. There is no separate creation message. |
| Recommendation | Add a compact “Task created” confirmation where it can be perceived visually and by assistive technology. |
| Evidence | [Screenshot](screenshots/usability/chromium-desktop-U02.png) |

## D06

| Field | Detail |
| --- | --- |
| Preconditions | Log in. |
| Reproduce | 1. Navigate to Dashboard. 2. Compare Dashboard and Tasks in the navigation. 3. Inspect Dashboard's aria-current attribute. |
| Expected | The active navigation link is visually and programmatically identified. |
| Actual | Navigation links share the same observed styling and Dashboard has no aria-current. The heading identifies the page. |
| Recommendation | Add aria-current="page" and a visible active-state style. |
| Evidence | [Screenshot](screenshots/usability/chromium-desktop-U03.png) · [Run record](logs/results.json) |

## D07

| Field | Detail |
| --- | --- |
| Preconditions | Access Login and Register as a visitor. Log in and create a task for Edit. |
| Reproduce | 1. Visit Login, Register, New Task and Edit Task. 2. Run axe with the selected WCAG tags and inspect label and select-name results. |
| Expected | Each input, textarea and select exposes an accessible name associated with its visible label. |
| Actual | Both auth fields on each auth page fail label. On each task form, Title, Description and Due Date fail label, and Category fails select-name. |
| Recommendation | Match label for attributes to unique control IDs. Associate field hints and inline errors with the relevant controls. |
| Evidence | [Login axe](logs/axe-login.json) · [Register axe](logs/axe-register.json) · [New task axe](logs/axe-new-task.json) · [Edit task axe](logs/axe-edit-task.json) |

## D08

| Field | Detail |
| --- | --- |
| Preconditions | Log in. The issue occurs with or without tasks. |
| Reproduce | 1. Open My Tasks. 2. Run axe and inspect the two select-name violations. |
| Expected | Each select exposes a stable accessible name independent of the selected option. |
| Actual | Both category and status selects lack names. |
| Recommendation | Associate persistent Category and Status labels with the selects. Give title search a persistent visible label as well. |
| Evidence | [Empty Tasks axe](logs/axe-empty-tasks.json) · [Populated Tasks axe](logs/axe-populated-tasks.json) |

## D09

| Field | Detail |
| --- | --- |
| Preconditions | Log in with no tasks, then create and complete one task. |
| Reproduce | 1. Run axe on empty My Tasks. 2. Create and complete a task. 3. Run axe again. |
| Expected | Normal-sized text has at least 4.5:1 contrast. |
| Actual | The empty-state text and completed title each measure 2.84:1 with #999999 on white. |
| Recommendation | Darken the text to achieve at least 4.5:1. Retain the existing completion indicator and strike-through. |
| Evidence | [Empty Tasks axe](logs/axe-empty-tasks.json) · [Populated Tasks axe](logs/axe-populated-tasks.json) |

## D10

| Field | Detail |
| --- | --- |
| Preconditions | Log in with a visible task. |
| Reproduce | 1. Open My Tasks. 2. Run axe with the WCAG 2.2 AA tag. 3. Inspect target-size for Edit and Delete. |
| Expected | Controls meet the 24 × 24 CSS px size threshold or the applicable spacing allowance. |
| Actual | Edit is 23.4 × 15 px and Delete is 39.3 × 15 px. Axe measured 11.8 px of safe clickable space for each. |
| Recommendation | Increase the interactive boxes to at least 24 × 24 CSS px or provide sufficient spacing. |
| Evidence | [Axe results](logs/axe-populated-tasks.json) · [Task list](screenshots/accessibility/chromium-desktop-A-axe-populated-tasks.png) |

## D11

| Field | Detail |
| --- | --- |
| Preconditions | Log in. |
| Reproduce | 1. Open My Tasks. 2. Inspect the main content wrapper for a main element or role. |
| Expected | One main landmark identifies primary content. |
| Actual | The wrapper is a div with no main role. The page has a navigation landmark, title and H1. |
| Recommendation | Use a main landmark in the shared template and verify that keyboard users can bypass repeated navigation. |
| Evidence | [A10 run record](logs/results.json) |

## D12

| Field | Detail |
| --- | --- |
| Preconditions | Log in with a populated task list. Use the profiles and browsers from the matrix. |
| Reproduce | 1. Open Tasks and Dashboard with Chromium or WebKit mobile mode at 390 or 768 px and measure the layout viewport. 2. Repeat Tasks at 390 px in Firefox. 3. In a Chromium desktop context try a 320 px viewport, then try 768 px with root font size set to 200%. |
| Expected | Layout responds to the configured width. Navigation and controls stay usable at narrow widths and with larger text. |
| Actual | Chromium and WebKit mobile mode use a 980 px layout viewport. Firefox Tasks at 390 px expands to a 563 px document. At 320 px in Chromium, the navigation extends to 405 px. Under simulated enlargement at 768 px, Log out is offscreen on Tasks and New Task, and Delete is offscreen on Tasks. |
| Recommendation | Set the shared viewport metadata, let navigation wrap, provide a contained responsive task table or list, and verify native browser text zoom and device behaviour. |
| Evidence | [Mobile Chromium](screenshots/compatibility/chromium-mobile-C01.png) · [Mobile Firefox](screenshots/compatibility/firefox-mobile-C01.png) · [320 px](screenshots/accessibility/chromium-desktop-A11.png) · [Enlarged Tasks](screenshots/accessibility/chromium-desktop-A12.png) |

## D13

| Field | Detail |
| --- | --- |
| Preconditions | Log in with a completed task. |
| Reproduce | 1. Open My Tasks. 2. Inspect the completed task toggle in the accessibility tree. |
| Expected | The button name identifies its action and task, with completion state available programmatically. |
| Actual | The tree reports `button "✓"` without action, task context or a programmatic toggle state. |
| Recommendation | Give the button a task-specific accessible name and expose state with a consistent toggle pattern. |
| Evidence | [A13 run record](logs/results.json) · [Screenshot](screenshots/accessibility/chromium-desktop-A13.png) |

## Device emulation retest

| Defect | Profiles and scenarios | Observed | Status | Evidence |
| --- | --- | --- | --- | --- |
| [D12](#d12) | iPhone 15, Pixel 7, Galaxy S24 and iPad Pro 11 in portrait and landscape · C01–C02 | Tasks layout viewport widths observed across profiles were 980 px, 981 px, 1194 px. 14 of 16 executed layout checks failed the existing criteria. | Confirmed · remains open | [Device matrix](COMPATIBILITY_TESTING.md#playwright-device-emulation-extension) · [Measurements](logs/devices-results.json) |
