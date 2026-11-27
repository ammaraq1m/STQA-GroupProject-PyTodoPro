# PyTodo Pro · Week 6 test automation and regression

| Item | Evidence |
| --- | --- |
| Execution | 2026-11-27T11:51:16.402032+00:00 to 2026-11-27T11:51:36.602675+00:00 · Git b39184b |
| Environment | Ubuntu 24.04.5 LTS x86_64 · Python 3.14.2 · Flask 3.0.3 · pytest 9.2.0 · Node 24.22.2 · Playwright 1.65.1 · headless Chromium 159.0.8154.6 |
| Review basis | [Group Project brief](../Group%20Project.pdf) · [Week 1 black-box results](../01_Black_Box/Blackbox%20Testing.md) · [Week 2 white-box results](../Week%202%20-%20White%20Box%20Testing/White-Box-Testing.md) · [Week 3 test report](../Week%203%20-%20GUI%20Compatibility%20Usability%20Accessibility%20Testing/WEEK_3_TEST_REPORT.md) · [Week 4 API results](../Week%204%20-%20Web%20and%20API%20Testing/API_TESTING.md) · [Week 5 test report](../Week%205%20-%20Security%20and%20Performance%20Testing/WEEK_5_TEST_REPORT.md) · original routes, helpers, templates and CSS |
| Isolation | Per-case SQLite files for pytest and a fresh Flask database for the browser run. Unique disposable browser accounts and contexts. |
| Wall time | 20.201 s overall, including 6.728 s pytest and 13.452 s Playwright child wall time. |

## Week 1–5 evidence inventory

| Source | Completed documented work | Manual, deferred or reuse decision |
| --- | --- | --- |
| Week 1 | 42 tests reported via pytest and Flask client, 32 pass and 10 fail. Report contains black-box equivalence and boundary cases. | Historical scripts named in the report are absent from this checkout. Retain original IDs and trace equivalent requirements. |
| Week 2 | 26 pytest checks, 22 pass and 4 fail. White-box helper boundaries and measured coverage. | Historical script named in the report is absent. Its completion boundary oracles informed GAP01–GAP04. The nested Week 3 manual checklists are templates marked Not run. |
| Week 3 | 141 automated cases (115 pass, 26 fail), plus 104 emulated-device cases (90 pass, 14 fail). Playwright and axe evidence reviewed. | Eight manual cases remain Not Run. Reuse Week 4 browser workflows with overlapping GUI coverage. Device and accessibility matrices are separate from this regression. |
| Week 4 | 43 automated cases, 29 pass and 14 fail. Two security runtime cases Not Run. | Reuse 20 API and 12 browser/comparison cases. Preserve A31/A32 as deferred. |
| Week 5 | 20 executed runtime or defensive source checks, 12 pass and 8 fail. Four runtime cases Not Run. Four Locust stages completed. | Reuse seven security cases. The threat model and source review are human analytical work. They do not establish completion of the manual workflow checklists. Load testing remains separate. |

No completed manual workflow records were present for the selected cases. The [traceability matrix](TRACEABILITY_MATRIX.md) maps historical manual procedures and requirements to executable cases and retains the original statuses.

## Final execution

| Group | Total | Pass | Fail | Not Run | Infrastructure errors |
| --- | --- | --- | --- | --- | --- |
| API reused | 20 | 11 | 9 | 0 | 0 |
| Security reused | 7 | 2 | 5 | 0 | 0 |
| Browser reused | 12 | 9 | 3 | 0 | 0 |
| New pytest | 6 | 3 | 3 | 0 | 0 |
| Deferred | 12 | 0 | 0 | 12 | 0 |
| **Total** | 57 | 25 | 20 | 12 | 0 |

All 39 reused cases matched their earlier outcomes. Six newly developed checks ran. GAP01 and GAP02 extended known completion-window defects to the HTML and API dashboards. GAP05 found the API update path also persists invalid due dates and causes later detail reads to fail. Three new checks passed. No tested prior defect resolved.

The initial staging failure was corrected in the Week 6 harness. Initial errors and unexecuted browser checks are archived separately and excluded from the final results. [Initial attempt](logs/initial-attempt/regression-results.json)

| Deliverable | Files |
| --- | --- |
| Selection and coverage | [Automation candidates](AUTOMATION_CANDIDATES.md) · [Traceability](TRACEABILITY_MATRIX.md) |
| Results and triage | [Regression testing](REGRESSION_TESTING.md) · [Defect report](DEFECT_REPORT.md) |
| Reuse and limits | [Automation reflection](AUTOMATION_REFLECTION.md) |
| Reproduction and data | [Runner](tests/run.py) · [Manifest](tests/manifest.json) · [Fixtures](test-data/FIXTURES.md) |

## Reproduce

From the repository root, run the one-time setup below in a Python environment. Use Node 24 and allow localhost port 51794. Project or historical files are read by the runner. Evidence is written to Week 6 only.

```bash
cd "Week 6 - Test Automation and Regression"
python -m pip install -r requirements.txt
npm --prefix tests ci
npm --prefix tests exec -- playwright install --with-deps chromium
```

Run the entire suite from the Week 6 folder with a single command.

```bash
python -B tests/run.py
```

The command returns nonzero while requirement assertions fail. It refreshes the current logs and screenshots. Compare [machine-readable results](logs/regression-results.json), [JUnit](logs/pytest-junit.xml) and [the evidence table](REGRESSION_TESTING.md).
