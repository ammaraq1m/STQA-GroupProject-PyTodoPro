# Week 4 request fixtures

| Fixture | Data and use |
| --- | --- |
| Disposable accounts | API uses qa_owner and qa_peer with fresh cookies and a generated password for each pytest case. Browser cases use qa_w01 through qa_i04, as applicable, with separate cookies per case. Invalid and boundary credentials are indicated by length in evidence. |
| Categories | Work = 1, Personal = 2, Study = 3, Urgent = 4 from application initialization. |
| Tasks | Alpha planning, Alpha home, Beta planning for search and filter scenarios. Pagination uses Sample 0 through Sample 11. Browser round trips use API to UI, UI to API and API revision. |
| Dates | Fixed upcoming date 2099-04-10. Dashboard uses local run-date offsets −1, +1 and +5 days. The Web server and Chromium run in UTC. The API uses the host clock. |
| Invalid data | Missing username or title, username lengths 2 and 21, password lengths 7 and 8, numeric username or title, spaces-only title, JSON array, truncated JSON, invalid date string, string-valued done and negative per_page. |
| Concrete request and response files | [API requests, responses and checked SQLite facts](../logs/api-responses.ndjson) · [Browser and cross-layer HTTP traffic](../logs/web-results.json). |
| Redaction | Evidence retains request methods, paths, Accept and Content-Type, payloads, statuses and JSON bodies. Passwords and cookie values are excluded. API evidence records whether a session cookie is present after the response. |
