from __future__ import annotations

from json import dumps as json_dumps
from pathlib import Path
from datetime import datetime

from logsnap.config import Config
from logsnap.watcher import SESSION_PATH


def export_snapshot(
    session_path: Path, snapshot_path: Path, default_format: str
) -> None:
    default_format = default_format.lower()
    if default_format not in ("jsonl", "text"):
        raise ValueError(
            f"Unsupported format: {default_format}. "
            "Use 'text' or 'jsonl'."
        )

    if not session_path.exists():
        raise FileNotFoundError(
            f"Session file not found at {session_path}.\n"
            "Run `logsnap watch` first.\n"
        )

    with (
        session_path.open("r") as src,
        snapshot_path.open("w") as dst,
    ):
        while True:
            line = src.readline()
            if not line:
                break

            if default_format == "text":
                dst.write(line)
            elif default_format == "jsonl":
                parts = line.rstrip("\n").split("|", 2)
                record = {
                    "timestamp": parts[1],
                    "source": parts[0],
                    "line": parts[2],
                }
                dst.write(
                    json_dumps(record, ensure_ascii=False)
                    + "\n"
                )


def cleanup_session(session_path: Path) -> None:
    session_path.unlink(missing_ok=True)


def run_snap(
    config: Config,
    format_override: str | None = None,
    session_path: Path = SESSION_PATH,
) -> None:
    fmt = format_override or config.default_format
    snapshot_dir = Path(config.snapshot_dir)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    snapshot_filename = (
        f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        f".{fmt if fmt == 'jsonl' else 'txt'}"
    )

    snapshot_path = snapshot_dir / snapshot_filename

    export_snapshot(session_path, snapshot_path, fmt)
    cleanup_session(session_path)
