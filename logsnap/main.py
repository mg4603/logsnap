import typer
from logsnap.watcher import start_watch
from logsnap.config import read_config

app = typer.Typer()


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


def main() -> None:
    app()


if __name__ == "__main__":
    main()
