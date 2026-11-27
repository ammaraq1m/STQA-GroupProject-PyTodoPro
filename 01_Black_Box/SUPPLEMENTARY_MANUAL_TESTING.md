# Week 1 supplementary manual test cases

These cases were designed retrospectively for assessor-visible manual coverage. The historical Week 1 report contains 42 reported cases. This suite records a separate human execution. [Historical Week 1 report](Blackbox%20Testing.md) · [Test design](BLACK_BOX_TEST_DESIGN.md)

## Session record

| Field | Value |
| --- | --- |
| Tester | Human group tester. Name was not supplied with the observations. |
| Actual date and time with time zone | 27 November 2026 MYT (UTC+08:00). The tester supplied the date and time zone. Exact times were not recorded. |
| Tested Git revision | `1e11392`, as reported by the tester |
| Browser and environment | Microsoft Edge. PyTodo Pro was served on loopback port 51797 using a temporary isolated SQLite database. |
| Test data | Disposable accounts and an isolated SQLite database |

## Execution summary

The group tester reported nine human manual executions on 27 November 2026 MYT. Each linked screenshot was opened and checked. The observations record tester-supplied inputs and action sequences alongside the visible evidence.

| Planned | Executed | Pass | Fail | Blocked | Not Run | Execution rate | Pass rate |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 9 | 9 | 8 | 1 | 0 | 0 | 100.00% (9/9) | 88.89% (8/9) |

These are supplementary results. The historical Week 1 report retains 42 cases, and the project baseline retains 480 verdict records. M04 reconfirmed the existing DEF-001. [Week 7 supplementary traceability](../Week%207/Execution%20and%20Regression%20Summary.md#week-1-supplementary-manual-verification)

## Set up and capture evidence

1. In a Bash terminal at the repository root with Flask available, start a local copy of the application state. Leave the terminal open for the session.

   ```bash
   PYTODO_QA_DIR="$(mktemp -d /tmp/pytodo-week1-manual.XXXXXX)"
   python -B -c 'import os, sys; import app as m; m.DATABASE = os.path.join(sys.argv[1], "manual.sqlite3"); m.init_db(); m.app.run(host="127.0.0.1", port=51797, debug=False)' "$PYTODO_QA_DIR"
   ```

2. Open `http://127.0.0.1:51797/` in a new browser session. In Codespaces, use the Ports tab to open the forwarded port with Private visibility. Start on **Log in**, then select **Register**. Use the disposable credentials below for this session.
3. Run M01–M09 in order. For each case, record the actual visible message or task state, the verdict and the screenshot filename. Use the tester's actual date and time, including the time zone. Aim to capture the page after submission, with the message, task row, filters or address visible as appropriate.
4. Upload the screenshots or place copies in the repository under `01_Black_Box/evidence/`. Keep the listed filenames. Report unavailable screenshots explicitly. Use **Blocked** if a concrete obstacle prevented a planned case from reaching a verdict, or **Not Run** if it was skipped. If an earlier registration unexpectedly succeeds, record it and use **Log out** before starting the next registration test.

Report observations as `M01 | actual message | M01.png`. Attach each screenshot or state where it is stored. The recorded expected results provide the basis for verdicts.

## M01 — Username below minimum with a valid password

| Field | Value |
| --- | --- |
| Test case ID | W1-M01 |
| Feature/requirement | Web registration, F01 |
| Technique/test type | Equivalence Partitioning, Boundary Value Analysis, Decision Table R2 |
| Objective | Reject a two-character username when the password is valid. |
| Preconditions | Fresh anonymous session, Register page open. |
| Test data | Username `ab` and password `PhaseQA9x` (9 characters). |
| Expected result | The Register page remains open and displays “Username must be 3-20 characters (letters, numbers, underscore).” |
| Actual result | The form rejected the two-character username and displayed “Username must be 3-20 characters (letters, numbers, underscore).” |
| Status | Pass |
| Evidence | [Username validation](evidence/Invalid%20username.png) |
| Defect ID | N/A at design time |

1. Enter the username and password in the Register form.
2. Select **Register** and inspect the heading and validation message.

## M02 — Password below minimum with a valid username

| Field | Value |
| --- | --- |
| Test case ID | W1-M02 |
| Feature/requirement | Web registration, F02 |
| Technique/test type | Equivalence Partitioning, Boundary Value Analysis, Decision Table R3 |
| Objective | Reject a seven-character password when the username is valid. |
| Preconditions | Anonymous, Register page open, `p01` unused. |
| Test data | Username `p01` and password `PhaseQ7` (7 characters). |
| Expected result | The Register page remains open and displays “Password must be at least 8 characters.” |
| Actual result | The form rejected the seven-character password and displayed “Password must be at least 8 characters.” |
| Status | Pass |
| Evidence | [Password validation](evidence/Invalid%20password.png) |
| Defect ID | N/A at design time |

1. Enter the provided username and password.
2. Select **Register** and inspect the heading and validation message.

## M03 — Both registration inputs are invalid

| Field | Value |
| --- | --- |
| Test case ID | W1-M03 |
| Feature/requirement | Web registration, F01 and F02 |
| Technique/test type | Equivalence Partitioning and Decision Table R4 |
| Objective | Check rejection and the web form's first reported error when both inputs are invalid. |
| Preconditions | Anonymous, Register page open. |
| Test data | Username `ab` and password `PhaseQ7` (7 characters). |
| Expected result | The Register page remains open and presents the username validation message first. The first-error expectation follows the validation order reviewed on this build. |
| Actual result | The form rejected both invalid inputs and displayed the username validation message first. |
| Status | Pass |
| Evidence | [First validation error](evidence/Both%20inputs%20invalid.png) |
| Defect ID | N/A at design time |

1. Enter both non-empty invalid inputs.
2. Select **Register** and note the message that appears first.

## M04 — Password exactly at the advertised minimum

| Field | Value |
| --- | --- |
| Test case ID | W1-M04 |
| Feature/requirement | Web registration, F01, F02 and F03 |
| Technique/test type | Boundary Value Analysis and Decision Table R1 |
| Objective | Check the advertised inclusive minimum of eight password characters on the web form. |
| Preconditions | Anonymous, Register page open, `p08` unused. |
| Test data | Username `p08` (3 characters) and password `PhaseQA8` (8 characters). |
| Expected result | Account creation succeeds and **My Tasks** opens in the new session. |
| Actual result | The form rejected the eight-character password and displayed “Password must be at least 8 characters.” My Tasks did not open. |
| Status | Fail |
| Evidence | [Eight-character password rejected](evidence/Eight-character%20password%20rejected.png) |
| Defect ID | DEF-001, existing defect reconfirmed. [Master defect register](../Week%208/MASTER_DEFECT_REGISTER.csv) |

1. Enter and submit the provided credentials.
2. Record whether My Tasks opened or the form presented an error. Record the observed message if shown.

## M05 — Password one character above the minimum

| Field | Value |
| --- | --- |
| Test case ID | W1-M05 |
| Feature/requirement | Web registration, F01, F02 and F03 |
| Technique/test type | Equivalence Partitioning, Boundary Value Analysis, Decision Table R1 |
| Objective | Provide a valid control with a three-character username and a nine-character password. |
| Preconditions | Anonymous, Register page open, `p09` unused. |
| Test data | Username `p09` (3 characters) and password `PhaseQA9x` (9 characters). |
| Expected result | Account creation succeeds and **My Tasks** opens, with the new account signed in. |
| Actual result | The nine-character password was accepted. My Tasks opened and showed account p09. |
| Status | Pass |
| Evidence | [My Tasks after registration](evidence/Registration%20successful.png) |
| Defect ID | N/A at design time |

1. Enter and submit the provided credentials.
2. Confirm **My Tasks** appears. Stay signed in as `p09` for the task cases.

## M06 — Title and status with the category filter cleared

| Field | Value |
| --- | --- |
| Test case ID | W1-M06 |
| Feature/requirement | My Tasks combined filtering, F16 |
| Technique/test type | Decision Table T7 |
| Objective | Check that title and status conditions both apply with All categories selected. |
| Preconditions | Signed in as `p09`. Clear filters and use only the disposable tasks below. |
| Test data | `Phase Alpha Review` (Work, Done), `Phase Alpha Draft` (Personal, Open), `Phase Beta Review` (Personal, Done). All descriptions and dates blank. Search `Alpha` with status Done. |
| Expected result | With All categories, Done and search `Alpha` active, only `Phase Alpha Review` appears. The draft fails the status condition and the beta review fails the title condition. |
| Actual result | With All categories and Done selected, only Phase Alpha Review appeared. The displayed search value was lowercase `alpha`. |
| Status | Pass |
| Evidence | [Filtered result showing lowercase alpha](evidence/Task%20completed.png). [Unfiltered capture](evidence/Combined%20filter%20result.png) shows all three tasks marked Done in an unfiltered view. It does not establish the draft’s status at the filtered checkpoint. |
| Defect ID | N/A at design time |

1. Create each task using **+ New Task**, the exact title and the selected category. Leave Description and Due Date blank.
2. Click the circle in the rows for `Phase Alpha Review` and `Phase Beta Review` to mark them Done. Leave the draft Open.
3. On My Tasks, set category to **All categories**, enter `Alpha` in **Search title**, select **Filter**, then select **Done** in the status dropdown.
4. Check the settings and list. Use **Tasks** in the navigation to reset filters before the next case.

## M07 — Create, complete and reopen a task

| Field | Value |
| --- | --- |
| Test case ID | W1-M07 |
| Feature/requirement | Task creation and completion, F08 and F14 |
| Technique/test type | State Transition, S1–S3 |
| Objective | Verify the valid sequence from absent to open, completed and reopened. |
| Preconditions | Signed in as `p09`, filters cleared, `Phase Lifecycle` absent. |
| Test data | Title `Phase Lifecycle`, category Study, Description and Due Date blank. |
| Expected result | The new row is Open. The first toggle shows a checkmark and Done badge. The second returns the same task to Open, with a circle control and inclusion in the Open filter. |
| Actual result | The tester observed Phase Lifecycle become Done and then reopen. The Open filter showed the task with the circle control after reopening. |
| Status | Pass |
| Evidence | [Reopened task under Open filter](evidence/Task%20reopened.png). The planned screenshot of Phase Lifecycle showing its Done badge is unavailable. The completion step is supported by the tester’s observation. |
| Defect ID | N/A at design time |

1. Create the task. Check that the circular completion control appears.
2. Click the circle. Confirm the checkmark and Done badge, then capture M07a.
3. Click the checkmark. Select **Open** from the status filter. Confirm the task row appears with the circle again and capture M07b.

## M08 — Cancel deletion and then confirm it

| Field | Value |
| --- | --- |
| Test case ID | W1-M08 |
| Feature/requirement | Owned-task deletion and confirmation, F15 |
| Technique/test type | State Transition, S5 and S6 |
| Objective | Verify that cancelling preserves the task and confirming removes it. |
| Preconditions | Signed in as `p09`, `Phase Lifecycle` exists, filters cleared through the **Tasks** navigation link. |
| Test data | The existing owned `Phase Lifecycle` row and its Edit URL. |
| Expected result | The row remains after Cancel. After Delete is confirmed, the row is absent from My Tasks after a refresh. |
| Actual result | Cancelling preserved Phase Lifecycle. The tester confirmed Delete and the task was absent after refreshing My Tasks. |
| Status | Pass |
| Evidence | [Task retained after Cancel](evidence/Cancel%20deletion.png) · [Task absent after confirmed deletion](evidence/Confirm%20deletion.png) |
| Defect ID | N/A at design time |

1. Open **Edit** on the `Phase Lifecycle` row, copy the address for M09 and return using **Tasks** in the navigation.
2. Click **Delete** for that row and select **Cancel** in the browser dialog. Verify it remains and capture M08a.
3. Click **Delete** again and accept the dialog. Refresh My Tasks, check that the row is absent and capture M08b.

## M09 — Attempt to edit an already deleted task

| Field | Value |
| --- | --- |
| Test case ID | W1-M09 |
| Feature/requirement | Web task editing, F08. F23 is related API evidence. |
| Technique/test type | State Transition, S7 |
| Objective | Check the web UI's handling of an edit request for the tester's deleted task. |
| Preconditions | Signed in as `p09`, the M08 target is deleted, and its former Edit URL is saved. |
| Test data | The actual Edit URL copied in M08. |
| Expected result | The browser returns to **My Tasks** and the deleted task remains absent. |
| Actual result | The tester opened the saved Edit URL and was returned to My Tasks. Phase Lifecycle remained absent. |
| Status | Pass |
| Evidence | [Final My Tasks page and address bar](evidence/Old%20Edit%20URL%20result.png) |
| Defect ID | N/A at design time |

1. Paste the copied URL into a new tab in the same signed-in browser session and press Enter.
2. Record the final page or error. Check whether `Phase Lifecycle` is present on My Tasks.
