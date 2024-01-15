"""Tests of motd."""
import subprocess
from pathlib import Path

import pytest

from . import conftest

executable = conftest.tools_dir / "motd"


def test_no_args():
    """Test running motd without arguments.

    Running motd without arguments should fail with the exit status for
    incorrect usage. A help message should be printed to stderr.
    """
    proc = subprocess.run([executable], check=False, capture_output=True)
    assert proc.returncode == conftest.CmdExitStatus.INCORRECT_USAGE
    assert not proc.stdout
    assert b"usage: motd" in proc.stderr


@pytest.mark.parametrize("help_option", ["-h", "--help"])
def test_help(help_option):
    """Test motd help message.

    Help message should be printed to stdout. Motd should exit with success.
    Both short (-h) and long (--help) help options should work.
    """
    proc = subprocess.run([executable, help_option], check=True, capture_output=True)
    assert not proc.stderr
    assert b"usage: motd" in proc.stdout


@pytest.fixture()
def invalid_msg_file(tmp_path: Path) -> dict:
    """Provide dict of paths to invalid msg files.

    Returns:
        dict: {
            'nonexistent': Path to a nonexistent file.
            'unreadable': Path to an unreadable file.
            'empty': Path to an empty file.
        }
    """
    unreadable_file = tmp_path / "unreadable"
    unreadable_file.touch(mode=0o200)  # writable, so it can be deleted during cleanup
    empty_file = tmp_path / "empty"
    empty_file.touch()
    return {
        "nonexistent": tmp_path / "nonexistent",
        "unreadable": unreadable_file,
        "empty": empty_file,
    }


@pytest.mark.parametrize("issue_type", ["nonexistent", "unreadable", "empty"])
def test_invalid_msg_file(invalid_msg_file: dict, issue_type: str):
    """Test motd with an invalid file.

    Motd with a nonexistent, unreadable or empty file should fail with
    the exit status for error. A message should be printed to stderr.
    """
    proc = subprocess.run(
        [executable, invalid_msg_file[issue_type]], check=False, capture_output=True
    )
    assert proc.returncode == conftest.CmdExitStatus.ERROR
    assert not proc.stdout
    assert "Error:" in proc.stderr.decode()


@pytest.fixture()
def msg_file(tmp_path: Path) -> dict:
    """Provide dict with path to a msg file and its content.

    Returns:
        dict: {
            'path': Path to a file with a msg.
            'content': Content of the file (a single message of the day).
        }
    """
    content = "My message"
    path = tmp_path / "messages"
    with path.open("w") as f:
        f.write(content)
    return {"path": path, "content": content}


def test_print_msg(msg_file: dict):
    """Test that motd prints a message from a file.

    A message from a given file should be printed to stdout. Motd should
    exit with success.
    """
    proc = subprocess.run(
        [executable, msg_file["path"]], check=True, capture_output=True
    )
    assert not proc.stderr
    assert proc.stdout.decode().strip() == msg_file["content"]
