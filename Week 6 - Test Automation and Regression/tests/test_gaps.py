"""Complement Week 4's contract coverage with boundary and ownership checks."""
from datetime import datetime, timedelta
import re
import sqlite3

import pytest

import helpers
from test_api import scenario  # Uses the staged Week 4 Flask-client fixture.


REFERENCE = datetime(2026, 2, 15, 12, 0, 0)


class FixedDatetime(datetime):
    @classmethod
    def now(cls, tz=None):
        assert tz is None
        return REFERENCE


@pytest.mark.parametrize("age,expected", [
    (timedelta(seconds=0), 1), (timedelta(days=7), 1),
    (timedelta(days=7, seconds=1), 0), (timedelta(seconds=-1), 0),
], ids=["GAP01", "GAP02", "GAP03", "GAP04"])
def test_dashboard_completion_window(scenario, monkeypatch, age, expected):
    client, _ = scenario.account()
    task = scenario.task(client, "Dashboard boundary")
    completed = (REFERENCE - age).strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(scenario.database) as db:
        db.execute("UPDATE tasks SET done=1, completed_at=? WHERE id=?", (completed, task["id"]))
    monkeypatch.setattr(helpers, "datetime", FixedDatetime)
    code, data = scenario.request(client, "GET", "/api/dashboard")
    web = client.get("/dashboard")
    values = re.findall(r'<div class="stat-value">\s*(\d+)\s*</div>', web.get_data(as_text=True))
    scenario.expect("seeded age in seconds", (REFERENCE-datetime.fromisoformat(completed)).total_seconds(),
                    age.total_seconds())
    scenario.expect("API completed-this-week count", [code, data["completed_this_week"]], [200, expected])
    scenario.expect("HTML dashboard status and all five counters", [web.status_code, values],
                    [200, ["1", "0", "0", "0", str(expected)]])
    scenario.verify()


def test_update_due_date_atomicity(scenario):
    client, _ = scenario.account()
    task = scenario.task(client, "Existing due date", due_date="2099-04-10")
    route = f"/api/tasks/{task['id']}"
    result = scenario.request(client, "PUT", route, {"due_date": "not-a-date"})
    scenario.rejection(result, None)
    scenario.expect("SQLite retains the previous due date",
                    scenario.rows("SELECT due_date FROM tasks"), [["2099-04-10"]])
    code, payload = scenario.request(client, "GET", route)
    scenario.expect("task is still readable with original date",
                    [code, payload.get("due_date") if payload else None], [200, "2099-04-10"])
    scenario.verify()


def test_web_peer_edit_denied(scenario):
    owner, owner_id = scenario.account()
    peer, _ = scenario.account("qa_peer")
    task = scenario.task(owner, "Owner fixture")
    route = f"/tasks/{task['id']}/edit"
    for response in (peer.get(route), peer.post(route, data={"title": "Peer revision"})):
        scenario.expect("peer receives redirect to own list", [response.status_code,response.location], [302,"/"])
        scenario.expect("owner title absent from denial response", b"Owner fixture" in response.data, False)
    scenario.expect("owner still reaches edit form", owner.get(route).status_code, 200)
    scenario.expect("owner and title unchanged", scenario.rows("SELECT user_id,title FROM tasks"),
                    [[owner_id, "Owner fixture"]])
    scenario.verify()
