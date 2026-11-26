[WHITE_BOX_TEST_REPORT.md](https://github.com/user-attachments/files/35450703/WHITE_BOX_TEST_REPORT.md)
# PyTodo Pro: White-Box Testing and Coverage Report

## Overview

| Item | Detail |
| --- | --- |
| Application under test | PyTodo Pro (`helpers.py`) |
| Technique | White-box testing: statement, branch, path and data-flow analysis |
| Test framework | PyTest + Coverage.py |
| Test file | `tests/test_whitebox_helpers.py` |
| Result | 26 tests: **22 passed, 4 failed** |
| Defects found | 4 |
| Statement coverage | 100% (31/31) |
| Branch coverage | 100% (18/18) |

Application: PyTodo Pro | Execution date: 26 November 2026

## 1. Scope and selected code units

The objective is to examine internal decisions, execute targeted tests and measure statement and branch coverage. The four pure functions in helpers.py were selected because they implement business-critical validation and dashboard logic, and are explicitly designed for independent testing. The Flask routes in app(1).py are outside this selected scope; no full-application coverage is claimed.

| Code unit (source lines) | Purpose and justification |
| --- | --- |
| compute_urgency (12–39) | High: task scheduling; multiple date-based branches and boundary risks. |
| is_valid_password (42–49) | High: account validation; minimum-length boundary. |
| is_valid_username (52–58) | High: account validation; type, length and character rules. |
| completed_in_last_n_days (61–75) | Medium: dashboard accuracy; time-window boundaries and future dates. |

## 2. Method and environment

Review source and docstring requirements; identify decisions and data dependencies; design equivalence and boundary cases; execute PyTest; measure coverage with Coverage.py; compare expected and actual outputs; document defects. Expected outputs follow the documented specifications, rather than reproducing implementation errors.

Environment: Python 3.13.5, PyTest 9.0.2, Coverage.py 7.13.3, Linux. Fixed dates are injected for reproducibility, with separate tests for default clock branches. Original source is unchanged. Flask was unavailable in the execution environment; API and web integration tests were not executed.

## 3. Control-flow and data-flow analysis

### compute_urgency

Start → today missing? Set current date if yes → due date missing? Return No due date if yes → parse date → due ≤ today? Return Overdue if yes → calculate delta → delta ≤ 2? Due Soon : Upcoming.

Decisions: lines 26, 28, 33, 37. Inputs due_date_str and today define due and delta_days; the latter is used only for future dates. U01–U07 cover all decision exits; U03 exposes the missing Due Today outcome.

### is_valid_password

Start → input not a string? Return False if yes → return length > 8.

Decision: line 47; line 49 returns a Boolean. P01–P04 cover type and both Boolean results, including 7, 8 and 9 characters.

### is_valid_username

Start → not a string? Return False → length outside 3–20? Return False → all characters alphanumeric or underscore? Return result.

Decisions: lines 54, 56; character predicate at line 58. N01–N07 exercise both length boundaries, valid and invalid characters, and both predicate outcomes.

### completed_in_last_n_days

Start → timestamp missing? Return False → now missing? Set current time → parse timestamp → calculate age → return age.total_seconds() > 0 AND age.days < n.

Decisions: lines 69, 71; short-circuit expression at line 75. C01–C08 test missing values, default clock, future, zero, inside, exact and beyond the time window. age is derived from now and completed_at; the second condition is skipped for non-positive ages.

Coverage.py measures line-to-line branches, not every Boolean subexpression or all possible paths. Invalid date formats, alternative n values and exhaustive character combinations remain outside the test scope.

## 4. White-box test cases

Expected values derive from helpers.py docstrings. Dates are relative to 26 November 2026; completion ages are relative to 12:00:00 on that date, with n = 7.

| ID | Input / condition | Expected | Actual | Result |
| --- | --- | --- | --- | --- |
| U01 | No due date | No due date | No due date | Pass |
| U02 | Yesterday | Overdue | Overdue | Pass |
| U03 | Today | Due Today | Overdue | Fail |
| U04 | Tomorrow | Due Soon | Due Soon | Pass |
| U05 | +2 days | Due Soon | Due Soon | Pass |
| U06 | +3 days | Upcoming | Upcoming | Pass |
| U07 | No due date; default clock | No due date | No due date | Pass |
| P01 | None | False | False | Pass |
| P02 | 7 characters | False | False | Pass |
| P03 | 8 characters | True | False | Fail |
| P04 | 9 characters | True | True | Pass |
| N01 | None | False | False | Pass |
| N02 | ab | False | False | Pass |
| N03 | abc | True | True | Pass |
| N04 | 20 letters | True | True | Pass |
| N05 | 21 letters | False | False | Pass |
| N06 | ab_1 | True | True | Pass |
| N07 | ab! | False | False | Pass |

| ID | Input / condition | Expected | Actual | Result |
| --- | --- | --- | --- | --- |
| C01 | No completion | False | False | Pass |
| C02 | 1 second in future | False | False | Pass |
| C03 | Age = 0 seconds | True | False | Fail |
| C04 | Age = 1 second | True | True | Pass |
| C05 | 7 days minus 1 second | True | True | Pass |
| C06 | Exactly 7 days | True | False | Fail |
| C07 | 7 days plus 1 second | False | False | Pass |
| C08 | Yesterday; default clock | True | True | Pass |

## 5. Execution and measured coverage

26 tests executed: 22 passed and 4 failed (84.62% pass rate). Coverage results are measured from the same execution, including failed assertions.

| Function | Statements hit/total | Branches hit/total |
| --- | --- | --- |
| compute_urgency | 11/11 | 8/8 |
| is_valid_password | 3/3 | 2/2 |
| is_valid_username | 5/5 | 4/4 |
| completed_in_last_n_days | 7/7 | 4/4 |
| Module-level definitions/import | 5/5 | 0/0 |
| helpers.py total | 31/31 (100%) | 18/18 (100%) |

No statements or measured branches are uncovered within helpers.py. However, 100% structural coverage does not prove correctness, as shown by the four failing tests. app(1).py was not included in the coverage denominator. Exception paths and exhaustive combinations were not tested.

## 6. Reproduction commands

```bash
python -m pip install pytest coverage
python -m coverage run --branch --source=helpers -m pytest tests/test_whitebox_helpers.py -v --tb=short
python -m coverage report -m
python -m coverage html -d htmlcov
```

## 7. Defect analysis and recommendations

| Defect / source line | Cause and impact | Recommended correction |
| --- | --- | --- |
| BUG-01 / 33–34 | Due today is classified as overdue; urgency is misleading. | Use due < today for Overdue and a separate equality check for Due Today. |
| BUG-02 / 49 | Strict > 8 rejects a valid eight-character password. | Use len(password) >= 8. |
| BUG-03 / 75 | Strict positive age excludes tasks completed at the reference time. | Allow age of zero. |
| BUG-04 / 75 | age.days < n excludes the exact inclusive limit. | Compare timedelta(0) <= age <= timedelta(days=n). Import timedelta. |

The zero-age expectation interprets “within the last N days” as including the current instant. Future completions are assumed invalid. These are reasonable interpretations of the documented time-window rule.

## 8. Conclusion

The selected business logic was fully covered at statement and measured branch level, while boundary-value tests identified four functional discrepancies. Correct the defects, rerun the same suite, and extend testing to Flask authentication, task ownership and API validation in subsequent work. No fixes have been applied so that the evidence reflects the supplied implementation.

## 9. Supporting deliverables

`tests/test_whitebox_helpers.py`: automated tests; execution.txt: original PyTest output; coverage.txt and coverage.json: measured results; htmlcov/index.html: interactive coverage report; README.txt: reproduction instructions. The package includes an unchanged copy of helpers.py.

Source references: supplied helpers.py (lines 12–75), app(1).py (registration and dashboard usage), and Project Week 2 assignment instructions.

