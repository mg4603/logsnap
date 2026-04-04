# ADR 0001: Use TOML for configuration file format

**Status: Accepted**
**Date: 04-04-2026**

## Context

logsnap needs a user-editable config file to store log file
paths, default output format, and snapshot output directory.
The format should be human-friendly and require minimal 
dependencies.


## Decision

Use TOML format for the config file located at 
`~/.config/logsnap/config.toml`. Python 3.11+ includes `tomllib`
in the stdlib for reading. For writing, `tomli-w` will be used
as a light-weight dependency.


## Alternatives considered

- `YAML`: human-friendly but requires pyyaml, an additional 
  dependency with a large surface area
- `JSON`: no extra dependency, but not pleasant to hand-edit 
  and lacks comment support
  

## Consequences
### Positive

- No extra dependency for reading config
- Human-editable and version-controllable
- Consistent with python ecosystem standards (pyproject.toml)


### Negative

- Python 3.11+ is the minimum supported version
- tomli-w needed as dependency for config writes
