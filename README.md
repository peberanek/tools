# Tools

A collection of personal tools.

## bashlib

A library of Bash utilities.

Example:
```bash
source /path/to/bashlib.bash

bashlib::err "Some error msg"
```

## homesync

Rsync wrapper for syncing contents of $HOME with a destination directory.

### Example

Contents of `~/.homesync_exclude`:
```
# Patterns excluded from sync (for details see rsync FILTER RULES)
venv/
.venv/
.mypy_cache/
.pytest_cache/
.cache
Downloads/
.local/
Public/
.var/
```

Run sync:
```
homesync --exclude-from ~/.homesync_exclude '/run/media/user/usb_drive/homesync/host/user'
```

## motd

Print a random message of the day to stdout. When opening a new terminal, I prefer to see something positive, encouraging or personally important to remember.

### Example

Contents of `~/.motd` (1 message per line):
```
Life is not a race. (Kenneth Reitz)
Practicality beats purity. (The Zen of Python)
Tiny is mighty. Tiny is safe. (BJ Fogg)
New chances come every day. (Marek Vaňha)
```

Add this to your `~/.bashrc`
```
motd ~/.motd
```

## How to run tests

```bash
pipenv sync
pre-commit install
```

``` bash
pipenv run pytest
```
