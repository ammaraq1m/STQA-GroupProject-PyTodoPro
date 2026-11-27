# Week 5 local performance workload

| Parameter | Prespecified value |
| --- | --- |
| Target | Original Flask app, one threaded development server bound to 127.0.0.1:51795 with debug/reloader disabled. The report baseline uses the project Flask 3.0.3 pin. |
| Fixture | 25 disposable accounts, 60 tasks per account and four original categories. Every fourth task is completed, for 15 completed tasks per account. Dates rotate among overdue, tomorrow, upcoming and unset. |
| Web reads | GET / is the primary task list. GET /dashboard is the summary navigation destination. |
| API reads | GET /api/tasks?page=0&per_page=10 is the default-sized list. GET /api/dashboard reads summary counters. |
| Traffic mix | One request per user per second at most. Users cycle evenly through the four reads, with different initial offsets. Requests time out after three seconds. |
| Authentication | Each simulated user logs in once per workload with a unique fixture account using the real API login route. Exclude login and warmup from reported performance. |
| Workloads | Stages of 1, 5, 10 and 25 concurrent users. Spawn at up to two users per second, verify all sessions, settle for three seconds, reset Locust statistics, then measure for 60 seconds per stage. |
| Progression | Use a fresh Locust runner and sessions per stage. Advance only when the previous stage completes within the stop criteria. |
| Stop thresholds | Stop immediately if Flask exits, host available memory drops below 512 MiB, or combined Flask and generator RSS exceeds 1 GiB at a five-second sample. Stop after three consecutive five-second samples above 95% host CPU or with more than 15% failed requests in each interval of at least 20 requests. Stop if the stage cannot authenticate all users within 30 seconds. |
| Success checks | Each measured response must be HTTP 200 and contain the expected page heading or valid JSON structure/counts. A stage may complete with errors below the safety threshold. |
| Scope | Read-only measured traffic on loopback. Login, writes, external systems, and production capacity are outside the timed workload. |
