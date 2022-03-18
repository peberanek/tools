# Tools

A collection of various command-line tools.

## rpm-ostree-notify

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
