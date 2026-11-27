# PyTodo Pro · Documentation compliance

Pages 5–6 of the project brief define the test case, defect report and RTM templates. This review covers all 225 master test designs, 29 canonical defects and 44 requirements in the Week 7 registers. The Week 8 CSVs use UTF-8 with BOM. Use a CSV-aware viewer for quoted multiline procedures. [Group Project.pdf](../Group%20Project.pdf) · [Week 7 test cases](../Week%207/Master%20Test%20Cases.csv) · [Week 7 defects](../Week%207/Master%20Defect%20Register.csv)

## Master test cases

| Required field | Week 7 review and Week 8 treatment |
| --- | --- |
| Test Case ID | Master test ID was present and unique. The new copy uses the brief's field name. |
| Feature/Requirement | Requirement IDs were present. The new copy expands them with Week 7 RTM descriptions. |
| Technique/Test Type | Testing category was present. Technique detail varies with the historical design and is preserved. |
| Objective | Week 7 used Test scenario. The Objective column uses the documented behaviour or scenario as the available objective. |
| Preconditions | Present. Some entries describe a general fixture. Exact setup depends on the linked historical case and execution environment. |
| Test Data | Present as literals, descriptions or cross-references. When the source lacks a fully specified fixture, the source description is the available detail. |
| Steps | Mixed numbered sequences and prose. Week 8 uses numbered procedures. A compact historical operation can remain one numbered step. Sensitive security cases reference the historical evidence through a defensive review step. |
| Expected Result | Present. Some oracles are inferred or provisional, as recorded in the RTM. |
| Actual Result | Present as observations, deferred reasons or measurements. Deferred cases explicitly say that execution was unavailable. |
| Status | Week 7 mixed outcomes and counts in one field. The template copy has a canonical verdict: Fail if any observed configuration failed, Pass if observed verdicts all passed, Not Run if there is no assertion verdict, and Blocked for any applicable standalone block. Original outcome summary and execution IDs retain the details. |
| Evidence | Repository-relative paths and source locators were present. The source file and execution/case identity are retained. For planned-only records, the source documents the plan or deferral. |
| Defect ID | 161 records have no linked defect, now marked N/A. Existing mapped IDs are preserved. |

The four load designs recorded eight measurements. Their template status is **Not Run for an acceptance verdict** because thresholds were unavailable. Their Actual Result, Original outcome summary and Original measurement procedure explicitly record the completed experiments. Verdict counts exclude these four designs. Both mixed configurations appear as Fail in the template view while retaining their full per-run outcomes in the history. [Week 8 master test cases](MASTER_TEST_CASES.csv) · [Execution History](../Week%207/Execution%20History.csv) · [Performance metrics](performance_metrics.csv)

## Master defect register

| Required field | Week 7 review and Week 8 treatment |
| --- | --- |
| Defect ID, Title | Present. The same canonical IDs and titles are retained. |
| Affected Feature | Week 7 kept Affected module. Week 8 adds a functional feature label and retains the module detail. |
| Environment | Week 7 used a generic evidence cross-reference for all 29 rows. Week 8 identifies the documented run context and retains source links for exact configurations. Earlier environment precision depends on the available report. |
| Preconditions | Week 7 had no dedicated column. Week 8 extracts the required setup from the historical procedure, fixture or review context. |
| Steps to Reproduce | Week 7 combined steps and defensive verification. The template copy numbers procedures and retains source review for security controls verified that way. |
| Expected Result, Actual Result | Present and retained. Observed failures and source-level findings remain distinguishable in the actual result and original lifecycle fields. |
| Severity | The brief uses Critical/Major/Moderate/Minor. Mapping is Critical → Critical, High → Major, Medium → Moderate and Low → Minor. |
| Priority | The brief uses High/Medium/Low. Mapping is P1 and P2 → High, P3 → Medium and P4 → Low. The Week 7 priority column retains the P1/P2 distinction used for release triage. |
| Evidence | Present, with original defect references and execution/requirement links retained. |
| Status | All 29 remain Open. The original lifecycle descriptor preserves confirmation and retest context. |

Owner is beyond the defect template and is required by the Week 7 exit gate for open non-blockers. The source lists no named owners or approvals. The copy marks the owner unavailable. Original affected cases, requirements, history and remediation recommendations are retained. [Week 8 master defect register](MASTER_DEFECT_REGISTER.csv)

## RTM and remaining evidence gaps

The brief requires Requirement/Feature, Test Scenario, Test Case ID(s), Test Type/Technique, Result and Defect ID. The optional Week 8 template view expands each requirement-to-design relationship to include the scenario and technique from the case repository, preserves observed outcome counts and shows unmapped requirements explicitly. Per-requirement totals can reference the same case or execution, so aggregate metrics use unique IDs. [Week 8 RTM template view](RTM_TEMPLATE_VIEW.csv) · [Week 7 requirement execution links](../Week%207/Requirement%20Execution%20Links.csv)

The original scripts and raw outputs for the Weeks 1–2 baseline reports remain unavailable. The later helper verification supplies additional Week 2 evidence. The Week 1 scope and risk matrix, decision tables, state model and completed manual test-case records provide the supplementary academic deliverables. M07 has a tester-reported completion step with only the reopened screenshot available. [Week 1 manual template and evidence](../01_Black_Box/SUPPLEMENTARY_MANUAL_TESTING.md) The archived Week 3 manual checklists retain their historical Not Run observations. Screenshots and machine artifacts exist for selected later runs. Audit-derived classifications and template mappings are Week 8 reporting judgments. [Findings and limitations](QUALITY_FINDINGS_AND_LIMITATIONS.md) · [Supplementary verification](../Week%202%20-%20White%20Box%20Testing/RECOVERED_EVIDENCE.md)
