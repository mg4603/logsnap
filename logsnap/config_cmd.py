import typer
from typing import List

from logsnap.config import (
    CONFIG_PATH,
    Config,
    write_config,
    read_config,
)

config_app = typer.Typer(
    name="config", help="Manage logsnap config."
)


@config_app.command()
def init() -> None:
    """Create ~/.config/logsnap/config.toml interactively."""
    if CONFIG_PATH.exists():
        overwrite = typer.confirm(
            f"{CONFIG_PATH} already exists. Overwrite?"
        )
        if not overwrite:
            typer.abort()

    snapshot_dir: str = typer.prompt(
        "Directory in which to store logsnap snapshots.",
        default="~/.config/logsnap/logsnap_snapshots/",
    )

    default_format: str = typer.prompt(
        "Format in which logsnap snapshots are exported.",
        default="text",
    )
    files: List[str] = []

    while True:
        value = typer.prompt(
            "Log file path. (blank line to stop)", default=""
        )
        if value == "":
            break
        files.append(value)

    cfg = Config(
        snapshot_dir=snapshot_dir,
        default_format=default_format,
        files=files,
    )

    write_config(cfg)
    typer.echo(f"Config written to {CONFIG_PATH}.")


@config_app.command()
def show() -> None:
    """Print current config values."""

    try:
        cfg = read_config(CONFIG_PATH)
    except FileNotFoundError:
        typer.echo(f"{CONFIG_PATH} doesn't exist.")
        raise typer.Exit(code=1)

    typer.echo(f"default_format : {cfg.default_format!r}")
    typer.echo(f"snapshot_dir   : {cfg.snapshot_dir!r}")
    typer.echo("\nfiles           ")

    for i, file in enumerate(cfg.files, start=1):
        typer.echo(f"               : {i}. {file}")
