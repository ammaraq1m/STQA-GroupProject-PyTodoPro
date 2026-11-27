"""Run the focused suite from unchanged prior sources in a disposable staging tree."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
W4 = REPO / "Week 4 - Web and API Testing" / "tests"
W5 = REPO / "Week 5 - Security and Performance Testing" / "tests"
MANIFEST = json.loads((ROOT / "tests" / "manifest.json").read_text())
MODULES = {"api": "test_api.py", "security": "test_security.py", "new": "test_gaps.py"}
EVIDENCE = {"api": "api-responses.ndjson", "security": "security-evidence.ndjson", "new": "api-responses.ndjson"}


def when():
    return datetime.now(timezone.utc).isoformat()


def stage_files(stage):
    mapping = {
        W4 / "test_api.py": "test_api.py", W4 / "server.py": "server.py",
        W4 / "web.cjs": "web.cjs", W5 / "test_security.py": "test_security.py",
        ROOT / "tests" / "test_gaps.py": "test_gaps.py",
    }
    fingerprints = {}
    for original, filename in mapping.items():
        fingerprints[str(original.relative_to(REPO))] = hashlib.sha256(original.read_bytes()).hexdigest()
        copy = stage / "tests" / filename
        shutil.copyfile(original, copy)
        if filename == "web.cjs":
            source = copy.read_text()
            begin = "      const result={id,group,objective,steps,expected,requests:[],status:'Fail'};"
            end = "      run.cases.push(result);"
            if source.count(begin) != 1 or source.count(end) != 1:
                raise ValueError("Week 4 runner timing hooks must be reviewed")
            copy.write_text(source.replace(begin, "      const caseStart=performance.now();\n"+begin)
                            .replace(end, "      result.durationSeconds=(performance.now()-caseStart)/1000;\n"+end))
    for name in ("app.py", "helpers.py", "templates", "static"):
        (stage.parent/name).symlink_to(REPO/name, target_is_directory=(REPO/name).is_dir())
    return fingerprints


def process(cmd, stage, filename, env=None):
    start = time.perf_counter()
    try:
        with (stage / "logs" / filename).open("w") as log:
            code = subprocess.run(cmd, cwd=stage, stdout=log, stderr=subprocess.STDOUT,
                                  env=env, timeout=180, check=False).returncode
    except subprocess.TimeoutExpired:
        code = 124
        with (stage / "logs" / filename).open("a") as log:
            print("Week 6 child process exceeded its time limit", file=log)
    return {"exitCode": code, "wallSeconds": round(time.perf_counter()-start, 3)}


def ndjson(path):
    if path.is_file():
        for line in path.read_text().splitlines():
            yield json.loads(line)


def pytest_cases(logs):
    report = logs / "pytest-junit.xml"
    outcomes = {item.attrib["name"]: item for item in ET.parse(report).iter("testcase")} if report.is_file() else {}
    for group, filename in MODULES.items():
        items = {row.get("node", row.get("test")): row for row in ndjson(logs/EVIDENCE[group])}
        for test_id, selector in MANIFEST[group].items():
            node = outcomes.get(selector)
            evidence = items.get(selector, {})
            assertions = evidence.get("assertions", [])
            error = next((node.find(tag) for tag in ("error","failure") if node.find(tag) is not None),
                         None) if node is not None else None
            if node is None or node.find("skipped") is not None:
                status = "Not Run"
            elif error is not None and (error.tag == "error" or not any(a["actual"] != a["expected"] for a in assertions)):
                status = "Infrastructure Error"
            else:
                status = "Fail" if error is not None else "Pass"
            yield {"id":test_id, "group":group, "source":"new" if group=="new" else "reused",
                   "selector":filename+"::"+selector, "status":status,
                   "durationSeconds":float(node.attrib["time"]) if node is not None else None,
                   "assertions": assertions,
                   "error":error.attrib.get("message") if error is not None else None}


def browser_cases(logs):
    path = logs / "web-results.json"
    run = json.loads(path.read_text()) if path.is_file() else {}
    observed = {case["id"]:case for case in run.get("cases", [])}
    for test_id in MANIFEST["browser"]:
        case = observed.get(test_id)
        if case is None:
            yield {"id":test_id,"group":"browser","source":"reused","status":"Not Run","durationSeconds":None}
        else:
            selected = {k:v for k,v in case.items() if k != "requests"}
            if case.get("screenshotError") or "actual" not in case:
                selected["status"] = "Infrastructure Error"
            yield {**selected,"group":"browser","source":"reused","selector":"web.cjs::"+test_id}


def main():
    start = time.perf_counter()
    result = {"started":when(),"processes":{}}
    with TemporaryDirectory(prefix="pytodo-week6-") as directory:
        stage = Path(directory) / "repo" / "week"
        for name in ("tests","logs"):
            (stage/name).mkdir(parents=True)
        result["sourceSha256"] = stage_files(stage)
        selectors = [f"tests/{MODULES[group]}::{selector}" for group in MODULES
                     for selector in MANIFEST[group].values()]
        result["processes"]["pytest"] = process(
            [sys.executable,"-B","-m","pytest","-p","no:cacheprovider","--tb=short","-v",
             "--junitxml=logs/pytest-junit.xml", *selectors], stage,"pytest.log")
        env = dict(os.environ, QA_PYTHON=sys.executable)
        installs = [str(ROOT/"tests"/"node_modules"),env.get("NODE_PATH")]
        env["NODE_PATH"] = os.pathsep.join(part for part in installs if part)
        result["processes"]["browser"] = process(
            ["node","tests/web.cjs"], stage,"browser.log",env)
        result["stagedCases"] = [*pytest_cases(stage/"logs"), *browser_cases(stage/"logs")]
        web = stage/"logs"/"web-results.json"
        if web.is_file():
            raw = json.loads(web.read_text())
            result["browser"] = {key:raw.get(key) for key in ("node","playwright","browser","options","fatal")}
        for name in ("logs","screenshots"):
            source = stage/name
            if source.is_dir():
                shutil.copytree(source,ROOT/name,dirs_exist_ok=True)
    result["cases"] = result.pop("stagedCases") + [
        {"id":test_id,"group":"deferred","source":"deferred","status":"Not Run","reason":reason,
         "durationSeconds":None} for test_id,reason in MANIFEST["deferred"].items()]
    result["finished"] = when()
    result["wallSeconds"] = round(time.perf_counter()-start,3)
    (ROOT/"logs"/"regression-results.json").write_text(json.dumps(result,indent=2)+"\n")
    for status in ("Pass","Fail","Infrastructure Error","Not Run"):
        print(f"{status}: {sum(case['status']==status for case in result['cases'])}")
    print(f"Runner wall time: {result['wallSeconds']:.3f} seconds")
    return 1 if any(x["status"]!="Pass" for x in result["cases"] if x["group"]!="deferred") else 0


if __name__ == "__main__":
    raise SystemExit(main())
