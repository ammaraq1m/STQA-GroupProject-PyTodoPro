# PyTodo Pro · Speaking script

Assign names to presenter roles A–D and rehearse slide 11 with the evidence tabs already open. Times are approximate. [Slide content](PRESENTATION_CONTENT.md) · [Demo commands](LIVE_DEMONSTRATION.md)

### Slide 1 · Presenter A · 40 seconds

“PyTodo Pro is a Flask and SQLite task manager with a browser interface and a JSON API. We evaluated registration, task management and dashboard reporting as one user journey. It works on several sampled happy paths. We recommend withholding approval for a multi-user deployment because important isolation, integrity and accessibility findings remain open.”

### Slide 2 · Presenter A · 45 seconds

“Our main question was whether users can manage their own tasks, receive correct results and recover from invalid input. We exercised disposable accounts, local SQLite, browser contexts and a controlled read workload. Physical devices, participant use, native assistive technology and deployed settings remain gaps.”

### Slide 3 · Presenter A · 65 seconds

“Week 1 used equivalence partitions and boundaries, recording 32 passes out of 42. Week 2 followed helper control flow. It reported every measured statement and branch in scope, yet four tests failed. For example, today was labelled Overdue. Week 3 separated interactions from presentation: the 88 emulated core GUI checks passed, while only two of 16 emulated layout checks passed. The screenshot shows the kind of layout problem a successful task action can miss.”

### Slide 4 · Presenter B · 55 seconds

“Week 4 tested web and API contracts and state shared across both interfaces. Twenty-nine checks passed and 14 failed. Week 5 used STRIDE, defensive checks and paced load. Week 6 combined selected earlier tests with new integration checks. Its recovered run retained 20 product failures and 12 deferrals. Matching earlier verdicts shows repeatability in the selected suite.”

### Slide 5 · Presenter B · 55 seconds

“Follow F19 in the RTM. GAP02 checks whether a task completed exactly seven days earlier appears in the dashboard total. The expected count was one, and both interfaces returned zero. The defect register tracks this as DEF-003. Thirty-nine of 44 requirements have a mapped case, and 35 have a recorded verdict or measurement. A mapped requirement can still contain untested scenarios.”

### Slide 6 · Presenter B · 55 seconds

“We planned 480 verdict records in the baseline and final view. Of 421 executed, 325 passed and 96 failed. That is an execution rate of 87.71% and a pass rate of 77.20% among executed records. Fifty-nine are Not Run. The 225 unique designs include four performance measurement designs. Repeated configurations and reruns account for the difference in denominators. The initial Week 6 attempt had 16 blocks and is archived independently.”

### Slide 7 · Presenter C · 60 seconds

“The consolidated register contains 29 open defects, including one Critical and nine Major. Invalid dates can be written before an error is returned, and later reads of the affected task can fail. On the UI, missing form labels and completion control names make core actions harder to identify. Narrow layouts and larger text can move controls out of view.”

### Slide 8 · Presenter C · 55 seconds

“Sampled password hashing and owner-read checks passed. Open findings include unsafe query construction, missing owner scope for deletion and a literal signing configuration. These are verified at the level documented in the reports. At 25 paced users, the pinned local workload returned aggregate P95 of 120 milliseconds. Both runs had zero failures among 2,460 timed read requests. Deployment traffic and write contention are still uncharacterised.”

### Slide 9 · Presenter C · 50 seconds

“We use the ISO/IEC 25010:2023 product model for this mapping. The course brief does not specify an edition. Functional suitability was directly evaluated. Six characteristics have partial evidence, including security and interaction capability. Maintainability evidence is indirect, and no safety assessment was performed. These judgements describe evidence depth.”

### Slide 10 · Presenter D · 60 seconds

“ISO quality management principles help explain the value of documented evidence and decision ownership. Relevant CMMI practice areas include requirements management, verification, process quality assurance and causal analysis. Our proposal runs focused smoke tests on changes and full regression at scheduled and candidate checkpoints. Failed tests stay visible, alongside setup errors and deferrals. Each failure needs a tracked decision and evidence before closure.”

### Slide 11 · Presenter D · 4 minutes

“Here is a disposable account. I create a task, complete it and view its dashboard count. Now the test client runs A01 and GAP02. The registration control passes. With a frozen clock, the inclusive seven-day case fails as expected for this baseline. Both dashboards return zero where the requirement expects one. Here is the F19 RTM row and DEF-003 evidence. The full helper coverage and the failing assertion can coexist.” Follow the runbook. If setup fails, state what stopped and switch to archived evidence.

### Slide 12 · Presenter D · 60 seconds

“We would first correct ownership, query construction, signing and failed-write integrity. Next we would confirm fixes, complete native accessibility and device checks, and verify representative deployment conditions. Four exit gates are unmet and the fifth requires a named review. We can demonstrate the application and our evaluation. The release decision remains on hold until the evidence supports approval.”
