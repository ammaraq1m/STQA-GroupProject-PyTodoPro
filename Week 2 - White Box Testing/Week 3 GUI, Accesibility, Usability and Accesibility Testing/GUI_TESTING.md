# PyTodo Pro: GUI Testing

## Objective

Verify interface functionality and visual consistency.

## Test environment

| Item | Details |
|---|---|
| Application | PyTodo Pro |
| Application URL / commit | |
| Tester | |
| Date | |
| Browser and version | |
| Operating system and version | |
| Device / viewport | |
| Tool / BrowserStack session URL | |

## Test checklist

| Test ID | Page / criteria | Test action | Expected result | Actual result | Status | Evidence / defect ID |
| --- | --- | --- | --- | --- | --- | --- |
| GUI-01 | Login form | Enter valid credentials and submit | Task list opens |  | Not run |  |
| GUI-02 | Login form | Submit invalid credentials | Understandable error is displayed |  | Not run |  |
| GUI-03 | Registration | Submit invalid username or password | Validation message is displayed |  | Not run |  |
| GUI-04 | Task creation | Enter valid task details and save | Task appears in list |  | Not run |  |
| GUI-05 | Task creation | Submit an empty title | Required-field validation prevents invalid task |  | Not run |  |
| GUI-06 | Task editing | Change a task title and save | Updated title is displayed |  | Not run |  |
| GUI-07 | Task completion | Toggle a task twice | Completion status updates each time |  | Not run |  |
| GUI-08 | Task deletion | Delete a test task | Selected task is removed |  | Not run |  |
| GUI-09 | Navigation | Open dashboard and return to task list | Links open correct pages |  | Not run |  |
| GUI-10 | Logout | Select logout | Login page opens |  | Not run |  |
| GUI-11 | Labels | Inspect form labels and controls | Labels are clear and accurate |  | Not run |  |
| GUI-12 | Visual consistency | Compare all main pages | Fonts, spacing and controls are consistent |  | Not run |  |

## Evidence

Save screenshots in `screenshots/gui/`. Link them using `[Screenshot](screenshots/gui/GUI-01.png)` once captured.

## Summary

| Item | Count / details |
|---|---|
| Passed | |
| Failed | |
| Blocked / not applicable | |
| Not run | |
| Key findings | |

Record actual results only after execution. Link defects to `DEFECT_REPORT.md`.
