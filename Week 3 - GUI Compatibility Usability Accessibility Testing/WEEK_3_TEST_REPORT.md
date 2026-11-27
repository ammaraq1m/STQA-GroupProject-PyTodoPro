# PyTodo Pro · Week 3 test report

| Item | Detail |
| --- | --- |
| Execution | 2026-11-27T10:29:20.966Z through 2026-11-27T10:30:34.393Z |
| Scope | Browser UI for registration, login, task workflows, dashboard, filters and logout. Selected usability heuristics and WCAG 2.2 A/AA checks. |
| Basis | [Project brief](../Group%20Project.pdf), [README](../README.md), [Week 1](../01_Black_Box/Blackbox%20Testing.md), [Week 2](../Week%202%20-%20White%20Box%20Testing/White-Box-Testing.md), Flask routes, helpers, all HTML templates and the shared CSS. |
| Environment | Ubuntu 24.04.5 LTS x86_64 · Python 3.14.2 · Flask 3.0.3 · Node v24.22.2 · Playwright 1.65.1 · axe-core 4.14.1 |
| Isolation | Flask listened on loopback. The harness set the database path to a fresh temporary SQLite database before initialization. Each configuration received a new browser context and QA account. |
| Evidence | [Execution log](logs/execution.log) · [Flask log](logs/flask.log) · [Structured results](logs/results.json) · [Screenshots](screenshots/) · [Automated scripts](tests/) |

## Execution summary

| Category | Automated planned | Executed | Pass | Fail | Automated Not Run | Manual Not Run |
| --- | --- | --- | --- | --- | --- | --- |
| GUI | 107 | 107 | 103 | 4 | 0 | 0 |
| Compatibility | 18 | 18 | 9 | 9 | 0 | 3 |
| Usability | 3 | 3 | 0 | 3 | 0 | 2 |
| Accessibility | 13 | 13 | 3 | 10 | 0 | 3 |
| Total | 141 | 141 | 115 | 26 | 0 | 8 |

Counts are individual test case executions per configuration. An axe scan is one case per page state regardless of violation count. Usability failures represent gaps against the stated heuristic expectations.

| Area | Coverage and outcome | Deliverable |
| --- | --- | --- |
| GUI | Core workflows across the browser matrix. Boundary validation and visual consistency checks on Chromium desktop. | [GUI testing](GUI_TESTING.md) |
| Compatibility | Three engines across desktop, tablet and mobile profiles. Narrow and mobile layout issues affect the tested configurations as shown in the matrix. | [Compatibility testing](COMPATIBILITY_TESTING.md) |
| Usability | Scripted checks verify navigation, feedback and error prevention. Participant testing is pending. | [Usability testing](USABILITY_TESTING.md) |
| Accessibility | Seven axe state scans and six targeted Playwright checks. Priority findings include missing names, low contrast and reflow. | [Accessibility testing](ACCESSIBILITY_TESTING.md) |
| Defects | 13 confirmed defects or usability gaps. Earlier password and due-date boundary findings reproduce through the GUI. | [Defect report](DEFECT_REPORT.md) |

## Reproduce the run

From the repository root, install the Flask requirements into an available Python environment. If needed, set QA_PYTHON to the interpreter path. The test runner expects loopback port 51793 to be available.

```bash
python -m pip install -r requirements.txt
cd "Week 3 - GUI Compatibility Usability Accessibility Testing/tests"
npm ci
npx playwright install --with-deps chromium firefox webkit
npm test
```

The runner rewrites current execution artifacts in the Week 3 folder and exits nonzero for any failed check or execution error. Preserve the supplied evidence before rerunning if you need a historical copy. The first startup attempt was blocked by the workspace sandbox and is retained in the sandbox logs. Results in the tables come from the localhost run.

## Device emulation extension

A separate run used Playwright’s iPhone 15, Pixel 7, Galaxy S24 and iPad Pro 11 profiles in portrait and landscape. Results below are additional to the original execution summary. All profiles were emulated. The three original physical-device cases remain Not Run because physical-device sessions were unavailable. [Compatibility matrix and screenshots](COMPATIBILITY_TESTING.md#playwright-device-emulation-extension)

| Additional checks | Executed | Pass | Fail | Not Run |
| --- | --- | --- | --- | --- |
| Core GUI (G01–G11) | 88 | 88 | 0 | 0 |
| Compatibility layout (C01–C02) | 16 | 2 | 14 | 0 |
| Total | 104 | 90 | 14 | 0 |

From the Week 3 tests directory, use `npm test -- --devices` after installing the dependencies in the original setup instructions. The extension writes [device results](logs/devices-results.json), [execution log](logs/devices-execution.log), [Flask log](logs/devices-flask.log) and screenshots in the device subfolders.
