# PyTodo Pro · Week 4 web and API test report

| Item | Detail |
| --- | --- |
| Execution date | 27 November 2026 UTC |
| Application | PyTodo Pro, repository revision 251617c |
| Review basis | [Group Project brief, page 3](../Group%20Project.pdf) · [Week 1](../01_Black_Box/Blackbox%20Testing.md) · [Week 2](../Week%202%20-%20White%20Box%20Testing/White-Box-Testing.md) · [Week 3](../Week%203%20-%20GUI%20Compatibility%20Usability%20Accessibility%20Testing/WEEK_3_TEST_REPORT.md) · Flask routes, helpers and HTML templates |
| Environment | Ubuntu 24.04.5 LTS x86_64, Python 3.14.2, Flask 3.0.3, pytest 9.2.0, Node 24.22.2, Playwright 1.65.1 and Chromium headless 159.0.8154.6 |
| Isolation | Playwright used a local Flask process and temporary SQLite database. Pytest used a fresh test-client SQLite database for each case. Accounts were disposable. Credential and cookie values are excluded from request evidence. |
| Scope | Web workflows and form validation, REST CRUD, request parsing, authentication/session behaviour, owner scoping, pagination, search, filters, dashboard and shared state. |
| Outcomes | 4 new defects and 6 prior defects reconfirmed. Two prior security cases remain Not Run in this execution. |

## Execution totals

| Suite | Total planned | Executed | Pass | Fail | Not Run | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Web | 8 | 8 | 6 | 2 | 0 | [Web results and screenshots](WEB_TESTING.md) |
| REST API | 33 | 31 | 20 | 11 | 2 | [API results](API_TESTING.md) |
| UI/API comparison | 4 | 4 | 3 | 1 | 0 | [Comparison results and screenshots](UI_API_COMPARISON.md) |
| **Total** | **45** | **43** | **29** | **14** | **2** | [Defect report](DEFECT_REPORT.md) |

Counts represent cases. One case can check several HTTP requests or database facts. Multiple failures can trace to a single defect.

| Area | Finding |
| --- | --- |
| Core workflows | Authenticating, task CRUD and completion, filtering and dashboard calculations passed with the valid fixtures. Core UI/API round trips and shared logout passed. |
| Validation | Some incorrect JSON types return HTML 500. An invalid date returns 500 after writing the record. PUT accepts whitespace titles and coerces the string "false" to completed. |
| Cross-interface behaviour | Required-field enforcement runs in the browser. The web endpoint still saves a missing or spaces-only title, while API create rejects those inputs. |
| Session and ownership | Independent disposable sessions see their own lists and dashboards. Non-owner read and update returned 404, and anonymous API task operations returned 401. |
| Remaining scope | A31 and A32 are listed in the API report as Not Run. Prior Week 1 findings remain traceable in the defect report. |

## Reproduce the run

From the repository root, install dependencies, then run both suites from the Week 4 folder. The browser runner requires loopback port 51794 and uses QA_PYTHON if set.

```bash
python -m pip install -r requirements.txt pytest==9.2.0
cd "Week 4 - Web and API Testing"
npm --prefix tests ci
npm --prefix tests exec -- playwright install --with-deps chromium
python -B -m pytest -p no:cacheprovider --tb=short -v --junitxml=logs/api-junit.xml tests/test_api.py > logs/api-execution.log 2>&1
npm --prefix tests test > logs/web-execution.log 2>&1
```

The suites return nonzero when an assertion fails. Reruns overwrite the current Week 4 evidence files. See the [request fixtures](test-data/FIXTURES.md), [API requests and responses](logs/api-responses.ndjson), [web HTTP evidence](logs/web-results.json) and [Flask access log](logs/web-flask.log).
