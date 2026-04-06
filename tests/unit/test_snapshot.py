import pytest
from json import loads as json_loads

from logsnap.snapshot import (
    export_snapshot,
    cleanup_session,
    run_snap,
)
from logsnap.config import Config


def test_raises_error_session_log_missing(tmp_path, capsys):
    session = tmp_path / "session.log"
    snapshot = tmp_path / "snapshot"

    with pytest.raises(FileNotFoundError):
        export_snapshot(session, snapshot, "text")


def test_snapshot_file_created(tmp_path):
    session = tmp_path / "session.log"
    session.write_text("line1\n")

    snapshot = tmp_path / "snapshot"
    export_snapshot(session, snapshot, "text")

    assert snapshot.exists()


def test_lines_written_correctly_in_text(tmp_path):
    session = tmp_path / "session.log"
    session.write_text("line1\n")

    snapshot = tmp_path / "snapshot"
    export_snapshot(session, snapshot, "text")

    assert snapshot.read_text() == "line1\n"


def test_lines_written_correctly_in_jsonl(tmp_path):
    session = tmp_path / "session.log"
    session.write_text("app.log|timestamp|line1\n")

    snapshot = tmp_path / "snapshot"
    export_snapshot(session, snapshot, "jsonl")

    lines = snapshot.read_text().splitlines()
    assert len(lines) == 1
    record = json_loads(lines[0])

    assert record["source"] == "app.log"
    assert record["timestamp"] == "timestamp"
    assert record["line"] == "line1"


def test_raises_error_on_invalid_format(tmp_path):
    session = tmp_path / "session.log"
    session.write_text("line1\n")

    snapshot = tmp_path / "snapshot"
    with pytest.raises(ValueError):
        export_snapshot(session, snapshot, "csv")


def test_session_deleted_after_cleanup(tmp_path):
    session = tmp_path / "session.log"
    session.write_text("line1\n")

    cleanup_session(session)

    assert not session.exists()


def test_cleanup_session_no_error_if_missing(tmp_path):
    session = tmp_path / "session.log"

    cleanup_session(session)


def test_format_override_takes_precedence(tmp_path):
    session = tmp_path / "session.log"
    session.write_text("app.log|2026-04-06T14:23:01|lines1\n")

    snapshot_dir = tmp_path / "snapshots"
    config = Config(
        default_format="text", snapshot_dir=str(snapshot_dir)
    )

    run_snap(
        config, format_override="jsonl", session_path=session
    )
    snapshots = list(snapshot_dir.iterdir())
    assert snapshots[0].suffix == ".jsonl"


def test_default_format_used_when_no_override(tmp_path):
    session = tmp_path / "session.log"
    session.write_text("app.log|2026-04-06T14:23:01|lines1\n")

    snapshot_dir = tmp_path / "snapshots"

    config = Config(
        default_format="text", snapshot_dir=str(snapshot_dir)
    )

    run_snap(config, session_path=session)
    snapshots = list(snapshot_dir.iterdir())
    assert snapshots[0].suffix == ".txt"


def test_snapshot_created_in_snapshot_dir(tmp_path):
    session = tmp_path / "session.log"
    session.write_text("app.log|2026-04-06T14:23:01|line1\n")

    snapshot_dir = tmp_path / "snapshots"

    config = Config(
        default_format="text", snapshot_dir=str(snapshot_dir)
    )
    run_snap(config, session_path=session)
    snapshots = list(snapshot_dir.iterdir())
    assert len(snapshots) == 1


def test_session_cleaned_up_after_snap(tmp_path):
    session = tmp_path / "session.log"
    session.write_text("app.log|2026-04-06T14:23:01|line1\n")

    snapshot_dir = tmp_path / "snapshots"

    config = Config(
        default_format="text", snapshot_dir=str(snapshot_dir)
    )
    run_snap(config, session_path=session)
    assert not session.exists()
