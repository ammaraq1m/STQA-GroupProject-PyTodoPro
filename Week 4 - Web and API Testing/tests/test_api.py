"""API contract checks using Flask's test client and a fresh SQLite file per case."""
import json
import secrets
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest
from werkzeug.security import check_password_hash

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent))
import app as target


def redact(data):
    if isinstance(data, dict):
        return {key: (f"<redacted; length={len(value)}>" if isinstance(value, str)
                      else "<redacted>") if key == "password" else redact(value)
                for key, value in data.items()}
    if isinstance(data, list):
        return [redact(item) for item in data]
    return data


class Scenario:
    def __init__(self, database):
        self.database = database
        self.requests = []
        self.assertions = []
        self.secret = secrets.token_urlsafe(18)

    def request(self, client, method, url, payload=None, raw=None):
        headers = {"Accept": "application/json"}
        args = {}
        if raw is not None:
            args.update(data=raw, content_type="application/json")
        elif payload is not None:
            args["json"] = payload
        if raw is not None or payload is not None:
            headers["Content-Type"] = "application/json"
        response = client.open(url, method=method, headers=headers, **args)
        data = response.get_json(silent=True)
        self.requests.append({
            "method": method, "url": url, "headers": headers, "session_after": client.get_cookie("session") is not None,
            "payload": redact(payload) if raw is None else raw, "status": response.status_code,
            "response_content_type": response.mimetype, "json": data,
            "location": response.headers.get("Location"),
            "non_json_excerpt": response.get_data(as_text=True)[:180] if data is None else None,
        })
        return response.status_code, data

    def expect(self, name, actual, expected):
        self.assertions.append({"check": name, "actual": actual, "expected": expected})

    def verify(self):
        failed = [a for a in self.assertions if a["actual"] != a["expected"]]
        assert not failed, json.dumps(failed, ensure_ascii=False)

    def new_client(self):
        return target.app.test_client()

    def account(self, username="qa_owner"):
        client = self.new_client()
        status, data = self.request(client, "POST", "/api/register",
                                    {"username": username, "password": self.secret})
        assert status == 201
        return client, data["id"]

    def task(self, client, title="Alpha planning", **fields):
        status, data = self.request(client, "POST", "/api/tasks", {"title": title, **fields})
        assert status == 201
        return data

    def rows(self, query, *args):
        with sqlite3.connect(self.database) as conn:
            return [list(row) for row in conn.execute(query, args)]

    def count(self, table):
        return self.rows(f"SELECT COUNT(*) FROM {table}")[0][0]

    def rejection(self, result, error, status=400):
        code, body = result
        self.expect("HTTP status", code, status)
        self.expect("JSON error", body.get("error") if isinstance(body, dict) else None,
                    error if error is not None else (body.get("error") if isinstance(body, dict) and body.get("error") else "JSON error message"))


@pytest.fixture(scope="session", autouse=True)
def fresh_response_log():
    (ROOT / "logs/api-responses.ndjson").write_text("")


@pytest.fixture
def scenario(tmp_path, monkeypatch, request):
    db = tmp_path / "test.sqlite3"
    monkeypatch.setattr(target, "DATABASE", str(db))
    monkeypatch.setitem(target.app.config, "TESTING", True)
    monkeypatch.setitem(target.app.config, "PROPAGATE_EXCEPTIONS", False)
    target.init_db()
    case = Scenario(db)
    yield case
    with (ROOT / "logs/api-responses.ndjson").open("a") as stream:
        stream.write(json.dumps({"node": request.node.name, "requests": case.requests,
                                 "assertions": case.assertions}) + "\n")
    db.unlink()


def test_A01_registration(scenario):
    s = scenario
    client, user = s.account()
    s.expect("registration response", s.requests[-1]["json"], {"id": user, "username": "qa_owner"})
    s.expect("session cookie issued", client.get_cookie("session") is not None, True)
    username, stored = s.rows("SELECT username, password_hash FROM users WHERE id = ?", user)[0]
    s.expect("SQLite persisted username", username, "qa_owner")
    s.expect("SQLite stored password hash verifies", stored != s.secret and check_password_hash(stored, s.secret), True)
    s.verify()


@pytest.mark.parametrize("case,username,secret,error", [
    ("A02", None, "valid-length", "invalid username"),
    ("A03", "ab", "valid-length", "invalid username"),
    ("A04", "x"*21, "valid-length", "invalid username"),
    ("A05", "qa_owner", "1234567", "invalid password"),
    ("A06", 123, "valid-length", None),
], ids=["A02","A03","A04","A05","A06"])
def test_registration_validation(scenario, case, username, secret, error):
    s = scenario
    payload = {"password": secret}
    if username is not None:
        payload["username"] = username
    s.rejection(s.request(s.new_client(), "POST", "/api/register", payload), error)
    s.expect("users written", s.count("users"), 0)
    s.verify()


def test_A07_password_boundary(scenario):
    s = scenario
    result = s.request(s.new_client(), "POST", "/api/register",
                       {"username": "qa_owner", "password": secrets.token_hex(4)})
    s.expect("HTTP status", result[0], 201)
    s.expect("users written", s.count("users"), 1)
    s.verify()


def test_A08_duplicate(scenario):
    s = scenario
    s.account()
    code, body = s.request(s.new_client(), "POST", "/api/register",
                           {"username": "qa_owner", "password": s.secret})
    s.expect("duplicate rejected with HTTP 400/409", code in (400, 409), True)
    s.expect("users written", s.count("users"), 1)
    s.verify()


def test_A09_session(scenario):
    s = scenario
    _, user = s.account()
    client = s.new_client()
    s.expect("login response", s.request(client, "POST", "/api/login",
             {"username":"qa_owner", "password":s.secret}), (200, {"id":user, "username":"qa_owner"}))
    s.expect("session authorized", s.request(client,"GET","/api/tasks"), (200, []))
    s.expect("logout redirects", s.request(client,"GET","/logout")[0], 302)
    s.expect("cookie removed", client.get_cookie("session") is None, True)
    s.rejection(s.request(client,"GET","/api/tasks"), "authentication required", 401)
    s.verify()


def test_A10_invalid_login(scenario):
    s = scenario
    s.account()
    client = s.new_client()
    s.rejection(s.request(client,"POST","/api/login",{"username":"qa_owner","password":secrets.token_hex(12)}),
                "invalid credentials", 401)
    s.expect("signed out", client.get_cookie("session") is None, True)
    s.verify()


def test_A11_categories(scenario):
    s = scenario
    code, body = s.request(s.new_client(),"GET","/api/categories")
    s.expect("HTTP status", code, 200)
    s.expect("categories match SQLite", [[x["id"],x["name"]] for x in body],
             s.rows("SELECT id,name FROM categories ORDER BY name"))
    s.verify()


def test_A12_auth_matrix(scenario):
    s = scenario
    client = s.new_client()
    for method, url in [("GET","/api/tasks"),("POST","/api/tasks"),("GET","/api/tasks/1"),
                        ("PUT","/api/tasks/1"),("DELETE","/api/tasks/1"),("GET","/api/dashboard")]:
        s.rejection(s.request(client,method,url), "authentication required", 401)
    s.expect("no task writes", s.count("tasks"), 0)
    s.verify()


def test_A13_create_get(scenario):
    s = scenario
    client, owner = s.account()
    task = s.task(client, "  Alpha planning  ", category_id=1, description="Fixture", due_date="2099-04-10")
    result = s.request(client,"GET",f"/api/tasks/{task['id']}")
    s.expect("detail equals creation", result, (200,task))
    s.expect("task fields", [task[k] for k in ("title","category","description","due_date","done","urgency","completed_at")],
             ["Alpha planning","Work","Fixture","2099-04-10",False,"Upcoming",None])
    s.expect("SQLite row",s.rows("SELECT user_id,title,category_id,description,due_date,done FROM tasks"),
             [[owner,"Alpha planning",1,"Fixture","2099-04-10",0]])
    s.verify()


@pytest.mark.parametrize("case,payload,raw,error", [
    ("A14", {}, None, "title is required"),
    ("A15", {"title":"   "}, None, "title is required"),
    ("A16", {"title":42}, None, None),
    ("A17", None, '{"title":', "title is required"),
    ("A18", {"title":"Invalid date fixture","due_date":"not-a-date"}, None, None),
    ("A19", ["title"], None, None),
], ids=["A14","A15","A16","A17","A18","A19"])
def test_create_validation(scenario, case, payload, raw, error):
    s = scenario
    client, _ = s.account()
    s.rejection(s.request(client,"POST","/api/tasks",payload,raw),error)
    s.expect("SQLite task title and date rows",s.rows("SELECT title,due_date FROM tasks"),[])
    s.verify()


def test_A20_update_reopen_delete(scenario):
    s = scenario
    client, _ = s.account()
    task = s.task(client,description="Keep me")
    url = f"/api/tasks/{task['id']}"
    code, completed = s.request(client,"PUT",url,{"title":"Revision","done":True})
    s.expect("completion response", [code,completed["title"],completed["description"],
                                    completed["done"],bool(completed["completed_at"])],
             [200,"Revision","Keep me",True,True])
    s.expect("SQLite completion",s.rows("SELECT title,done,completed_at FROM tasks"),
             [["Revision",1,completed["completed_at"]]])
    code, reopened = s.request(client,"PUT",url,{"done":False})
    s.expect("reopened response", [code,reopened["done"],reopened["completed_at"]],[200,False,None])
    s.expect("delete response",s.request(client,"DELETE",url),(200,{"result":"ok"}))
    s.rejection(s.request(client,"GET",url), "not found", 404)
    s.expect("SQLite task count",s.count("tasks"),0)
    s.verify()


@pytest.mark.parametrize("case,payload,raw",[
    ("A21",{"title":"   "},None),("A22",{"done":"false"},None),("A23",None,'{"done":'),
],ids=["A21","A22","A23"])
def test_update_validation(scenario,case,payload,raw):
    s = scenario
    client, _ = s.account()
    task = s.task(client)
    s.rejection(s.request(client,"PUT",f"/api/tasks/{task['id']}",payload,raw),None)
    s.expect("SQLite unchanged",s.rows("SELECT title,done,completed_at FROM tasks"),
             [[task["title"],0,None]])
    s.verify()


def test_A24_owner_isolation(scenario):
    s = scenario
    owner, owner_id = s.account()
    other, other_id = s.account("qa_peer")
    s.task(owner,"Owner task")
    s.task(other,"Peer task")
    for client, title in [(owner,"Owner task"),(other,"Peer task")]:
        code, data = s.request(client,"GET","/api/tasks")
        s.expect("account sees own list",[code,[x["title"] for x in data]],[200,[title]])
        s.expect("account dashboard",s.request(client,"GET","/api/dashboard"),
                 (200,{"total":1,"open":1,"overdue":0,"due_soon":0,"completed_this_week":0}))
    s.expect("SQLite ownership",s.rows("SELECT user_id,title FROM tasks ORDER BY id"),
             [[owner_id,"Owner task"],[other_id,"Peer task"]])
    s.verify()


def test_A25_no_match(scenario):
    s = scenario
    client,_ = s.account()
    for method in ("GET","PUT"):
        s.rejection(s.request(client,method,"/api/tasks/999",{"title":"New"} if method=="PUT" else None),
                    "not found",404)
    s.expect("no task rows",s.count("tasks"),0)
    s.verify()


def test_A26_pagination(scenario):
    s = scenario
    client,_ = s.account()
    for i in range(12):
        s.task(client,f"Sample {i}")
    for query, expected in [("",list(range(11,1,-1))),("?page=0&per_page=2",[11,10]),
                            ("?page=1&per_page=2",[9,8]),("?page=6&per_page=2",[])]:
        code, data = s.request(client,"GET","/api/tasks"+query)
        s.expect("page status and titles",[code,[x["title"] for x in data]],
                 [200,[f"Sample {i}" for i in expected]])
    s.verify()


def test_A27_negative_page_size(scenario):
    s = scenario
    client,_ = s.account()
    for i in range(12):
        s.task(client,f"Sample {i}")
    code,data = s.request(client,"GET","/api/tasks?per_page=-1")
    s.expect("status or bounded response",code==400 or (code==200 and len(data)<=10),True)
    s.expect("SQLite fixture retained",s.count("tasks"),12)
    s.verify()


def test_A28_filter(scenario):
    s = scenario
    client,_ = s.account()
    task = s.task(client,"Alpha planning",category_id=1)
    s.task(client,"Alpha home",category_id=2)
    s.task(client,"Beta planning",category_id=1)
    s.request(client,"PUT",f"/api/tasks/{task['id']}",{"done":True})
    for q, matches in [("q=Alpha",["Alpha home","Alpha planning"]),
                       ("category=Work&status=open",["Beta planning"]),
                       ("category=Work&status=done&q=Alpha",["Alpha planning"]),("q=missing",[])]:
        code, data = s.request(client,"GET","/api/tasks?"+q)
        s.expect(q,[code,[x["title"] for x in data]],[200,matches])
    s.verify()


def test_A29_dashboard(scenario):
    s = scenario
    client,_ = s.account()
    for title, days in [("Old",-1),("Tomorrow",1),("Finished",5)]:
        task = s.task(client,title,due_date=(date.today()+timedelta(days=days)).isoformat())
    s.request(client,"PUT",f"/api/tasks/{task['id']}",{"done":True})
    s.expect("dashboard counters",s.request(client,"GET","/api/dashboard"),
             (200,{"total":3,"open":2,"overdue":1,"due_soon":1,"completed_this_week":1}))
    s.verify()


def test_A30_due_today(scenario):
    s = scenario
    client,_ = s.account()
    task = s.task(client,"Today",due_date=date.today().isoformat())
    s.expect("urgency label",task["urgency"],"Due Today")
    s.verify()



def test_A33_peer_read_update_denied(scenario):
    s = scenario
    owner, owner_id = s.account()
    peer, _ = s.account("qa_peer")
    task = s.task(owner, "Owner task")
    url = f"/api/tasks/{task['id']}"
    s.rejection(s.request(peer, "GET", url), "not found", 404)
    s.rejection(s.request(peer, "PUT", url, {"title": "Peer revision"}), "not found", 404)
    s.expect("owner still reads original", s.request(owner, "GET", url), (200, task))
    s.expect("SQLite owner and title unchanged",
             s.rows("SELECT user_id,title FROM tasks"), [[owner_id, "Owner task"]])
    s.verify()
