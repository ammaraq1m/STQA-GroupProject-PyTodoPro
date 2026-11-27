# PyTodo Pro · Week 3 GUI testing

Start each browser configuration with a fresh browser context and a unique QA account. G01–G11 run in order and share the tasks created in G04 and G07. G12–G19 use separate Chromium desktop test data. The expected outcomes come from the visible UI, the README, helper specifications and basic form behaviour.

## Chromium desktop checklist

| ID | Procedure and test data | Expected result | Actual result | Status | Evidence | Defect |
| --- | --- | --- | --- | --- | --- | --- |
| G01 | From Log in click Register, enter a unique username and valid password, then submit. | Registration opens My Tasks for the new user. | `["My Tasks", "qa_chromium_desktop"]` | Pass | [Run record](logs/results.json) | — |
| G02 | Log out, enter the registered username and a wrong password, then click Log in. | Incorrect credentials are rejected with a readable error. | Invalid username or password. | Pass | [Screenshot](screenshots/gui/chromium-desktop-G02.png) · [Run record](logs/results.json) | — |
| G03 | Enter the registered username and correct password and submit. | Valid credentials restore the session and open My Tasks. | My Tasks | Pass | [Run record](logs/results.json) | — |
| G04 | Click + New Task, fill title, description, Work and 2099-04-10, then click Create Task. | New task appears with its title, category and date. | `["○", "Alpha planning", "Work", "2099-04-10", "Upcoming", "Edit\nDelete"]` | Pass | [Screenshot](screenshots/gui/chromium-desktop-G04.png) · [Run record](logs/results.json) | — |
| G05 | Click Edit for Alpha planning, inspect prefill, replace all four fields and save, then reopen Edit. | Edit form is prefilled and saves the updated title, category, date and description. | `{"before": ["Alpha planning", "Week 3 fixture description", "1", "2099-04-10"], "displayed": ["○", "Alpha revised", "Study", "2099-04-12", "Upcoming", "Edit\nDelete"], "after": ["Alpha revised", "Updated description", "3", "2099-04-12"]}` | Pass | [Run record](logs/results.json) | — |
| G06 | Activate the Alpha revised completion button three times and check each badge. | Completion can be toggled on, off and on again. | `["Done", "Upcoming", "Done"]` | Pass | [Run record](logs/results.json) | — |
| G07 | Create Beta errands under Personal. Search for revised, then for missing-title. | Title search matches a substring and gives a useful empty result. | `[["Alpha revised"], ["No tasks match your filters."]]` | Pass | [Run record](logs/results.json) | — |
| G08 | Clear search, select Study then Open then Done. Reset category and select Open. | Category, open/done status and combined criteria select the expected tasks. | `[["Alpha revised"], [], ["Alpha revised"], ["Alpha revised"], ["Beta errands"]]` | Pass | [Run record](logs/results.json) | — |
| G09 | Click Dashboard, read all five counters, then use Tasks in the navigation. | Dashboard counters match 2 total, 1 open and 1 recently completed. Tasks returns to the list. | `[["2", "1", "0", "0", "1"], "My Tasks"]` | Pass | [Run record](logs/results.json) | — |
| G10 | Click Delete for Beta errands, dismiss its dialog, then click Delete again and accept. | Cancelling preserves the task and confirming removes it after reload. | `["Delete this task?", 1, 0, 1]` | Pass | [Run record](logs/results.json) | — |
| G11 | Click Log out, then request /dashboard in the same browser context. | Logout opens Log in and a fresh dashboard request redirects there. | `["/login", "/login"]` | Pass | [Run record](logs/results.json) | — |
| G12 | Open Register, fill only Password, submit. | A blank username is blocked by required-field validation. | `{"missing": true, "message": "Please fill out this field."}` | Pass | [Run record](logs/results.json) | — |
| G13 | Submit ab with a valid password, then use a valid username with 1234567. | Invalid username and seven-character password produce the relevant messages. | `["Username must be 3-20 characters (letters, numbers, underscore).", "Password must be at least 8 characters."]` | Pass | [Run record](logs/results.json) | — |
| G14 | Register a unique account using exactly 12345678. | An eight-character password meets the displayed minimum. | `["Create an account", ["Password must be at least 8 characters."]]` | Fail | [Screenshot](screenshots/gui/chromium-desktop-G14.png) · [Run record](logs/results.json) | [D01](DEFECT_REPORT.md#d01) |
| G15 | Open New Task, leave Title empty and click Create Task. | An empty title is blocked by required-field validation. | `{"missing": true, "message": "Please fill out this field."}` | Pass | [Run record](logs/results.json) | — |
| G16 | Enter three spaces into Title and click Create Task. | Spaces-only title is rejected with feedback. | `{"heading": "My Tasks", "errors": [], "blankRows": 1}` | Fail | [Screenshot](screenshots/gui/chromium-desktop-G16.png) · [Run record](logs/results.json) | [D02](DEFECT_REPORT.md#d02) |
| G17 | Enter three spaces into Title and click Save Changes. | Spaces-only title is rejected with feedback. | `{"heading": "My Tasks", "errors": [], "blankRows": 2}` | Fail | [Screenshot](screenshots/gui/chromium-desktop-G17.png) · [Run record](logs/results.json) | [D02](DEFECT_REPORT.md#d02) |
| G18 | Create a Work task with today’s UTC date and read its badge. | A task due today shows Due Today. | Overdue | Fail | [Screenshot](screenshots/gui/chromium-desktop-G18.png) · [Run record](logs/results.json) | [D03](DEFECT_REPORT.md#d03) |
| G19 | Compare nav link text and computed nav, background and heading styling on Tasks and Dashboard. | Tasks and Dashboard use consistent navigation and page headings. | `[{"nav": ["PyTodo Pro", "Tasks", "Dashboard", "Log out"], "navColor": "rgb(27, 58, 92)", "background": "rgb(245, 246, 248)", "headingSize": "32px"}, {"nav": ["PyTodo Pro", "Tasks", "Dashboard", "Log out"], "navColor": "rgb(27, 58, 92)", "background": "rgb(245, 246, 248)", "headingSize": "32px"}]` | Pass | [Screenshot](screenshots/gui/chromium-desktop-G19.png) · [Run record](logs/results.json) | — |

## Core workflow cross-check

Each column counts G01–G11 for that browser and viewport. Individual outcomes and the actual values for each browser are in the [execution log](logs/execution.log).

| Configuration | Pass | Fail | Not Run |
| --- | --- | --- | --- |
| chromium-desktop | 11 | 0 | 0 |
| chromium-tablet | 11 | 0 | 0 |
| chromium-mobile | 11 | 0 | 0 |
| firefox-desktop | 11 | 0 | 0 |
| firefox-tablet | 11 | 0 | 0 |
| firefox-mobile | 11 | 0 | 0 |
| webkit-desktop | 11 | 0 | 0 |
| webkit-tablet | 11 | 0 | 0 |
| webkit-mobile | 11 | 0 | 0 |

## Core workflows on emulated devices

G01–G11 were repeated in portrait and landscape using the Playwright profiles listed in the [compatibility matrix](COMPATIBILITY_TESTING.md#playwright-device-emulation-extension). The [device run log](logs/devices-execution.log) records expected-case execution and observed values by configuration.

| Emulated profile | Pass | Fail | Not Run | Invalid login evidence | Task creation evidence |
| --- | --- | --- | --- | --- | --- |
| Pixel 7 · Portrait | 11 | 0 | 0 | [PNG](screenshots/gui/devices/pixel-7-portrait-G02.png) | [PNG](screenshots/gui/devices/pixel-7-portrait-G04.png) |
| Pixel 7 · Landscape | 11 | 0 | 0 | [PNG](screenshots/gui/devices/pixel-7-landscape-G02.png) | [PNG](screenshots/gui/devices/pixel-7-landscape-G04.png) |
| Galaxy S24 · Portrait | 11 | 0 | 0 | [PNG](screenshots/gui/devices/galaxy-s24-portrait-G02.png) | [PNG](screenshots/gui/devices/galaxy-s24-portrait-G04.png) |
| Galaxy S24 · Landscape | 11 | 0 | 0 | [PNG](screenshots/gui/devices/galaxy-s24-landscape-G02.png) | [PNG](screenshots/gui/devices/galaxy-s24-landscape-G04.png) |
| iPhone 15 · Portrait | 11 | 0 | 0 | [PNG](screenshots/gui/devices/iphone-15-portrait-G02.png) | [PNG](screenshots/gui/devices/iphone-15-portrait-G04.png) |
| iPhone 15 · Landscape | 11 | 0 | 0 | [PNG](screenshots/gui/devices/iphone-15-landscape-G02.png) | [PNG](screenshots/gui/devices/iphone-15-landscape-G04.png) |
| iPad Pro 11 · Portrait | 11 | 0 | 0 | [PNG](screenshots/gui/devices/ipad-pro-11-portrait-G02.png) | [PNG](screenshots/gui/devices/ipad-pro-11-portrait-G04.png) |
| iPad Pro 11 · Landscape | 11 | 0 | 0 | [PNG](screenshots/gui/devices/ipad-pro-11-landscape-G02.png) | [PNG](screenshots/gui/devices/ipad-pro-11-landscape-G04.png) |
