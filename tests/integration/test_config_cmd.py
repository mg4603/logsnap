from typer.testing import CliRunner


from logsnap.main import app


def test_config_init_happy_path(tmp_path, monkeypatch):
    runner = CliRunner()
    config_path = tmp_path / "config.toml"

    monkeypatch.setattr(
        "logsnap.config.CONFIG_PATH", config_path
    )
    monkeypatch.setattr(
        "logsnap.config_cmd.CONFIG_PATH", config_path
    )

    result = runner.invoke(
        app,
        ["config", "init"],
        input=f"{str(tmp_path / 'logspan_snapshots')}\ntext\n{str(tmp_path / 'app.log')}\n\n",
    )

    assert result.exit_code == 0
    assert f"Config written to {config_path}" in result.output


def test_config_init_user_overwrites(tmp_path, monkeypatch):
    runner = CliRunner()
    config_path = tmp_path / "config.toml"

    config_path.write_text("")

    monkeypatch.setattr(
        "logsnap.config_cmd.CONFIG_PATH", config_path
    )
    monkeypatch.setattr(
        "logsnap.config.CONFIG_PATH", config_path
    )

    result = runner.invoke(
        app,
        ["config", "init"],
        input=f"y\n{str(tmp_path / 'logsnap_snapshots')}\ntext\n{str(tmp_path / 'app.log')}\n\n",
    )

    assert result.exit_code == 0
    assert f"Config written to {config_path}" in result.output


def test_config_init_user_aborts(tmp_path, monkeypatch):
    runner = CliRunner()
    config_path = tmp_path / "config.toml"

    config_path.write_text("")

    monkeypatch.setattr(
        "logsnap.config.CONFIG_PATH", config_path
    )
    monkeypatch.setattr(
        "logsnap.config_cmd.CONFIG_PATH", config_path
    )

    result = runner.invoke(app, ["config", "init"], input="N\n")

    assert result.exit_code == 1


def test_config_init_blank_line_stops_file_input(
    tmp_path, monkeypatch
):
    runner = CliRunner()
    config_path = tmp_path / "config.toml"

    monkeypatch.setattr(
        "logsnap.config.CONFIG_PATH", config_path
    )
    monkeypatch.setattr(
        "logsnap.config_cmd.CONFIG_PATH", config_path
    )

    result = runner.invoke(
        app,
        ["config", "init"],
        input=f"{str(tmp_path / 'logsnap_dir')}\ntext\n{str(tmp_path / 'app.log')}\n{str(tmp_path / 'app1.log')}\n\n",
    )

    assert result.exit_code == 0

    config_text = config_path.read_text()
    assert "app.log" in config_text
    assert "app1.log" in config_text


def test_config_show_happy_path(tmp_path, monkeypatch):
    runner = CliRunner()
    config_path = tmp_path / "config.toml"

    config_path.write_text("""[general]
default_format = "text"
snapshot_dir = "~/logsnap_snapshots"
[sources]
files = [
    "/var/log/syslog",
    "/var/log/app.log"
]
                           """)

    monkeypatch.setattr(
        "logsnap.config.CONFIG_PATH", config_path
    )
    monkeypatch.setattr(
        "logsnap.config_cmd.CONFIG_PATH", config_path
    )

    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
    assert "default_format : 'text'" in result.output
    assert (
        "snapshot_dir   : '~/logsnap_snapshots'"
        in result.output
    )
    assert "files" in result.output
    assert (
        "               : 1. /var/log/syslog" in result.output
    )
    assert (
        "               : 2. /var/log/app.log" in result.output
    )


def test_config_show_config_does_not_exist(
    tmp_path, monkeypatch
):
    runner = CliRunner()
    config_path = tmp_path / "config.toml"

    monkeypatch.setattr(
        "logsnap.config.CONFIG_PATH", config_path
    )
    monkeypatch.setattr(
        "logsnap.config_cmd.CONFIG_PATH", config_path
    )

    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 1
    assert f"{config_path} doesn't exist" in result.output
