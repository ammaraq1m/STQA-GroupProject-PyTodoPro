# PyTodo Pro · Week 6 automation reflection

| Topic | Observation |
| --- | --- |
| Repeatability | Per-case SQLite files, disposable browser contexts, generated credentials and a frozen helper clock keep cases independent. Those controls let the suite reproduce the exact completion boundaries through both dashboard routes. |
| Efficiency | One runner selects pytest cases and executes Playwright, exports results and captures screenshots. Its measured wall time includes staging and cleanup. A comparable timed manual run was unavailable, so the evidence supports an automated duration only. |
| Consistency | Reusing earlier case bodies preserves test oracles and enables matched-ID comparisons. API errors, browser validation and persisted state retain their own assertions. Missing fixtures or startup problems are visible as infrastructure outcomes. |
| Regression detection | Positive controls show the routes still operate with valid data. Exact business boundary failures remain visible because assertions follow the stated behaviour. Known failures still return a failing suite status. |
| Reuse maintenance | The runner stages earlier files in a disposable tree and verifies the two Playwright timing anchors. A future hook for an output directory and case timings would let the browser suite be imported directly. Source-based security checks need review when authorization or configuration moves. |
| Environment | The browser suite needs Chromium libraries, a free loopback port and Node. Pytest needs the pinned Flask dependencies. Clock injection removes boundary drift from the new checks. The browser dashboard still uses a real clock within its own fixture process. |
| Human judgement | Keep physical device, screen reader, native zoom, visual contrast and participant evaluations separate. Repeated browser assertions validate observable interactions and cannot establish human comprehension. |
| Future regression work | Run lightweight API and helper checks on each change. Run the Chromium suite in CI with pinned dependencies and publish JUnit, JSON and screenshots. Schedule compatibility and performance separately. Review persistent defect IDs after fixes and rerun the matching cases before closure. |
