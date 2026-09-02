"""FIM-X configuration. All state lives under one application data root so the
monitored targets and the application's own storage never overlap."""
from __future__ import annotations

import os
import sys
from pathlib import Path

APP_NAME = "FIM-X"
APP_VERSION = "0.4.6"

def _default_root() -> Path:
    env = os.environ.get("FIMX_HOME")
    if env:
        return Path(env)
    if sys.platform == "win32":
        base = os.environ.get("PROGRAMDATA") or os.path.expanduser("~")
        return Path(base) / "FIM-X"
    return Path(os.path.expanduser("~")) / ".fimx"

APP_ROOT: Path = _default_root()
DB_PATH: Path = APP_ROOT / "fimx.db"
SNAPSHOT_DIR: Path = APP_ROOT / "snapshots"
LOG_DIR: Path = APP_ROOT / "logs"
EXPORT_DIR: Path = APP_ROOT / "exports"

COALESCE_WINDOW_MS = 1500
WRITE_SETTLE_MS = 400
WRITE_SETTLE_RETRIES = 12
LOCKED_FILE_RETRY_MS = 500
QUEUE_MAX = 20000
HASH_CHUNK = 1024 * 1024
DEFAULT_MAX_HASH_MB = 2048

def self_exclusions() -> list[str]:
    return [str(APP_ROOT).replace("\\", "/").rstrip("/") + "/*", str(APP_ROOT).replace("\\", "/")]

DEFAULT_EXCLUSIONS = [
    "*/~$*", "*.tmp", "*.temp", "*.crdownload", "*.part",
    "*/.git/*", "*/node_modules/*",
    "*/System Volume Information/*", "*/$RECYCLE.BIN/*",
    "*/AppData/Local/Temp/*",
]

TEXT_LIKE = {".txt", ".log", ".csv", ".md", ".json", ".xml", ".ini", ".cfg", ".yaml", ".yml", ".sql", ".py", ".bat", ".ps1"}

def ensure_dirs() -> None:
    for d in (APP_ROOT, SNAPSHOT_DIR, LOG_DIR, EXPORT_DIR):
        d.mkdir(parents=True, exist_ok=True)
