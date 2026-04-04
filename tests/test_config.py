import pytest
from pathlib import Path
from logsnap.config import Config, read_config, write_config


def test_write_and_read_config(tmp_path):
    config_path = tmp_path / "config.toml"
    config = Config(
        files=["/var/log/app.log"], default_format="json", snapshot_dir="/tmp/snapshots"
    )
    write_config(config, path=config_path)
    loaded = read_config(path=config_path)

    assert loaded.files == ["/var/log/app.log"]
    assert loaded.default_format == "json"
    assert loaded.snapshot_dir == "/tmp/snapshots"


def test_read_config_missing_file(tmp_path):
    missing = tmp_path / "nonexistent.toml"
    with pytest.raises(FileNotFoundError):
        read_config(path=missing)


def test_write_creates_parent_dirs(tmp_path):
    config_path = tmp_path / "nested" / "dir" / "config.toml"
    config = Config()
    write_config(config, path=config_path)
    assert config_path.exists()


def test_default_config_values():
    config = Config()
    assert config.files == []
    assert config.default_format == "text"
    assert "logsnap-snapshots" in config.snapshot_dir
