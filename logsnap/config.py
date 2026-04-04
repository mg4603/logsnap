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
