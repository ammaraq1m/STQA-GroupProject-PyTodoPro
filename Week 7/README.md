# PyTodo Pro · Week 7

| Deliverable | Use |
| --- | --- |
| [Software Test Plan](Software%20Test%20Plan.md) | Scope, baseline, milestones, owners, risks and proposed gates |
| [Test Strategy](Test%20Strategy.md) | Techniques, prioritization, tools and limitations by testing approach |
| [Requirements Traceability Matrix](Requirements%20Traceability%20Matrix.csv) | Requirement source and classification, mapped case IDs, evidence, open defects and coverage gaps |
| [Requirement Execution Links](Requirement%20Execution%20Links.csv) | Requirement-to-case-to-execution links for baseline and final results |
| [Master Test Cases](Master%20Test%20Cases.csv) | Original case designs, procedures, expected results, dispositions and overlap |
| [Master Defect Register](Master%20Defect%20Register.csv) | Consolidated findings, original defect references, verification and lifecycle |
| [Execution History](Execution%20History.csv) | Preserved observations by configuration, attempt and source week |
| [Execution and Regression Summary](Execution%20and%20Regression%20Summary.md) | Counts, rates, coverage, security, performance and gate assessment |

## Reading the registers

CSV files use UTF-8 with BOM. Open with a CSV-aware spreadsheet importer. IDs such as W2-U03 use the original week and source ID. The historical manual checklists are archived under Week 3 and retain their Week 3 master IDs and original Not Run statuses. EX IDs identify observations, including planned Not Run entries. Performance stages use Week 7-assigned LOAD IDs with the original stage user counts. Evidence references are repository-relative paths followed by a line, case ID, configuration or run locator. One observation can map to multiple requirements, so RTM counts are per requirement and should not be added across requirements. The RTM and Master Defect Register link each defect to the requirements it directly affects. Requirement Execution Links retain case-level defect references because a single execution can exercise several assertions.

Defect severity reflects impact. Critical covers potential severe compromise, High covers major integrity, access or workflow impact, Medium covers material correctness or usability with limited scope, and Low covers bounded impact. Priority reflects recommended action order. P1 addresses immediate security and data risks, P2 significant barriers, P3 normal remediation and P4 lower-impact improvements. Severity and priority are Week 7 triage judgments. Owners and waivers remain TBD. Cases with related open defects can still pass on a different surface or control.

Duplicate references were merged when the evidence pointed to the same faulty control or boundary. The API date write defect spans create and update. Web blank titles and API whitespace updates retain separate records because the code paths validate differently and need independent confirmation. The two completion boundaries have different failing conditions and separate cases. Expected controls inferred from the code or weekly checks remain subject to approval.

## Evidence baseline

[Project brief](../Group%20Project.pdf) · [Application README](../README.md) · [Week 1](../01_Black_Box/Blackbox%20Testing.md) · [Week 2](../Week%202%20-%20White%20Box%20Testing/White-Box-Testing.md) · [Week 3](../Week%203%20-%20GUI%20Compatibility%20Usability%20Accessibility%20Testing/WEEK_3_TEST_REPORT.md) · [Week 4](../Week%204%20-%20Web%20and%20API%20Testing/WEEK_4_TEST_REPORT.md) · [Week 5](../Week%205%20-%20Security%20and%20Performance%20Testing/WEEK_5_TEST_REPORT.md) · [Week 6](../Week%206%20-%20Test%20Automation%20and%20Regression/WEEK_6_TEST_REPORT.md)

Work on Week 7 reconciled existing results. The original scripts and raw output for the Week 1 and Week 2 baseline reports remain unavailable. The original outcomes are retained as report-level evidence. The separately verified 42-invocation helper suite is supplementary evidence. The Week 1 human manual session has its own results and traceability table. [Week 1 supplementary traceability](Execution%20and%20Regression%20Summary.md#week-1-supplementary-manual-verification) [Week 2 supplementary verification](../Week%202%20-%20White%20Box%20Testing/RECOVERED_EVIDENCE.md)
