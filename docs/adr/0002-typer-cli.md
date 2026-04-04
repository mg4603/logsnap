# ADR 0002: Use Typer for CLI interface

**Status: Accepted**
**Date: 04-04-2026**

## Context

logsnap needs a CLI framework to handle commands, subcommands,
flags, and help text. The framework should be Pythonic, low
boilerplate, and support subcommands cleanly.


## Decision

Use Typer as the CLI framework. It builds on top of Click and
uses Python type hints for argument definitions, resulting in
minimal boilerplate, and automatic help text generation.


## Alternatives Considered

- `argparse`: stdlib, no dependency, but verbose and requires 
  manual help text
- `Click`: solid and widely used, but more boilerplate than 
  `Typer` for subcommands


## Consequences
### Positive

- Minimal boilerplate for defining commands
- Automatic help text from type hints and docstrings
- Consistent with scaffoldr


### Negative

- Extra dependency (typer)
- Typer is opinionated - less flexibility for non-standard
  CLI patterns
