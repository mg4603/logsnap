import typer
from enum import Enum
from typing import Optional

from logsnap.watcher import start_watch
from logsnap.config import read_config
from logsnap.snapshot import run_snap
from logsnap.config_cmd import config_app


class OutputFormat(str, Enum):
    text = "text"
    jsonl = "jsonl"


app = typer.Typer()
app.add_typer(config_app)


@app.command()
def watch(
    keyword: str = typer.Option(
        None,
        "--filter",
        "-f",
        help="Filter lines by keyword (case-insensitive)",
    ),
) -> None:
    """Tail log files defined in config."""

    config = read_config()
    start_watch(config.files, keyword=keyword)


@app.command()
def snap(
    fmt: Optional[OutputFormat] = typer.Option(
        None,
        "--format",
        help=(
            "Output format (text or jsonl). "
            "Overrides config default."
        ),
    ),
) -> None:
    """Export session buffer to a snapshot file."""
    config = read_config()
    run_snap(config, format_override=fmt.value if fmt else None)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
