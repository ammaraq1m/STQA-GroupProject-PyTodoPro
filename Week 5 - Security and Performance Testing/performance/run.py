"""Seed an isolated database, run four bounded Locust stages and export evidence."""
import csv
from datetime import date, datetime, timedelta, timezone
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import secrets
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
import time

from locust.env import Environment
import gevent
import psutil
import requests
from werkzeug.security import generate_password_hash

from locustfile import ReadUser

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent))
import app as target

HOST = "http://127.0.0.1:51795"
WORKLOADS = (1, 5, 10, 25)
SECONDS = 60
MIB = 1024**2


def utc():
    return datetime.now(timezone.utc).isoformat()


def seed(database):
    target.DATABASE = str(database)
    target.init_db()
    accounts = []
    now = datetime.now()
    due_dates = [(date.today() + timedelta(days=d)).isoformat() for d in (-2, 1, 7)] + [None]
    with sqlite3.connect(database) as conn:
        for i in range(25):
            username = f"perf_user_{i+1:02}"
            password = secrets.token_urlsafe(20)
            user_id = conn.execute("INSERT INTO users(username,password_hash) VALUES (?,?)",
                                   (username, generate_password_hash(password))).lastrowid
            accounts.append((i, username, password))
            fixtures = []
            for j in range(60):
                done = int(j % 4 == 0)
                fixtures.append((user_id, f"Sample task {j+1:02}", "Disposable fixture",
                                 j % 4 + 1, due_dates[(j // 4) % 4], done,
                                 (now-timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S") if done else None,
                                 now.isoformat()))
            conn.executemany(
                """INSERT INTO tasks(user_id,title,description,category_id,due_date,done,completed_at,created_at)
                   VALUES (?,?,?,?,?,?,?,?)""", fixtures)
    return accounts


def capture_environment(database):
    read = lambda p: Path(p).read_text().strip() if Path(p).exists() else None
    with sqlite3.connect(database) as conn:
        counts = {name: conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
                  for name in ("users", "tasks", "categories")}
    return {
        "captured_utc": utc(), "platform": platform.platform(), "os_release": read("/etc/os-release"),
        "cpu_model": next((s.split(":",1)[1].strip() for s in (read("/proc/cpuinfo") or "").splitlines()
                           if s.startswith("model name")), None),
        "affinity_cpus": len(os.sched_getaffinity(0)), "cgroup_cpu_max": read("/sys/fs/cgroup/cpu.max"),
        "cgroup_memory_max": read("/sys/fs/cgroup/memory.max"), "host_ram_mib": round(psutil.virtual_memory().total/MIB),
        "host_available_mib": round(psutil.virtual_memory().available/MIB),
        "python": platform.python_version(), "sqlite": sqlite3.sqlite_version,
        **{pkg: version(pkg) for pkg in ("locust", "flask", "werkzeug", "psutil", "matplotlib")},
        "database_bytes": database.stat().st_size, "fixture_rows": counts, "workloads": WORKLOADS,
        "seconds_per_stage": SECONDS, "spawn_rate": 2, "pace_seconds": 1,
    }


def sample(server, generator, runner, users, elapsed, previous, monitor, last):
    requests_now = runner.stats.total.num_requests
    failures_now = runner.stats.total.num_failures
    inc, errors = requests_now - previous[0], failures_now - previous[1]
    data = {
        "users": users, "elapsed_s": round(elapsed, 2), "host_cpu_pct": psutil.cpu_percent(),
        "server_cpu_pct_one_core": server.cpu_percent(), "generator_cpu_pct_one_core": generator.cpu_percent(),
        "combined_rss_mib": round((server.memory_info().rss+generator.memory_info().rss)/MIB, 1),
        "available_mib": round(psutil.virtual_memory().available/MIB, 1),
        "interval_requests": inc, "interval_failures": errors,
    }
    monitor.append(data)
    last["cpu"] = last["cpu"] + 1 if data["host_cpu_pct"] > 95 else 0
    last["error"] = last["error"] + 1 if inc >= 20 and errors / inc > .15 else 0
    if data["available_mib"] < 512 or data["combined_rss_mib"] > 1024:
        return (requests_now, failures_now), "memory threshold"
    if last["cpu"] >= 3:
        return (requests_now, failures_now), "CPU threshold"
    if last["error"] >= 3:
        return (requests_now, failures_now), "error threshold"
    return (requests_now, failures_now), None


def stage(users, server_proc, accounts, monitor):
    env = Environment(user_classes=[ReadUser], host=HOST)
    env.fixture_accounts = iter(accounts[:users])
    env.authenticated = env.auth_errors = 0
    runner = env.create_local_runner()
    server, generator = psutil.Process(server_proc.pid), psutil.Process()
    reason = None
    records = []
    elapsed = 0
    try:
        print(f"{utc()} stage {users}: ramping at 2 users/s", flush=True)
        runner.start(users, spawn_rate=2)
        deadline = time.monotonic() + 30
        while env.authenticated < users and time.monotonic() < deadline:
            if env.auth_errors or server_proc.poll() is not None:
                break
            gevent.sleep(.2)
        if env.authenticated != users:
            return {"users": users, "status": "Not Run", "reason": "authentication ramp failed"}, []
        gevent.sleep(3)
        runner.stats.reset_all()
        psutil.cpu_percent()
        server.cpu_percent()
        generator.cpu_percent()
        start = time.monotonic()
        print(f"{utc()} stage {users}: measuring", flush=True)
        previous = (0, 0)
        streaks = {"cpu": 0, "error": 0}
        for second in range(1, SECONDS+1):
            gevent.sleep(max(0, start+second-time.monotonic()))
            elapsed = time.monotonic()-start
            if server_proc.poll() is not None:
                reason = "Flask exited"
                break
            if second % 5 == 0:
                previous, reason = sample(server, generator, runner, users, elapsed, previous, monitor, streaks)
                if reason:
                    break
        # Copy values at the end of the measurement window before stopping users.
        for metric in [*runner.stats.entries.values(), runner.stats.total]:
            if not metric.num_requests or metric.name.startswith("setup"):
                continue
            rows = metric.num_requests
            records.append({
                "users": users, "endpoint": metric.name, "method": metric.method or "ALL",
                "seconds": round(elapsed, 3), "requests": rows, "failures": metric.num_failures,
                "error_pct": round(metric.num_failures*100/rows, 3), "requests_per_s": round(rows/elapsed, 3),
                "mean_ms": round(metric.avg_response_time, 3), "median_ms": metric.median_response_time,
                "p95_ms": metric.get_response_time_percentile(.95),
            })
        print(f"{utc()} stage {users}: {elapsed:.2f}s, {runner.stats.total.num_requests} requests, "
              f"{runner.stats.total.num_failures} failures, stop={reason}", flush=True)
        return {"users": users, "status": "Stopped" if reason else "Completed",
                "seconds": round(elapsed,3), "authenticated": env.authenticated, "reason": reason,
                "errors": [str(error.error) for error in runner.stats.errors.values()]}, records
    finally:
        runner.quit()


def write_csv(name, rows):
    if rows:
        with (ROOT / "results" / name).open("w", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)


def main():
    if version("flask") != "3.0.3":
        raise RuntimeError("Install the project Flask 3.0.3 pin before measuring")
    all_records, monitoring, stages = [], [], []
    with TemporaryDirectory(prefix="pytodo-week5-perf-") as directory:
        database = Path(directory) / "load.sqlite3"
        accounts = seed(database)
        snapshot = capture_environment(database)
        (ROOT / "results" / "environment.json").write_text(json.dumps(snapshot, indent=2)+"\n")
        print(f"{utc()} preflight: {snapshot['fixture_rows']}, {snapshot['database_bytes']} bytes, "
              f"{snapshot['affinity_cpus']} CPUs", flush=True)
        with (ROOT / "logs" / "flask.log").open("w") as log:
            server = subprocess.Popen([sys.executable, "-B", str(Path(__file__).with_name("server.py")), str(database)],
                                      stdout=log, stderr=log)
            try:
                for _ in range(50):
                    if server.poll() is not None:
                        raise RuntimeError("Flask exited during preflight")
                    try:
                        if requests.get(HOST+"/api/categories", timeout=1).status_code == 200:
                            break
                    except requests.RequestException:
                        pass
                    gevent.sleep(.2)
                else:
                    raise RuntimeError("Flask not ready")
                advance = True
                for users in WORKLOADS:
                    if advance:
                        result, records = stage(users, server, accounts, monitoring)
                        all_records.extend(records)
                        advance = result["status"] == "Completed"
                    else:
                        result = {"users":users, "status":"Not Run","reason":"earlier stage did not complete"}
                    stages.append(result)
                    write_csv("performance.csv", all_records)
                    write_csv("monitoring.csv", monitoring)
                    (ROOT / "results" / "stages.json").write_text(json.dumps(stages, indent=2)+"\n")
            finally:
                server.terminate()
                server.wait(timeout=10)
    return 0 if all(item["status"] == "Completed" for item in stages) else 1


if __name__ == "__main__":
    raise SystemExit(main())
