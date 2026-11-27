# PyTodo Pro · Week 5 security and performance test report

| Item | Detail |
| --- | --- |
| Revision | 4c11244 · execution 27 November 2026 UTC |
| Review basis | [Group Project brief](../Group%20Project.pdf) · [Week 1](../01_Black_Box/Blackbox%20Testing.md) · [Week 2](../Week%202%20-%20White%20Box%20Testing/White-Box-Testing.md) · [Week 3](../Week%203%20-%20GUI%20Compatibility%20Usability%20Accessibility%20Testing/WEEK_3_TEST_REPORT.md) · [Week 4](../Week%204%20-%20Web%20and%20API%20Testing/WEEK_4_TEST_REPORT.md) · application routes, templates and helpers |
| Security | 24 cases including 20 executed via Flask test client or defensive inspection. 12 passed, 8 failed and 4 were Not Run. |
| Defects | 4 newly documented findings and 4 prior findings reconfirmed. Two known weaknesses were reconfirmed through code inspection. |
| Performance | 4 of 4 timed stages completed on the project-pinned Flask version. 2,460 timed requests, 0 failures. At 25 users, 24.999 req/s and 120 ms aggregate P95. |
| Isolation | One temporary SQLite database per security case and a separate 1,500-task temporary database for the localhost load experiment. No credentials or session values are recorded. |

## Deliverables

| Area | Result and evidence |
| --- | --- |
| Threat model | [STRIDE threats and test mappings](STRIDE_THREAT_MODEL.md) |
| Security | [Case results](SECURITY_TESTING.md) · [pytest output](logs/security-execution.log) · [request evidence](logs/security-evidence.ndjson) |
| Performance | [Experiment, results and charts](PERFORMANCE_TESTING.md) · [workload definition](test-data/WORKLOAD.md) · [raw CSV](results/performance.csv) |
| Defects | [New findings and prior defect cross-references](DEFECT_REPORT.md) |

Prioritize owner-scoping API deletion, binding API search inputs and replacing the literal session signing key. Then address CSRF protection, cookie configuration, validation and durable audit events. The load run establishes a local read baseline under a paced workload. A production-like capacity estimate requires longer runs, a separate load generator and more representative traffic.

## Reproduce

From the repository root, use a Python environment with the Week 5 dependency pins. Port 51795 must be free. Evidence files are overwritten by a rerun.

```bash
cd "Week 5 - Security and Performance Testing"
python -m pip install -r requirements.txt
python -B -m pytest -p no:cacheprovider --tb=short -v --junitxml=logs/security-junit.xml tests/test_security.py > logs/security-execution.log 2>&1
python -B performance/run.py > logs/locust.log 2>&1
python -B performance/plot.py
```

Pytest returns nonzero for failed assertions. The Locust driver exits nonzero if any planned stage does not complete.
