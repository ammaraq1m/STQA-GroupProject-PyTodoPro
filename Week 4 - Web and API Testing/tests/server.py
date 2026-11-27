"""Launch the original application against a temporary SQLite database."""
from pathlib import Path
import sys
import signal
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import app as target

def stop_server(*_):
    raise SystemExit(0)

signal.signal(signal.SIGTERM, stop_server)

with TemporaryDirectory(prefix="pytodo-week4-") as directory:
    target.DATABASE = str(Path(directory) / "test.sqlite3")
    target.init_db()
    print(f"Isolated database: {target.DATABASE}", flush=True)
    target.app.run(host="127.0.0.1", port=int(sys.argv[1]), debug=False)
