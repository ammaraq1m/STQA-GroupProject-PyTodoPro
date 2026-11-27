# Week 2 supplementary helper verification

The recovered `test_helpers.py` and `coverage_report.txt` were uploaded in commit `fbab8e8`. The uploaded log reports Python 3.12.3, pytest 9.2.0 and the `pytest-cov` plugin. It recorded 42 collected invocations, with 38 Pass and four strict XFAIL. Coverage applies to `helpers.py` and shows 31/31 statements and 18/18 measured branches. [Uploaded test script](test_helpers.py) · [Uploaded execution and coverage log](coverage_report.txt)

The historical Week 2 report describes a separate 26-case run under Python 3.13.5 and pytest 9.0.2, with 22 Pass and four Fail. Its script name, case IDs and inputs differ from the recovered suite. Its original script and raw output remain unavailable. The 26-case report remains the Week 7–9 metrics baseline. The supplementary suite overlaps that baseline, and each verification below reruns the same 42 invocations. [Historical Week 2 report](White-Box-Testing.md) · [Baseline metrics](../Week%208/SOFTWARE_QUALITY_METRICS.md)

## Independent verification

On 27 November 2026, the uploaded suite was rerun against the repository's `helpers.py` in a disposable directory on Linux using Python 3.14.2, pytest 9.2.0 and Coverage.py 7.13.3.

| Run | Observed result | Statement coverage | Measured branch coverage |
| --- | --- | ---: | ---: |
| Uploaded markings applied | 38 Pass, 4 XFAIL | 31/31 | 18/18 |
| `--runxfail` applied to expose the underlying assertions | 38 Pass, 4 Fail | 31/31 | 18/18 |

The same four assertions failed. The report associates each supplementary test with the corresponding historical expectation and master defect.

| Behaviour | Supplementary case | Historical Week 2 case and defect | Master defect |
| --- | --- | --- | --- |
| A task due today should display Due Today | U5 | U03 / BUG-01 | DEF-002 |
| An eight-character password should be valid | P2 | P03 / BUG-02 | DEF-001 |
| A completion at the reference instant should count | C8 | C03 / BUG-03 | DEF-004 |
| A completion exactly seven days earlier should count | C6 | C06 / BUG-04 | DEF-003 |

The second run exercised the same expected outcomes with pytest's XFAIL handling disabled. The uploaded suite and application files were preserved. Coverage describes the statement and branch outcomes counted by Coverage.py for the helper module.

## Reproduce

Run from the repository root with a Python virtual environment active. The coverage data is stored in a temporary directory.

```bash
python -m pip install pytest==9.2.0 coverage==7.13.3
export COVERAGE_FILE="$(mktemp -d)/.coverage"
python -B -m coverage run --branch --source=helpers -m pytest -p no:cacheprovider -q -rx "Week 2 - White Box Testing/test_helpers.py"
python -B -m coverage report -m
python -B -m coverage run --branch --source=helpers -m pytest -p no:cacheprovider -q --runxfail --tb=short "Week 2 - White Box Testing/test_helpers.py"
python -B -m coverage report -m
```

The second pytest invocation returns exit code 1 when the four documented assertions fail. The following coverage report is still available.
