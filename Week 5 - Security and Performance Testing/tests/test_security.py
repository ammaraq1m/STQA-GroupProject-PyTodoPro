"""Defensive behavioural checks and source review. No attack payloads or live targets."""
import ast
import json
from pathlib import Path
import secrets
import sqlite3
import sys

import pytest
from werkzeug.security import check_password_hash

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent))
import app as target


@pytest.fixture(scope="session", autouse=True)
def reset_evidence():
    (ROOT / "logs" / "security-evidence.ndjson").write_text("")


class Check:
    def __init__(self, database):
        self.db = database
        self.requests = []
        self.checks = []
        self.secret = secrets.token_urlsafe(20)

    def request(self, client, method, url, **kwargs):
        response = client.open(url, method=method, **kwargs)
        self.requests.append({"method": method, "path": url, "status": response.status_code,
                              "content_type": response.mimetype})
        return response

    def user(self, name="qa_owner"):
        client = target.app.test_client()
        r = self.request(client, "POST", "/api/register",
                         json={"username": name, "password": self.secret})
        assert r.status_code == 201, "Fixture registration failed"
        return client, r.json["id"]

    def task(self, client, name="Defensive review fixture"):
        r = self.request(client, "POST", "/api/tasks", json={"title": name})
        assert r.status_code == 201, "Fixture create failed"
        return r.json["id"]

    def rows(self, sql):
        with sqlite3.connect(self.db) as conn:
            return conn.execute(sql).fetchall()

    def expect(self, name, actual, expected):
        self.checks.append({"assertion": name, "actual": actual, "expected": expected})

    def verify(self):
        mismatches = [a for a in self.checks if a["actual"] != a["expected"]]
        assert not mismatches, json.dumps(mismatches)


@pytest.fixture
def check(tmp_path, monkeypatch, request):
    db = tmp_path / "security.sqlite3"
    monkeypatch.setattr(target, "DATABASE", str(db))
    monkeypatch.setitem(target.app.config, "TESTING", True)
    monkeypatch.setitem(target.app.config, "PROPAGATE_EXCEPTIONS", False)
    target.init_db()
    item = Check(db)
    yield item
    evidence = ROOT / "logs" / "security-evidence.ndjson"
    with evidence.open("a") as out:
        out.write(json.dumps({"test": request.node.name, "requests": item.requests,
                              "assertions": item.checks})+"\n")
    db.unlink()


def source_function(name):
    tree = ast.parse((ROOT.parent / "app.py").read_text())
    return next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name)


def test_S01_invalid_login_generic(check):
    check.user()
    client = target.app.test_client()
    for user in ("qa_owner", "qa_unknown"):
        r = check.request(client, "POST", "/api/login",
                          json={"username": user, "password": secrets.token_urlsafe(12)})
        check.expect("generic failure", [r.status_code, r.json, client.get_cookie("session") is None],
                     [401, {"error":"invalid credentials"}, True])
    check.verify()


def test_S02_protected_routes(check):
    client = target.app.test_client()
    for method, path in [("GET","/api/tasks"),("POST","/api/tasks"),("GET","/api/tasks/1"),
                         ("PUT","/api/tasks/1"),("DELETE","/api/tasks/1"),("GET","/api/dashboard")]:
        r = check.request(client,method,path)
        check.expect("signed-out API denial", [r.status_code,r.json], [401,{"error":"authentication required"}])
    r = check.request(client,"GET","/dashboard")
    check.expect("signed-out web redirect",[r.status_code,r.location],[302,"/login"])
    check.verify()


def test_S03_login_logout_cookie(check):
    check.user()
    client = target.app.test_client()
    r = check.request(client,"POST","/api/login",json={"username":"qa_owner","password":check.secret})
    check.expect("session established",[r.status_code,client.get_cookie("session") is not None],[200,True])
    r = check.request(client,"GET","/logout")
    check.expect("session cleared",[r.status_code,client.get_cookie("session") is None],[302,True])
    check.expect("protected API denies logged-out client",check.request(client,"GET","/api/tasks").status_code,401)
    check.verify()


def test_S04_password_hashes(check):
    check.user()
    check.user("qa_peer")
    hashes = [row[0] for row in check.rows("SELECT password_hash FROM users")]
    check.expect("two distinct salted hashes verify and differ from plaintext",
                 len(set(hashes)) == 2 and all(value != check.secret and check_password_hash(value,check.secret)
                                               for value in hashes), True)
    check.verify()


def test_S05_cookie_httponly(check):
    client,_ = check.user()
    check.expect("session cookie HttpOnly",client.get_cookie("session").http_only,True)
    check.verify()


def test_S06_cookie_deployment_flags(check):
    client,_ = check.user()
    cookie = client.get_cookie("session")
    check.expect("Secure flag",cookie.secure,True)
    check.expect("explicit SameSite policy",cookie.same_site in ("Lax","Strict"),True)
    check.verify()


def test_S07_owner_scoped_reads(check):
    owner,_ = check.user()
    peer,_ = check.user("qa_peer")
    check.task(owner,"Owner fixture")
    check.task(peer,"Peer fixture")
    for client,title in [(owner,"Owner fixture"),(peer,"Peer fixture")]:
        listing = check.request(client,"GET","/api/tasks")
        summary = check.request(client,"GET","/api/dashboard")
        check.expect("account list", [listing.status_code,[t["title"] for t in listing.json]],[200,[title]])
        check.expect("account dashboard", [summary.status_code, summary.json["total"]],[200,1])
    check.verify()


def test_S08_peer_read_update_denied(check):
    owner,uid = check.user()
    peer,_ = check.user("qa_peer")
    task_id = check.task(owner,"Owner fixture")
    route = f"/api/tasks/{task_id}"
    for method, payload in [("GET",{}),("PUT",{"json":{"title":"Changed fixture"}})]:
        r = check.request(peer,method,route,**payload)
        check.expect("peer access denied",[r.status_code,r.json],[404,{"error":"not found"}])
    check.expect("original owner and title retained", check.rows("SELECT user_id,title FROM tasks"),[(uid,"Owner fixture")])
    check.verify()


def test_S09_owner_delete(check):
    owner,_ = check.user()
    task_id = check.task(owner)
    r = check.request(owner,"DELETE",f"/api/tasks/{task_id}")
    check.expect("owner deletes owned task",[r.status_code,r.json],[200,{"result":"ok"}])
    check.expect("no task row remains",check.rows("SELECT id FROM tasks"),[])
    check.verify()


def test_S10_credentials_absent_from_responses(check):
    client,_ = check.user()
    login = check.request(client,"POST","/api/login",json={"username":"qa_owner","password":check.secret})
    task_id = check.task(client)
    task = check.request(client,"GET",f"/api/tasks/{task_id}")
    digest = check.rows("SELECT password_hash FROM users")[0][0]
    exposed = any(value in response.get_data(as_text=True) for response in (login,task)
                  for value in (check.secret,digest,"password_hash"))
    check.expect("no password or hash in sampled success bodies",exposed,False)
    check.verify()


def test_S11_required_title(check):
    client,_ = check.user()
    r = check.request(client,"POST","/api/tasks",json={"title":"   "})
    check.expect("blank title rejected",[r.status_code,r.json],[400,{"error":"title is required"}])
    check.expect("no task written",check.rows("SELECT id FROM tasks"),[])
    check.verify()


def test_S12_type_validation(check):
    client,_ = check.user()
    r = check.request(client,"POST","/api/tasks",json={"title":42})
    check.expect("validation code",r.status_code,400)
    check.expect("JSON error response",r.is_json,True)
    check.expect("no task written",check.rows("SELECT id FROM tasks"),[])
    check.verify()


def test_S13_error_body_does_not_disclose_internals(check):
    client,_ = check.user()
    r = check.request(client,"POST","/api/tasks",json={"title":42})
    body = r.get_data(as_text=True)
    check.expect("error body excludes secrets, debugger and stack trace",
                 any(value in body for value in (check.secret,"Traceback","Werkzeug Debugger","app.py")),False)
    check.verify()


def test_S14_ordinary_search(check):
    client,_ = check.user()
    check.task(client,"Invoice planning")
    check.task(client,"Errands")
    r = check.request(client,"GET","/api/tasks?q=Invoice")
    check.expect("normal query returns matching owner row",
                 [r.status_code,[task["title"] for task in r.json]],[200,["Invoice planning"]])
    check.verify()


def test_S15_search_source_review(check):
    node = source_function("api_list_tasks")
    query_interpolation = any(isinstance(n,ast.JoinedStr) and
                              any(isinstance(child,ast.Name) and child.id=="q" for child in ast.walk(n))
                              for n in ast.walk(node))
    check.expect("search term bound without query interpolation",query_interpolation,False)
    check.verify()


def test_S16_delete_source_review(check):
    node = source_function("api_delete_task")
    uses_session_owner = any(isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and
                             n.value.id=="session" and isinstance(n.slice,ast.Constant) and
                             n.slice.value=="user_id" for n in ast.walk(node))
    check.expect("delete handler looks up session owner for authorization",uses_session_owner,True)
    check.verify()


def test_S17_session_signing_configuration(check):
    tree = ast.parse((ROOT.parent / "app.py").read_text())
    literal = any(isinstance(n,ast.Assign) and isinstance(n.value,ast.Constant) and
                  any(isinstance(t,ast.Subscript) and isinstance(t.slice,ast.Constant) and
                      t.slice.value=="SECRET_KEY" for t in n.targets) for n in ast.walk(tree))
    check.expect("session signing key is not assigned a literal in app source",literal,False)
    check.verify()


def test_S18_auditable_task_mutation(check):
    owner,_ = check.user()
    task_id = check.task(owner)
    check.request(owner,"DELETE",f"/api/tasks/{task_id}")
    tables = [r[0] for r in check.rows("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
              if not r[0].startswith("sqlite_")]
    check.expect("persistent audit table exists in application SQLite",
                 any("audit" in name or "event" in name for name in tables),True)
    check.expect("task deleted",check.rows("SELECT id FROM tasks"),[])
    check.verify()


def test_S19_web_mutation_form_source_review(check):
    template = (ROOT.parent/"templates"/"index.html").read_text()
    base = (ROOT.parent/"templates"/"base.html").read_text()
    check.expect("task-list mutation forms include CSRF token field",
                 any(token in template.lower() for token in ("csrf_token","csrfmiddlewaretoken")),True)
    check.expect("logout uses an explicit POST form",
                 not ('href="{{ url_for(\'logout\') }}"' in base),True)
    check.verify()


def test_S20_pagination_limit(check):
    client,_ = check.user()
    for i in range(12):
        check.task(client,f"Sample {i}")
    r = check.request(client,"GET","/api/tasks?per_page=-1")
    check.expect("negative page size rejected or bounded",
                 [r.status_code, len(r.json) if isinstance(r.json,list) else None]
                 in ([400,None], [200,10]),True)
    check.expect("database fixture unchanged",check.rows("SELECT COUNT(*) FROM tasks")[0][0],12)
    check.verify()
