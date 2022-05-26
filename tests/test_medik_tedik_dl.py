"""Tests of medik-tedik-dl."""

import os
import subprocess

working_dir: str = os.path.dirname(os.path.realpath(__file__))
prog_path: str = f"{working_dir}/../medik-tedik-dl"

# Tests often make prog to exit with non-zero exit code, raising an error
# is not useful.
# pylint: disable=subprocess-run-check


def test_no_args():
    """Test prog without arguments.

    prog must return non-zero exit status, print error msg and usage into
    STDERR.
    """
    proc = subprocess.run([prog_path], capture_output=True)
    assert proc.returncode != 0
    for keyword in ("usage", "error"):
        assert keyword in proc.stderr.decode("utf-8").lower()
