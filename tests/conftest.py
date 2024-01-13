"""Top-level pytest plugin."""
import enum
import os
from pathlib import Path

_this_dir = Path(os.path.realpath(__file__)).parent

tools_dir = _this_dir / ".." / "tools"


class CmdExitStatus(enum.IntEnum):
    """Exit statuses of an executed command.

    https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html
    """

    ERROR = 1
    INCORRECT_USAGE = 2
