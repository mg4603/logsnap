import time
import threading
from logsnap.watcher import (
    tail_file,
    open_handles,
    poll_files,
    start_watch,
)


def test_tail_file_returns_new_lines(tmp_path):
    log = tmp_path / "app.log"
    log.write_text("line1\nline2\n")
    f = log.open("r")
    f.seek(0, 2)
    log.open("a").write("line3\n")
    lines = tail_file(f, keyword=None)
    f.close()
    assert lines == ["line3"]


def test_tail_file_filters_by_keyword(tmp_path):
    log = tmp_path / "app.log"
    log.write_text("")
    f = log.open("r")
    f.seek(0, 2)

    with log.open("a") as a:
        a.write("ERROR something failed\n")
        a.write("INFO all good\n")
    lines = tail_file(f, "error")

    f.close()
    assert lines == ["ERROR something failed"]


def test_tail_file_filter_case_insensitive(tmp_path):
    log = tmp_path / "app.log"
    log.write_text("")
    f = log.open("r")
    f.seek(0, 2)

    with log.open("a") as a:
        a.write("error lowercase\n")
        a.write("ERROR uppercase\n")
        a.write("Error capitalize\n")

    lines = tail_file(f, keyword="ERROR")
    f.close()

    assert set(lines) == {
        "error lowercase",
        "ERROR uppercase",
        "Error capitalize",
    }


def test_empty_list_when_no_new_lines(tmp_path):
    log = tmp_path / "app.log"
    log.write_text("")
    f = log.open("r")
    f.seek(0, 2)
    lines = tail_file(f, keyword=None)
    f.close()

    assert lines == []


def test_open_handles_skips_missing_files(tmp_path, capsys):
    missing = str(tmp_path / "missing.log")

    def run():
        open_handles([missing])

    t = threading.Thread(target=run)
    t.start()
    t.join(timeout=1)

    captured = capsys.readouterr()
    assert "skipping" in captured.err


def test_poll_files_returns_prefixed_lines(
    tmp_path,
):
    log = tmp_path / "app.log"
    log.write_text("")
    f = log.open("r")
    f.seek(0, 2)

    with log.open("a") as a:
        a.write("line1\n")

    handles = {log: f}
    lines = poll_files(handles)
    f.close()

    assert lines == ["[app.log] line1"]


def test_poll_files_returns_empty_when_none():
    lines = poll_files(None)
    assert lines == []


def test_start_watch_no_valid_files(tmp_path, capsys):
    missing = tmp_path / "missing.log"
    start_watch([missing])
    captured = capsys.readouterr()
    assert "no valid log files to watch" in captured.err


def test_start_watch_prints_lines(tmp_path, capsys):
    log = tmp_path / "app.log"
    log.write_text("")

    def run():
        start_watch([str(log)])

    t = threading.Thread(target=run, daemon=True)
    t.start()
    time.sleep(0.2)

    with log.open("a") as f:
        f.write("hello world\n")

    time.sleep(0.3)
    t.join(timeout=0.1)

    captured = capsys.readouterr()
    assert "hello world" in captured.out
    assert "app.log" in captured.out


def test_start_watch_skips_invalid_paths(tmp_path, capsys):
    valid_path = tmp_path / "valid.log"
    valid_path.write_text("")
    missing_path = str(tmp_path / "missing.log")

    def run():
        start_watch([str(valid_path), missing_path])

    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join(timeout=0.1)

    captured = capsys.readouterr()
    assert "skipping" in captured.err
