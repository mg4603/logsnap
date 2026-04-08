# logsnap

`logsnap` lets you tail multiple log files in one place, filter
by keyword, and snapshot the output for later analysis.

![CI](https://github.com/mg4603/logsnap/actions/workflows/ci.yml/badge.svg)

## Why
- Watch multiple log files in one terminal instead of juggling
  separate tail sessions
- You can snapshot logs for later analysis
- You can filter logs to debug why a program with multiple
  dependencies failed

## Demo
![demo](demo.gif)

## Installation
```bash
pipx install logsnap
```
Or with pip:
```bash
pip install logsnap
```

## Quickstart
Setup your config:
```bash
logsnap config init
```

Then watch log files from config:
```bash
logsnap watch
```

Export from buffer to query later:
```bash
logsnap snap
```

## Configuration
```toml
[general]
default_format = "text"
snapshot_dir = "~/logsnap_snapshots"
[sources]
files = [
    "/var/log/syslog",
    "/var/log/app.log"
]
```
 
## Commands
```bash
logsnap watch           starts watching configured log files

logsnap snap            export session buffer to configured 
                        snapshot directory

logsnap config init     create config file at 
                        ~/.config/logsnap/config.toml

logsnap config show     show config details in human readable 
                        format    
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup and
contribution guidelines.

## Architecture decisions
All architectural decisions are documented in 
[docs/adr] (docs/adr).

## License

MIT © Michael George
