#!/usr/bin/env python3
"""FIM-X entry point.

    python run.py                 start the console on http://127.0.0.1:8733
    python run.py --port 9000     use a different port
    python run.py --no-browser    do not open a browser window
    python run.py --verify        verify the audit chain and exit
    python run.py --selftest      run the built-in end-to-end check and exit
"""
from __future__ import annotations

import argparse
import signal
import sys
import threading
import webbrowser

from fimx import analyzers, config
from fimx.core import audit, monitor, retention
from fimx.database import db


def bootstrap() -> None:
    config.ensure_dirs()
    db.init_db()
    analyzers.load_builtin()


def main() -> int:
    parser = argparse.ArgumentParser(prog="fim-x", description="Forensic file integrity monitoring")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8733)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--verify", action="store_true", help="verify the audit chain and exit")
    parser.add_argument("--selftest", action="store_true", help="run the end-to-end self test and exit")
    args = parser.parse_args()

    bootstrap()

    if args.verify:
        result = audit.verify()
        print(f"Audit chain: {'VERIFIED' if result['verified'] else 'FAILED'}")
        print(f"Entries checked: {result['entries_checked']}")
        for problem in result["problems"]:
            print(f"  [{problem['issue']}] seq={problem.get('seq')} {problem.get('event_uid')}: "
                  f"{problem['detail']}")
        print(result["note"])
        return 0 if result["verified"] else 2

    if args.selftest:
        from tests.selftest import run_selftest
        return 0 if run_selftest() else 1

    if args.host not in ("127.0.0.1", "localhost"):
        print("WARNING: FIM-X has no authentication. Binding outside 127.0.0.1 exposes the case "
              "timeline to anyone who can reach this host.", file=sys.stderr)

    for purge in retention.purge_all():
        if purge.get("applied"):
            print(f"  retention {purge['target_name']}: {purge['raw_events_removed']} raw event(s) and "
                  f"{purge['content_snapshots_pruned']} content snapshot(s) pruned")

    resumed = monitor.SERVICE.resume_persisted(auto=bool(db.get_setting("auto_resume_on_start", False)))
    for entry in resumed:
        print(f"  target {entry['target_id']}: "
              f"{'resumed' if entry.get('resumed') else entry.get('note') or entry.get('error')}")

    from fimx.web.api import create_app
    app = create_app()

    url = f"http://{args.host}:{args.port}/"
    print(f"{config.APP_NAME} {config.APP_VERSION}")
    print(f"  data root : {config.APP_ROOT}")
    print(f"  console   : {url}")
    print("  press Ctrl+C to stop\n")

    def shutdown(signum, frame):
        print("\nStopping monitors and closing sessions...")
        monitor.SERVICE.stop_all()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    try:
        signal.signal(signal.SIGTERM, shutdown)
    except (AttributeError, ValueError):
        pass

    if not args.no_browser:
        threading.Timer(1.2, lambda: webbrowser.open(url)).start()

    try:
        app.run(host=args.host, port=args.port, threaded=True, debug=False, use_reloader=False)
    finally:
        monitor.SERVICE.stop_all()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
