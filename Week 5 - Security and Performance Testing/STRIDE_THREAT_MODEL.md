# PyTodo Pro · Week 5 STRIDE threat model

| Boundary | Crossing and assets | Security expectation |
| --- | --- | --- |
| B1 | Browser/API client → Flask routes. Credentials, cookie, form values and JSON enter the app. | Authenticate users, validate inputs, return minimal errors and protect sessions. |
| B2 | Flask request/session → SQLite. User ID and task identifier govern task and dashboard access. | Scope each read and write to the authenticated owner and preserve validated state. |
| B3 | SQLite → Flask serializers/templates → client. Task state and user data are rendered or returned as JSON. | Expose only permitted data and escape untrusted content at the rendering boundary. |
| B4 | Runtime configuration → application. Session key, cookie policy and deployment settings. | Use managed secrets, secure transport and hardened cookie defaults for HTTPS deployment. |
| B5 | Application actions and errors → operational records. Actor, resource, timestamp and outcome. | Log security-relevant events without passwords, cookie values or unnecessary task content. |

Risks are qualitative. High denotes a plausible loss of private task data, account integrity or service availability with material impact. Moderate denotes a narrower exposure or a gap in defence or accountability.

| Threat | STRIDE | Boundary / asset | Threat and potential impact | Risk | Mitigation | Safe case mapping |
| --- | --- | --- | --- | --- | --- | --- |
| T01 | Spoofing | B1, B4 · identity and session | Inadequate credential checks or weak session configuration could allow impersonation. | High | Retain generic login errors, load and rotate a deployment-specific signing key, and configure Secure, HttpOnly and explicit SameSite policy over HTTPS. | S01, S03–S06, S17. Key review checks configuration only. |
| T02 | Tampering | B1, B2 · tasks and database | Unvalidated types or unsafe query construction can alter expected behaviour or undermine database integrity. | High | Validate object and field types, normalize titles, bind values in queries and validate before commit. | S11, S12, S14, S15. Query construction reviewed without adversarial requests. |
| T03 | Tampering | B1 · web mutation forms | Missing form-level protections can allow an unwanted state change in an authenticated browser. | High | Require a server-validated anti-CSRF control for mutations and make logout POST-only. | S19, source inspection only. |
| T04 | Repudiation | B5 · audit trail | A deleted or changed task lacks a persistent event tying an actor to the action, reducing investigation and recovery options. | Moderate | Record actor ID, resource ID, action, time and result in restricted audit storage. | S18, own-task delete and local schema review. |
| T05 | Information disclosure | B2, B3 · tasks and credentials | Broad queries or verbose responses could expose another account's data, hashes or diagnostics. | High | Owner-scope reads, minimize response fields, and keep production error pages generic with debug disabled. | S02, S07, S08, S10, S13. |
| T06 | Denial of service | B1, B2 · request handling | Unbounded result sizes and per-request processing errors can increase database and server work. | Moderate | Validate pagination and cap page size, reject bad data early, and monitor request volume and failures. | S12, S20 with 12 rows. Performance stages use valid bounded reads. |
| T07 | Elevation of privilege | B2 · task ownership | If access checks differ by method, an authenticated user may gain control of a task outside their ownership. | High | Centralize owner authorization and apply it to all task mutations, including deletion. | S02, S08, S09, S16. Delete authorization reviewed in source. |
| T08 | Information disclosure | B3 · rendered task title | An escaping override for user-authored titles increases the risk that data is treated as markup. | Moderate | Restore template autoescaping for titles and add a benign output-encoding test. | N03, runtime verification Not Run. Source review identified the title-rendering override. |
