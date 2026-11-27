# PyTodo Pro · Week 6 automation candidates

| Selection criterion | How it was applied |
| --- | --- |
| Repetition | Prefer checks that should run on every change to the application or its dependencies. |
| Stability | Prefer deterministic response, persisted-state and semantic UI checks. Fix time at exact boundaries. |
| Criticality | Prioritize sign-in, private task access, writes and task state integrity. |
| Regression value | Keep cases that distinguish a known defect from its documented expected behaviour, including representative passing controls. |

| Original IDs | Source | Scenario | Criteria | Priority | Suitability and justification |
| --- | --- | --- | --- | --- | --- |
| G01–G03, G11; W01–W03; A01, A09, A10, A12 | Weeks 3 and 4 | Registration, login, logout and access gates | Repetition, criticality, stability | High | High. Repeat through Chromium and Flask test client with explicit session and navigation assertions. Reuse Week 4 cases. |
| TC10, TC28, TC32; P03; G14; W07; A07, A08 | Weeks 1–4 | Minimum password and duplicate registration | Regression value, stability, criticality | High | High. Boundary and duplicate outcomes are objective. Reuse the browser and API tests. |
| G04–G06, G10; W04; A13, A20 | Weeks 3 and 4 | Task CRUD, completion, reopen and cancellation | Criticality, repetition | High | High. Assert rendered state and SQLite changes using existing scripts. |
| TC35, TC42; G15–G17; W03, W08; I03; A15, A16, A18, A21–A23 | Weeks 1, 3 and 4 | Required/type validation and atomicity | Regression value, stability, criticality | High | High. Reuse observed regressions. Add GAP05 to verify that update preserves a valid due date after rejection. |
| TC36–TC38; G07, G08; W05; A26–A28 | Weeks 1, 3 and 4 | Pagination, ordinary title search and combined filters | Repetition, stability, regression value | High | High. Ordered fixture titles and result counts have exact comparisons. |
| TC16, TC24, TC26; U03, C03, C06; G09, G18; W06; A29, A30 | Weeks 1–4 | Dashboard counters, due-today and completion window boundaries | Regression value, stability | High | High. Reuse valid aggregate and due-today tests. GAP01–GAP04 add fixed-clock checks through both dashboard routes. |
| I01–I04 | Week 4 | Browser/API shared task state and session | Criticality, regression value | High | High. Reuse Playwright and its shared request context. |
| A33; S04–S06, S15–S17, S19 | Weeks 4 and 5 | Ownership, credential handling and defensive configuration checks | Criticality, regression value | High | High for API and fixture checks. Source checks are useful for this revision and should be reviewed when handlers change. GAP06 covers the separate web edit route. |
| GUI-01–GUI-10 | Week 3 checklist stored under Week 2 | Manual GUI scenarios with objective outcomes | Repeatability, stability | High | High for automation mapping. The source checklist rows are marked Not run. Week 6 runs the mapped automated equivalents. |
| GUI-11, GUI-12; C-M01–C-M03, U-M01–U-M02, A-M01–A-M03 | Historical checklist and Week 3 | Visual clarity, physical-device behaviour, participant evaluation and manual accessibility | Depends on human or hardware evidence | Medium | Excluded from the focused run. Automated evidence cannot establish participant understanding, native device behaviour or what assistive technology announces. |
| A31, A32; N01–N04 | Weeks 4 and 5 | Adversarial runtime, executable content, HTTPS deployment | Criticality, environment and scope | High | Runtime coverage deferred. Reuse defensive source checks and ordinary functional ownership/search. Preserve individual Not Run entries. |
| C01–C02 and axe states; Locust stages | Weeks 3 and 5 | Viewport fit, automated accessibility and performance | Regression value, environment dependence | Medium | Existing tools and evidence remain available. Run separately when layout, accessibility or performance is the focus. Short load measurements vary with host activity. |

The [manifest](tests/manifest.json) lists each chosen executable case independently. Closely related historical IDs above describe coverage lineage. They do not add execution counts.
