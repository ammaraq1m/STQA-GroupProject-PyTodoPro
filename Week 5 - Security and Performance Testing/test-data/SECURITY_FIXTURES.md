# Week 5 security fixtures

| Fixture | Data | Evidence policy |
| --- | --- | --- |
| Database | One Flask-initialized SQLite file per security case. Four default categories are seeded by the original app. Files are removed during fixture teardown. | Store selected SQLite facts and schema observations. |
| Accounts | Disposable qa_owner and qa_peer; qa_unknown remains unregistered. Generate a password at runtime. Use the same generated password for two users in the salt check. | Record comparison booleans only. No passwords or password hashes are written to test evidence. |
| Session | Separate Flask test clients represent anonymous, owner and peer sessions. | Store cookie presence and flags. Omit cookie values and the application signing key. |
| Records | Owner fixture, Peer fixture, Invoice planning, Errands and Sample 0 through Sample 11. All are synthetic test tasks. | Store selected returned titles and whether the storage changes match expectations. |
| Input examples | A whitespace-only title, a numeric title, an ordinary Invoice substring and a negative page size against 12 rows. | Record response status, content type and assertion results. |
| Source checks | API search binding, deletion authorization, session-key configuration, task mutation form controls and logout method. | Record the control property observed. No destructive cross-owner request, adversarial search input, forged cookie or cross-site submission is sent. |
