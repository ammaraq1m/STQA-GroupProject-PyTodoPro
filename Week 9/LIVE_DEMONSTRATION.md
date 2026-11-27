# PyTodo Pro · Live demonstration runbook

Allow four minutes once setup is complete. Present the task workflow, one passing and one known failing regression check, the linked defect, and the coverage or load evidence. Start in the repository root in Bash on Linux. Use Python 3.14.2, a desktop browser and a free loopback port 51796. The optional full regression also requires Node 24.22.2, Chromium and its system libraries, and free port 51794. Install dependencies in advance. All demo files, databases and new logs go into a temporary directory. [Application setup](../README.md) · [Historical Week 6 environment](../Week%206%20-%20Test%20Automation%20and%20Regression/WEEK_6_TEST_REPORT.md)

## Preflight and stage

Run in Terminal A. Preserve the displayed temporary path for Terminal B.

```bash
demo_root="$(mktemp -d /tmp/pytodo-week9-demo.XXXXXX)"
mkdir -p "$demo_root/demo/tests" "$demo_root/demo/logs"
cp app.py helpers.py "$demo_root/"
cp -R templates static "$demo_root/"
cp 'Week 4 - Web and API Testing/tests/test_api.py' \
   'Week 6 - Test Automation and Regression/tests/test_gaps.py' "$demo_root/demo/tests/"
python -m venv "$demo_root/venv"
"$demo_root/venv/bin/python" -m pip install -r 'Week 6 - Test Automation and Regression/requirements.txt'
printf 'Demo directory: %s\n' "$demo_root"
cd "$demo_root"
venv/bin/python -B -c 'from app import app, init_db; init_db(); app.run(host="127.0.0.1", port=51796, debug=False)'
```

Expected: Flask serves `http://127.0.0.1:51796` and creates SQLite in the temporary copy. Open that URL in a fresh browser window. Register `week9_demo` with a disposable password longer than eight characters. Create `Week 9 presentation` with category Study and a future due date. The task appears on My Tasks. Complete it, check that the badge reads Done, then visit Dashboard. Expect Total 1 and Open 0. Allow a second before showing the recent completion count because this build has a zero-age boundary defect. The register/create/complete/dashboard sequence was rehearsed using the Flask test client in a disposable copy. Rehearse the browser delivery on the presentation machine. Press Ctrl+C in Terminal A after the demonstration.

## Run a successful and a previously failing case

In Terminal B, substitute the path printed by Terminal A on the first line.

```bash
demo_root=/tmp/pytodo-week9-demo.REPLACE_ME
cd "$demo_root/demo"
../venv/bin/python -B -m pytest -p no:cacheprovider -q --tb=short \
  --junitxml=logs/demo-junit.xml \
  'tests/test_api.py::test_A01_registration' \
  'tests/test_gaps.py::test_dashboard_completion_window[GAP02]'
printf 'Pytest exit: %s\n' "$?"
```

Expected output includes `.F`, `1 failed, 1 passed` and `Pytest exit: 1`. A01 passes registration with HTTP 201 and expected account/session and stored-password checks. GAP02 freezes the clock and checks a task completed exactly seven days earlier. Both dashboards respond normally but count zero instead of one. The selected two cases were rehearsed in an isolated copy during Week 9 with Python 3.14.2, Flask 3.0.3 and pytest 9.2.0. The new rehearsal is separate from Week 8 totals. Distinguish the known assertion mismatch from setup, collection or fixture errors. If a future revised build passes this case, show the new result and validate the fix before updating status. [Historical regression case results](../Week%206%20-%20Test%20Automation%20and%20Regression/REGRESSION_TESTING.md)

## Show the evidence chain

1. Open the [RTM](../Week%208/RTM_TEMPLATE_VIEW.csv) and find F19 / W6-GAP02. Open [DEF-003](../Week%208/MASTER_DEFECT_REGISTER.csv) by searching for its ID.
2. Compare the expected/actual counts with the focused regression result or the new JUnit and console output. The open defect records the boundary and both affected dashboards. [Week 6 defect evidence](../Week%206%20-%20Test%20Automation%20and%20Regression/DEFECT_REPORT.md#r17)
3. Show [Week 2 helper coverage](../Week%202%20-%20White%20Box%20Testing/White-Box-Testing.md#5-execution-and-measured-coverage) (31/31 statements and 18/18 branches in `helpers.py`, four failed assertions). Alternatively show the [pinned load chart](../Week%208/charts/performance_latency.svg) (120 ms P95 at 25 paced users, 0/2,460 timed failures) and its [workload limits](../Week%205%20-%20Security%20and%20Performance%20Testing/PERFORMANCE_TESTING.md).

## Optional full regression rehearsal

Use a new terminal at the repository root. This takes longer than the live segment and may require pre-installed system packages or administrator access for Playwright. The copy omits historical logs and screenshots. Keep the two-case demonstration as the timed version.

```bash
full_root="$(mktemp -d /tmp/pytodo-week9-full.XXXXXX)"
cp app.py helpers.py "$full_root/"
cp -R templates static "$full_root/"
for week in 'Week 4 - Web and API Testing' 'Week 5 - Security and Performance Testing' 'Week 6 - Test Automation and Regression'; do
  mkdir -p "$full_root/$week/tests"
  cp "$week"/tests/*.* "$full_root/$week/tests/"
done
python -m venv "$full_root/venv"
"$full_root/venv/bin/python" -m pip install -r 'Week 6 - Test Automation and Regression/requirements.txt'
cd "$full_root/Week 6 - Test Automation and Regression"
export PLAYWRIGHT_BROWSERS_PATH="$full_root/browser-cache"
npm --prefix tests ci --cache "$full_root/npm-cache"
npm --prefix tests exec -- playwright install --with-deps chromium
"$full_root/venv/bin/python" -B tests/run.py
printf 'Regression exit: %s\n' "$?"
```

Historical comparison point: exit 1 with 25 Pass, 20 Fail, zero Infrastructure Error and 12 Not Run. On 27 November 2026 at 14:13 UTC the isolated Week 9 rehearsal matched every recorded case status and all five staged input hashes. It finished in 23.691 seconds. The first Week 9 attempt could not open its loopback socket in the sandbox. Its 12 unstarted browser cases were infrastructure-blocked for that attempt, and the loopback-enabled rerun recovered them. The output belongs to the temporary copy. Inspect its actual statuses before comparing. Unexpected counts can reflect runner or environment differences and should be shown as such. [Archived machine results](../Week%206%20-%20Test%20Automation%20and%20Regression/logs/regression-results.json)

## Backup if live execution fails

Keep the [CRUD screenshot](../Week%204%20-%20Web%20and%20API%20Testing/screenshots/web/W04.png), [dashboard screenshot](../Week%204%20-%20Web%20and%20API%20Testing/screenshots/web/qa_w06-dashboard.png), [archived A01 and GAP02 results](../Week%206%20-%20Test%20Automation%20and%20Regression/REGRESSION_TESTING.md), RTM, defect register and coverage table open or available offline. State the specific startup, dependency or test error. Walk the workflow with screenshots, explain the archived pass/fail and link DEF-003 to evidence. Identify each artifact as a previous result when presenting it. Stop any running local demo server and close the browser session after delivery.
