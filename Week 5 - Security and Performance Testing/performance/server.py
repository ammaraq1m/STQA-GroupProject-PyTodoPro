"""Start the unmodified Flask app for a managed local performance run."""
import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import app as target

if __name__ == "__main__":
    target.DATABASE = sys.argv[1]
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    target.app.run(host="127.0.0.1", port=51795, debug=False, threaded=True)
