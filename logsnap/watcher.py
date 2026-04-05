from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import TextIO

POLL_INTERVAL = 0.1


def tail_file(f: object, keyword: str | None) -> list[str]:
    """Read new lines from an open file handle."""
    lines = []
    try:
        line = f.readline()
        while line:
            if (
                keyword is None
                or keyword.lower() in line.lower()
            ):
                lines.append(line.rstrip("\n"))
            line = f.readline()
    except OSError as e:
        print(
            f"[warning] error reading file: {e}",
            file=sys.stderr,
        )

    return lines


def open_handles(file_paths: list[str]) -> dict[Path, TextIO]:
    handles: dict[Path, TextIO] = {}

    for path_str in file_paths:
        path = Path(path_str).expanduser()
        if not path.exists():
            print(
                f"[warning] file not found, skipping: {path}",
                file=sys.stderr,
            )
            continue
        try:
            f = path.open("r")
            f.seek(0, 2)
            handles[path] = f
        except OSError as e:
            print(
                f"[warning] cannot open {path}: {e}",
                file=sys.stderr,
            )

    return handles


def poll_files(
    handles: dict[Path, TextIO] | None = None,
    keyword: str | None = None,
) -> list[str]:
    if handles is None:
        return []

    lines: list[str] = []

    for path, f in handles.items():
        for line in tail_file(f, keyword):
            lines.append(f"[{path.name}] {line}")

    return lines


def start_watch(
    file_paths: list[str], keyword: str | None = None
) -> None:
    """Tail multiple log files and return to terminal"""
    handles = open_handles(file_paths)

    if not handles:
        print(
            "[error] no valid log files to watch",
            file=sys.stderr,
        )
        return

    print(
        f"Watching {len(handles)} file(s)."
        "Press Ctrl+C to stop.\n"
    )

    try:
        while True:
            for line in poll_files(handles, keyword):
                print(line)

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        for f in handles.values():
            f.close()
