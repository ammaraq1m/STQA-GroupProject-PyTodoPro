# Week 6 regression test data

| Scope | Data and isolation |
| --- | --- |
| Reused API and security | Fresh SQLite database per pytest case. Reuse the [Week 4 fixtures](../../Week%204%20-%20Web%20and%20API%20Testing/test-data/FIXTURES.md) and [Week 5 fixtures](../../Week%205%20-%20Security%20and%20Performance%20Testing/test-data/SECURITY_FIXTURES.md). |
| Browser | Fresh temporary Flask database per suite run. Each case uses its own browser context and unique fixture account. Reuse the Week 4 Chromium cases, task data and generated credentials. |
| Completion boundary | Set the helper clock to 2026-02-15 12:00:00. Seed one completed task at age zero, exactly seven days, seven days and one second, or one second in the future. Each parameter has its own fixture database. |
| Date update integrity | Create a task due 2099-04-10. Submit an invalid date string to its API update. Check the HTTP response, SQLite value and subsequent owner read. |
| Web ownership | Two disposable clients and one task. Verify the peer cannot open the edit form or change the title through its form POST. |
| Redaction | Runner preserves earlier fixture redaction. Passwords, cookies, hashes and signing keys are not included in execution evidence. |
