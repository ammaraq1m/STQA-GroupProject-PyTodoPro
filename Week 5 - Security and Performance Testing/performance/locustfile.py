"""Authenticated read-only Locust scenario for the isolated fixture server."""
from itertools import cycle

from locust import HttpUser, constant_pacing, task

ENDPOINTS = (
    ("/", "/", "My Tasks"),
    ("/dashboard", "/dashboard", "Dashboard"),
    ("/api/tasks?page=0&per_page=10", "/api/tasks", None),
    ("/api/dashboard", "/api/dashboard", None),
)


class ReadUser(HttpUser):
    wait_time = constant_pacing(1)

    def on_start(self):
        index, username, password = next(self.environment.fixture_accounts)
        self.routes = cycle(ENDPOINTS[index % 4:] + ENDPOINTS[:index % 4])
        with self.client.post("/api/login", json={"username": username, "password": password},
                              name="setup /api/login", timeout=3, allow_redirects=False,
                              catch_response=True) as response:
            try:
                accepted = response.status_code == 200 and response.json()["username"] == username
            except (ValueError, KeyError, TypeError):
                accepted = False
            if accepted:
                self.environment.authenticated += 1
            else:
                response.failure("Fixture login failed")
                self.environment.auth_errors += 1

    @task
    def read(self):
        path, name, heading = next(self.routes)
        with self.client.get(path, name=name, timeout=3,
                             allow_redirects=False, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Expected 200, received {response.status_code}")
                return
            if heading:
                valid = f"<h1>{heading}</h1>" in response.text
            else:
                try:
                    body = response.json()
                    valid = (isinstance(body, list) and len(body) == 10) if name == "/api/tasks" else (
                        isinstance(body, dict) and body.get("total") == 60 and body.get("open") == 45)
                except ValueError:
                    valid = False
            if not valid:
                response.failure("Unexpected response content")
