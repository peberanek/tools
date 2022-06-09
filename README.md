# Tools

Collection of various command-line tools. Used and tested on [Fedora 36 Silverblue](https://silverblue.fedoraproject.org/).

## trading_prep

Print basic info for quick orientation in the actual trading day.

## fxrates

Get foreign market exchange rates (declared by the Czech National Bank) to the command-line.

## medik-tedik-dl

Download images from [medik-tedik.cz](http://www.medik-tedik.cz/) with ease.

## normname

Helps to keep naming conventions for files (e.g. no whitespaces, lowercase only).

## rbak

Backup $HOME dir via rsync. Simply syncs the content of $HOME with a destination dir.

Config files:

* `~/.config/rbak/exclude`:

    > Replace `<user>` with your user name.

    ```text
    # Patterns excluded from rsync transfer. Replace <user> with your user name. For details
    # see `man rsync`, section `INCLUDE/EXCLUDE PATTERN RULES`.
    <user>/.cache
    <user>/Downloads
    <user>/.local/share/Trash
    ```

* `~/.config/rbak/rbak.conf`:

    > Add path to the destination dir to the `DEST=` key below. E.g. `DEST="/run/media/joe/usbdrive/backup_dir"`.

    ```bash
    DEST=FIXME
    ```

## rpm-ostree-notify

[`rpm-ostree`](https://coreos.github.io/rpm-ostree/) is a great tool providing automatic upgrades of my Fedora Silverblue workstation. However, the tool doesn't notify me when the pending upgrade contains security fixes. This means I may work whole the day on unpached system. `rpm-ostree-notify` sends me a desktop notification when security fixes are ready to be applied.

Config files:

* `rpm-ostree-notify.conf` (must reside in the same directory as `rpm-ostree-notify`):

    ```bash
    FREQUENCY="30m"
    START_DELAY="5m"
    IMMEDIATE_UPGRADE="1"
    ```

* Desktop file `~/.config/autostart/rpm-ostree-notify.desktop` (Gnome) for running it as startup application:

    > Add path to the executable to the `Exec=` key below.

    ```ini
    [Desktop Entry]
    Name=rpm-ostree-notify
    Comment=Notify me when the pending rpm-ostree deployment contains security advisories
    Exec=FIXME
    Type=Application
    ```

## Testing

Tests are written in Python 3 using Pytest. Install Python venv and run the tests like this:

```bash
python3 -m venv venv  # create a new venv
source venv/bin/activate
python3 -m pip install pytest
cd tests/  # pytest config files lives there
python3 -m pytest  # run all tests
```

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

### Examples

```text
docs: correct spelling of README
test: mark tests requiring internet connection
feat(rpm-ostree-notify): use a config file
```

### Git hook

Install git hook for auto-checking the commit message:

```bash
cd .git/hooks/ && ln -s ../../.githooks/commit-msg commit-msg && cd -
```

If you need to bypass commit-msg hook check, use:

```bash
git commit -m "foobar" --no-verify
```
