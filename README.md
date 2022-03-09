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
