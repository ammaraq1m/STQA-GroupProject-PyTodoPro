# PyTodo Pro execution and regression summary

**The proposed test exit criteria remain unmet.** The Week 6 final regression passed 25 of 45 executed checks and failed 20. Open findings include 1 Critical and 9 High defects. The evidence baseline is Weeks 1–6 as stored at repository revision `17f54e1`.

## Results by run

Pass rate = Pass ÷ (Pass + Fail). Planned or recorded observations include Not Run and Blocked. A row represents a test verdict at its reported granularity, so repeated configurations and reruns increase execution counts. Performance stages are reported separately.

| Evidence group | Pass | Fail | Blocked | Not Run | Total records | Pass rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| W1 black-box report | 32 | 10 | 0 | 0 | 42 | 76.19% |
| W2 white-box report | 22 | 4 | 0 | 0 | 26 | 84.62% |
| W3 engine matrix | 115 | 26 | 0 | 0 | 141 | 81.56% |
| W3 device emulation extension | 90 | 14 | 0 | 0 | 104 | 86.54% |
| W3 planned manual and historical templates | 0 | 0 | 0 | 41 | 41 | — |
| W4 web, API and comparison | 29 | 14 | 0 | 2 | 45 | 67.44% |
| W5 security | 12 | 8 | 0 | 4 | 24 | 60.00% |
| W6 final regression | 25 | 20 | 0 | 12 | 57 | 55.56% |
| **Baseline and final total** | **325** | **96** | **0** | **59** | **480** | **77.20%** |
| W6 initial attempt, archived separately | 16 | 13 | 16 | 12 | 57 | 55.17% |

The initial attempt includes four pytest source-check infrastructure errors and twelve browser checks that did not start. They are recorded as Blocked. The Week 3 sandbox startup failure is recorded as a run-level incident because no case-level outcomes were produced. Week 3 manual records include eight explicitly deferred cases and 33 checklist designs. Each of the seven COM configurations contributes one bundled checklist design with five workflow checkpoints. [Week 3 sandbox incident](../Week%203%20-%20GUI%20Compatibility%20Usability%20Accessibility%20Testing/logs/sandbox-execution.log) · [Full execution history](Execution%20History.csv)

## Week 1 supplementary manual verification

A group tester executed the nine Week 1 supplementary cases in Microsoft Edge on 27 November 2026 MYT using revision 1e11392 and an isolated temporary SQLite database. There were 9 planned, 9 executed, 8 Pass, 1 Fail, 0 Blocked and 0 Not Run. Execution was 100.00% (9/9) and the pass rate was 88.89% (8/9). The historical 480-record baseline and original requirement and design denominators remain the basis of the preceding results. [Case procedures, observations and screenshots](../01_Black_Box/SUPPLEMENTARY_MANUAL_TESTING.md)

| Supplementary case | Requirements | Design rule | Verdict | Defect or evidence note |
| --- | --- | --- | --- | --- |
| W1-M01 | F01 | Registration R2, two-character username | Pass | Expected username error observed. |
| W1-M02 | F02 | Registration R3, seven-character password | Pass | Expected password error observed. |
| W1-M03 | F01, F02 | Registration R4, both inputs invalid | Pass | Username error appeared first. |
| W1-M04 | F01, F02, F03 | Registration R1, eight-character boundary | Fail | Reconfirmed existing DEF-001. |
| W1-M05 | F01, F02, F03 | Registration R1, nine-character control | Pass | My Tasks opened as p09. |
| W1-M06 | F16 | Filter T7, title and Done status | Pass | Only Phase Alpha Review shown with search alpha and All categories. |
| W1-M07 | F08, F14 | S1–S3, create, complete and reopen | Pass | Reopen captured. Completion observation supplied by the tester. The planned Done screenshot is unavailable. |
| W1-M08 | F15 | S5–S6, cancel and confirm deletion | Pass | The task remained after Cancel and disappeared after confirmation. |
| W1-M09 | F08 | S7, open a stale web Edit URL | Pass | My Tasks opened and the deleted task remained absent. |

DEF-001 remains open in the consolidated register. M04 adds human verification of the same failure. [Master defect register](Master%20Defect%20Register.csv)

## Design and requirement coverage

| Measure | Result |
| --- | --- |
| Distinct source designs | 225 total. W1 42, W2 26, W3 78, W4 45, W5 28, W6 6. Includes four load-stage designs, with synthetic IDs because the source used user counts. |
| Designs with a Pass or Fail | 174 of 225. Four more were measured. The remaining 47 are manual or deferred runtime records. |
| Automation coverage | 106 executable assertion-based case designs present in repository, 68 earlier designs reported automated with scripts absent, four automated measurement designs. Combined historical automation 178/225 (79.11%), with 110/225 (48.89%) represented by current scripts including load. |
| Requirement design coverage | 39/44 (88.64%) have mapped cases. Of 44 requirements, 12 are explicit and 32 inferred. |
| Requirement execution coverage | 35/44 (79.55%) have a verdict or measurement. 23 have at least one failure, 11 have passing evidence only among executed verdicts, and one has measurements. Passing evidence can coexist with unverified scope. |
| Structural coverage | Week 2 reports 31/31 statements and 18/18 measured branches for helpers.py. Application-wide coverage is unavailable. |

Designs describe the original test procedures. Overlapping manual, helper, API and GUI designs retain their source IDs when layers, fixtures or oracles differ. The same design repeated across browser profiles or rerun in Week 6 retains its master ID. Deferred historical planning IDs such as W4-A31 and W5-N01 remain visible with their overlap marked. The Week 6 12 deferrals refer back to existing cases.

Five requirements lack designed historical cases. These cover peer web toggle/delete, unknown categories, duplicate web registration, production-like performance targets and persistence across restart. Four have designs with only Not Run evidence. These cover untrusted browser content, deployed TLS, participant usability and native assistive technology. Partial gaps include physical devices, native zoom, contrast, broader validation and the current runtime verification of API search and deletion controls. [RTM](Requirements%20Traceability%20Matrix.csv)

## Week 6 regression and defect status

| Group | Pass | Fail | Not Run |
| --- | ---: | ---: | ---: |
| Reused API | 11 | 9 | 0 |
| Reused security | 2 | 5 | 0 |
| Reused browser/comparison | 9 | 3 | 0 |
| New Flask integration | 3 | 3 | 0 |
| Deferred | 0 | 0 | 12 |

All 39 reused cases retained their earlier verdicts, including 17 failures. GAP01 and GAP02 confirmed the two completion-window failures through both dashboards. GAP05 extended the invalid-date persistence defect to update and subsequent owner reads. The other three new cases passed. Week 6 confirms 17 master defects still open, including source confirmation for security controls. Twelve others retain their last confirmation from earlier weeks. The harness recovered from its initial failure. No application defect has closure evidence. [Week 6 results](../Week%206%20-%20Test%20Automation%20and%20Regression/REGRESSION_TESTING.md) · [Master defect register](Master%20Defect%20Register.csv)

Each block represents one open defect.

```text
Critical   █               1
High       █████████       9
Medium     ██████████████ 14
Low        █████           5
```

Priority totals are P1 3, P2 7, P3 14 and P4 5. P1 covers unsafe API search construction, missing API delete owner scope and the literal signing key. Sampled authentication, salted password storage, cookie HttpOnly, owner list/detail/read-update controls and ordinary search passed. Missing deployment cookie flags, CSRF controls and durable audit evidence remain open. Week 5 STRIDE T08 also flags the task-title escaping override in source. The browser runtime case remains Not Run. Week 5–6 search and deletion findings come from defensive source review. Week 1 reports runtime failures, and corresponding later runtime retests remain deferred. [Week 5 security findings](../Week%205%20-%20Security%20and%20Performance%20Testing/SECURITY_TESTING.md)

## Performance

| Users | Pinned requests | Request failures | Pinned req/s | Pinned P95 ms | Preliminary P95 ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 60 | 0 | 1.00 | 10 | 16 |
| 5 | 300 | 0 | 5.00 | 36 | 33 |
| 10 | 600 | 0 | 10.00 | 60 | 64 |
| 25 | 1,500 | 0 | 25.00 | 120 | 140 |

Each run measured 2,460 requests with zero failures across four paced, 60-second stages. The pinned run had highest endpoint P95 of 130 ms on the web task list at 25 users, with peak combined RSS 144.1 MiB and peak sampled host CPU 44%. Raw requests and eight stage observations are outside the case pass-rate denominator. The preliminary stack used Flask 3.1.3 and the pinned stack used Flask 3.0.3. The values describe separate local experiments with no approved service-level target or saturation threshold. [Week 5 performance report](../Week%205%20-%20Security%20and%20Performance%20Testing/PERFORMANCE_TESTING.md) · [Latency chart](../Week%205%20-%20Security%20and%20Performance%20Testing/charts/latency.png) · [Throughput and error chart](../Week%205%20-%20Security%20and%20Performance%20Testing/charts/throughput-errors.png)

## Exit decision

E1 remains unmet due to incomplete high-risk coverage. E2 remains unmet due to open Critical, High and P1 defects. E3 remains unmet with 20 final failures despite zero final infrastructure errors. E4 remains unmet with failing layout/accessibility cases, pending native tests and TBD deployment thresholds. E5 awaits a named reviewer and approval. Outstanding manual work includes three physical-device checks, two participant sessions, three native accessibility checks, and historical checklist procedures with no manual results. [Software Test Plan](Software%20Test%20Plan.md)
