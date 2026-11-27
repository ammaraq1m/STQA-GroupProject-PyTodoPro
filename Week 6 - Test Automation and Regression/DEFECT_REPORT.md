# PyTodo Pro · Week 6 regression defect report

| Classification | Outcome |
| --- | --- |
| Persistent application findings | All 17 reused failing cases still failed against their original expectations. Two additional new cases confirmed previously known completion boundary bugs through both dashboard interfaces. |
| Resolved findings | None observed among the rerun cases. |
| Newly observed failure | GAP05 exposed the existing invalid-date validation problem in API update and showed that the resulting persisted data also makes the subsequent detail request fail. This is a new affected path under R04. |
| Infrastructure | The initial staging layout produced four source-check errors and prevented browser startup. Correcting the Week 6 harness resolved those errors. The final run had zero infrastructure errors. |
| Safe scope | R12 and R13 use defensive source checks. Prior adversarial runtime checks remain Not Run. |

| Week 6 ID | Regression evidence | Prior reference | Status |
| --- | --- | --- | --- |
| [R01](#r01) | A07 and W07 reject the documented password boundary. | W4 R01, W3 D01, W2 BUG-02 | Persistent |
| [R02](#r02) | A08 creates duplicate accounts. | W4 R03, W1 D05 | Persistent |
| [R03](#r03) | A16 produces HTML 500 for a numeric title. | W4 D01, W5 R01 | Persistent |
| [R04](#r04) | A18 persists an invalid date on create. GAP05 exposes update persistence and a failed later read. | W4 R05, W1 D09 | Persistent with new affected route |
| [R05](#r05) | W08 and I03 show that web creation saves missing or blank titles. | W4 R02, W3 D02 | Persistent |
| [R06](#r06) | A21 stores whitespace via API update. | W4 D02 | Persistent |
| [R07](#r07) | A22 completes the task when the input is the string false. | W4 D03 | Persistent |
| [R08](#r08) | A23 accepts truncated JSON as a successful update. | W4 D04 | Persistent |
| [R09](#r09) | A27 returns all 12 fixtures when given a negative page size. | W4 R06, W5 R04, W1 D08 | Persistent |
| [R10](#r10) | A30 describes a task due today as Overdue. | W4 R04, W2 BUG-01, W1 D02 | Persistent |
| [R11](#r11) | S06 observes missing cookie hardening flags. | W5 D01 | Persistent |
| [R12](#r12) | S15 confirms unsafe API search construction through source inspection. | W5 R02, W1 D06 | Persistent, source |
| [R13](#r13) | S16 confirms missing API delete owner scoping through source inspection. | W5 R03, W1 D07 | Persistent, source |
| [R14](#r14) | S17 observes a literal session signing key assignment. | W5 D02 | Persistent |
| [R15](#r15) | S19 observes missing form token markup and GET logout. | W5 D04 | Persistent |
| [R16](#r16) | GAP01 shows each dashboard excludes a completion exactly at the reference time. | W2 BUG-03 and C03, W1 D04 and TC26 | Persistent, new route evidence |
| [R17](#r17) | GAP02 shows each dashboard excludes a completion exactly at the seven-day cutoff. | W2 BUG-04 and C06, W1 D03 and TC24 | Persistent, new route evidence |

## Retest details and remediation

### R01

| Field | Detail |
| --- | --- |
| Severity | Moderate |
| Reproduce using | A07, W07 |
| Expected and observed | Eight-character password accepted → HTTP 400 or form validation error. |
| Recommendation | Apply the advertised inclusive minimum on both surfaces. |

### R02

| Field | Detail |
| --- | --- |
| Severity | Moderate |
| Reproduce using | A08 |
| Expected and observed | Duplicate rejected → both registration calls return 201 and two rows are written. |
| Recommendation | Enforce username uniqueness and handle duplicate conflicts. |

### R03

| Field | Detail |
| --- | --- |
| Severity | Major |
| Reproduce using | A16 |
| Expected and observed | Numeric title rejected with JSON 400 → HTML 500, no write. |
| Recommendation | Validate JSON shape and field types before string operations. |

### R04

| Field | Detail |
| --- | --- |
| Severity | Major |
| Reproduce using | A18, GAP05 |
| Expected and observed | Malformed date rejected with no write → HTTP 500 after persistence. Subsequent task detail GET subsequently returns 500 in GAP05. |
| Recommendation | Validate the date before committing either create or update. Retest that a rejected update keeps the previous valid date and readable resource. |

### R05

| Field | Detail |
| --- | --- |
| Severity | Moderate |
| Reproduce using | W08, I03 |
| Expected and observed | Missing or whitespace title rejected → web creates a blank task despite normal required-field enforcement. |
| Recommendation | Validate the trimmed title at the web endpoint and keep in-form feedback. |

### R06

| Field | Detail |
| --- | --- |
| Severity | Moderate |
| Reproduce using | A21 |
| Expected and observed | Reject spaces without changing the title → PUT succeeds and saves the spaces. |
| Recommendation | Apply the same normalized title rule to API create and update. |

### R07

| Field | Detail |
| --- | --- |
| Severity | Major |
| Reproduce using | A22 |
| Expected and observed | Reject non-boolean done → API returns 200, stores done and sets a timestamp. |
| Recommendation | Require a JSON boolean before state transitions. |

### R08

| Field | Detail |
| --- | --- |
| Severity | Moderate |
| Reproduce using | A23 |
| Expected and observed | Malformed JSON receives JSON 400 → API returns 200 with original task. |
| Recommendation | Handle parse errors distinctly from a valid empty partial update. |

### R09

| Field | Detail |
| --- | --- |
| Severity | Minor |
| Reproduce using | A27 |
| Expected and observed | Reject or cap negative page size → all 12 rows returned. |
| Recommendation | Validate and cap pagination. |

### R10

| Field | Detail |
| --- | --- |
| Severity | Moderate |
| Reproduce using | A30 |
| Expected and observed | Due Today → Overdue. |
| Recommendation | Handle due-date equality as its own class. |

### R11

| Field | Detail |
| --- | --- |
| Severity | Moderate |
| Reproduce using | S06 |
| Expected and observed | HTTPS deployment baseline has Secure and explicit SameSite → both flags absent. |
| Recommendation | Configure HTTPS cookie policy and retain HttpOnly. |

### R12

| Field | Detail |
| --- | --- |
| Severity | Critical |
| Reproduce using | S15, source |
| Expected and observed | Bound search value → source interpolation found. |
| Recommendation | Parameterize the search query. |

### R13

| Field | Detail |
| --- | --- |
| Severity | High |
| Reproduce using | S16, source |
| Expected and observed | Authenticated owner scope for deletion → source check finds no owner condition. |
| Recommendation | Apply owner scope to all task writes. |

### R14

| Field | Detail |
| --- | --- |
| Severity | High |
| Reproduce using | S17, source |
| Expected and observed | Signing key from deployment configuration → literal assignment present. |
| Recommendation | Configure a high-entropy deployment key and rotate the existing one. |

### R15

| Field | Detail |
| --- | --- |
| Severity | High |
| Reproduce using | S19, source |
| Expected and observed | Mutation forms have CSRF protection and logout uses POST → sampled forms lack token markup and logout uses GET. |
| Recommendation | Validate CSRF tokens at mutation routes and make logout POST-only. |

### R16

| Field | Detail |
| --- | --- |
| Severity | Moderate |
| Reproduce using | GAP01 |
| Expected and observed | Completion age zero counts → both dashboards report zero recent completions. |
| Recommendation | Include age zero within the valid window. Keep the future control excluded. |

### R17

| Field | Detail |
| --- | --- |
| Severity | Moderate |
| Reproduce using | GAP02 |
| Expected and observed | Exactly seven days ago counts → both dashboards report zero recent completions. |
| Recommendation | Include the exact seven-day boundary. Keep the older control excluded. |

The [regression table](REGRESSION_TESTING.md) and [machine-readable findings](logs/regression-results.json) contain expected and actual evidence. Prior keys refer to the [Week 1 defect table](../01_Black_Box/Blackbox%20Testing.md), [Week 2 white-box report](../Week%202%20-%20White%20Box%20Testing/White-Box-Testing.md), [Week 3 defect report](../Week%203%20-%20GUI%20Compatibility%20Usability%20Accessibility%20Testing/DEFECT_REPORT.md), [Week 4 defect report](../Week%204%20-%20Web%20and%20API%20Testing/DEFECT_REPORT.md), and [Week 5 defect report](../Week%205%20-%20Security%20and%20Performance%20Testing/DEFECT_REPORT.md).
