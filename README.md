# PyTodo Pro | STQA Group Project

PyTodo Pro is the Flask and SQLite task manager evaluated for Software Testing and Quality Assurance (TEB3433 / TFB3433) at Universiti Teknologi PETRONAS in the September 2026 semester. This repository contains the supplied application and the group's test designs, execution evidence, defect reports and quality assessment.

## Team members

| Team member | Student ID | Project role |
| --- | --- | --- |
| Muhammad Adam Muzir bin Mohamad Azmi | 22006801 | QA/Test Lead |
| Muhammad Ammar Aqim bin Mohd Alwi | 22003435 | Test Design Coordinator |
| Ahmad Zamani Ridzwan bin Mohd Zawawi | 22006275 | Automation/Tool Coordinator |
| Ikmal Hakim bin Mohd Fahmi | 22005529 | Defect & Metrics Coordinator |

## Project deliverables

| Week | Deliverable |
| --- | --- |
| 1 | [Black-box test design, results and findings](01_Black_Box/Blackbox%20Testing.md) |
| 2 | [White-box analysis and reported helper coverage](Week%202%20-%20White%20Box%20Testing/White-Box-Testing.md) and [supplementary helper verification](Week%202%20-%20White%20Box%20Testing/RECOVERED_EVIDENCE.md) |
| 3 | [GUI, compatibility, usability and accessibility results](Week%203%20-%20GUI%20Compatibility%20Usability%20Accessibility%20Testing/WEEK_3_TEST_REPORT.md) |
| 4 | [Web, REST API and cross-interface testing](Week%204%20-%20Web%20and%20API%20Testing/WEEK_4_TEST_REPORT.md) |
| 5 | [STRIDE, defensive security checks and local performance results](Week%205%20-%20Security%20and%20Performance%20Testing/WEEK_5_TEST_REPORT.md) |
| 6 | [Test automation, traceability and regression results](Week%206%20-%20Test%20Automation%20and%20Regression/WEEK_6_TEST_REPORT.md) |
| 7 | [Test plan, strategy, RTM, master registers and execution summary](Week%207/README.md) |
| 8 | [Integrated QA evaluation, metrics and residual risks](Week%208/FINAL_QA_EVALUATION_REPORT.md) |
| 9 | [Standards integration](Week%209/STANDARDS_INTEGRATION.md), [presentation content](Week%209/PRESENTATION_CONTENT.md), [demo runbook](Week%209/LIVE_DEMONSTRATION.md) and [submission checklist](Week%209/FINAL_SUBMISSION_CHECKLIST.md) |

[Official group project guideline](Group%20Project.pdf)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

On Windows PowerShell, activate the environment with `.\.venv\Scripts\Activate.ps1`. The application creates `pytodo_pro.db` on first run and serves at `http://127.0.0.1:5000/`. Register a disposable account in the web UI or with `POST /api/register` to get started.

## Run automated tests

The recorded Week 6 run used Ubuntu 24.04, Python 3.14.2, Flask 3.0.3, pytest 9.2.0, Node.js 24.22.2 and Playwright 1.65.1 with Chromium. The runner uses its own temporary databases and starts the browser test server on loopback port 51794.

### Focused regression suite

Use a disposable checkout or copy because reruns replace the logs and screenshots in the suite's output directory. From the repository root with the virtual environment activated, run the setup and suite below.

```bash
cd "Week 6 - Test Automation and Regression"
python -m pip install -r requirements.txt
npm --prefix tests ci
npm --prefix tests exec -- playwright install --with-deps chromium
python -B tests/run.py
```

The runner can return a nonzero exit code when an assertion fails or an infrastructure problem occurs. Read the merged results to see the verdict for each case. The recorded final run had 25 Pass, 20 Fail and 12 Not Run. [Regression results](Week%206%20-%20Test%20Automation%20and%20Regression/logs/regression-results.json)

### Individual suites

| Suite | Setup and execution |
| --- | --- |
| Week 3 browser, device emulation and accessibility | [Playwright and axe-core commands](Week%203%20-%20GUI%20Compatibility%20Usability%20Accessibility%20Testing/WEEK_3_TEST_REPORT.md#reproduce-the-run) |
| Week 4 web and REST API | [Playwright and pytest commands](Week%204%20-%20Web%20and%20API%20Testing/WEEK_4_TEST_REPORT.md#reproduce-the-run) |
| Week 5 security and performance | [Defensive checks and local Locust commands](Week%205%20-%20Security%20and%20Performance%20Testing/WEEK_5_TEST_REPORT.md#reproduce) |

The original scripts and raw outputs behind the Weeks 1–2 baseline reports remain unavailable. The separately verified Week 2 helper suite provides supplementary evidence. [Week 2 reproduction commands](Week%202%20-%20White%20Box%20Testing/RECOVERED_EVIDENCE.md#reproduce)

## Application overview

### Web UI

- `/register`, `/login` and `/logout` manage accounts and sessions.
- `/` lists tasks with category and completion filters and title search.
- `/tasks/new` and `/tasks/<id>/edit` create and edit tasks.
- `/dashboard` shows total, open, overdue, due-soon and recently completed task counts.

### JSON REST API

- `POST /api/register` and `POST /api/login` accept `username` and `password` in the JSON body.
- `GET /api/categories` lists the four seeded categories. Registration, login and the category list are public. Task and dashboard requests require a session cookie.
- `GET /api/tasks?category=&status=&q=&page=&per_page=` lists, filters and paginates tasks.
- `POST /api/tasks` accepts `title`, `description`, `category_id` and `due_date` in `YYYY-MM-DD` format.
- `GET`, `PUT` and `DELETE /api/tasks/<id>` read, partially update and remove a task, respectively.
- `GET /api/dashboard` returns dashboard counters.

### Data model and urgency

- `users` stores `id`, `username` and `password_hash`.
- `categories` stores `id` and `name`, seeded with Work, Personal, Study and Urgent.
- `tasks` stores `id`, `user_id`, `title`, `description`, `category_id`, `due_date`, `done`, `completed_at` and `created_at`.

The documented task labels are `No due date`, `Overdue`, `Due Today`, `Due Soon`, `Upcoming` and `Done`. The helper defines the date boundaries, and the weekly reports record observed behavior. [Urgency helper](helpers.py)
