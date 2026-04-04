# ADR 0003: Use pure Python polling for log tailing

**Status: Accepted**
**Date: 04-04-2026**

## Context

`logsnap watch` needs to follow one or more log files in real
time and stream new lines to the terminal. The implementation
should be simple and require no extra dependencies for `v0.1.0`.


## Decision

Use pure Python file polling: open each file, seek to end, and
loop checking for new lines with a short sleep interval between
iterations. Run until interrupted with `Ctrl+C`.


## Alternatives Considered

- `watchdog`: event driven via OS file system events, more
  robust but adds a dependency and complexity for `v0.1.0` scope
- `subprocess tail`: simple but not cross platform, ties `logsnap`
  to Unix systems


## Consequences
### Positive

- Zero extra dependencies
- Simple to implement and reason about
- Good enough for local file tailing in `v0.1.0`

### Negative

- Polling is less efficient than event-driven approach on large
  numbers of files
- `watchdog` migration needed if `v0.2.0` adds Docker or cloud 
  sources
