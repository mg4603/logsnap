from __future__ import annotations

import tomllib
from pathlib import Path
from dataclasses import dataclass, field

import tomli_w

CONFIG_PATH = Path.home() / ".config" / "logsnap" / "config.toml"


@dataclass
class Config:
    files: list[str] = field(default_factory=list)
    default_format: str = "text"
    snapshot_dir: str = str(Path.home() / "logsnap-snapshots")


def read_config(path: Path = CONFIG_PATH) -> Config:
    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found at {path}.\n"
            "Run `logsnap config init` to create one.\n"
        )

    with path.open("rb") as f:
        data = tomllib.load(f)

    general = data.get("general", {})
    sources = data.get("sources", {})

    return Config(
        files=sources.get("files", []),
        default_format=general.get("default_format", "text"),
        snapshot_dir=general.get(
            "snapshot_dir",
            Path.home() / "logsnap-snapshots",
        ),
    )


def write_config(config: Config, path: Path = CONFIG_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "general": {
            "default_format": config.default_format,
            "snapshot_dir": config.snapshot_dir,
        },
        "sources": {"files": config.files},
    }

    with path.open("wb") as f:
        tomli_w.dump(data, f)
