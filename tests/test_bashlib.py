"""Tests of bashlib.bash."""


import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest

from . import conftest


@pytest.fixture(autouse=True)
def bashlib_path(tmp_path: Path) -> Path:
    """Provide path to bashlib."""
    file = "bashlib.bash"
    shutil.copy(conftest.tools_dir / file, tmp_path)
    return tmp_path / file


@pytest.fixture(autouse=True)
def _chdir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Change working directory to tmp_path.

    Make sure custom scripts operate in the tmp_path directory.
    """
    monkeypatch.chdir(tmp_path)


@pytest.fixture()
def script(request: pytest.FixtureRequest, tmp_path: Path, bashlib_path: Path) -> Path:
    script = textwrap.dedent(
        f"""\
        #!/bin/bash
        source {bashlib_path}
        """
    )
    marker = request.node.get_closest_marker("script_append")
    assert marker is not None, "Missing data for fixture marker 'script_append'."
    script += textwrap.dedent(marker.args[0])
    path = tmp_path / "script"
    path.touch(0o700)
    with path.open("w") as f:
        f.write(script)
    return path


@pytest.mark.script_append("bashlib::err 'My error message.'")
def test_err(script: Path):
    """Test fn err.

    Execute a script that calls bashlib::err. An error message should be
    printed to stderr.
    """
    proc = subprocess.run([script], check=True, capture_output=True)
    assert not proc.stdout
    assert proc.stderr.strip() == b"My error message."


@pytest.mark.script_append(
    """\
    bashlib::ask 'My question:'
    exit $?
    """
)
@pytest.mark.parametrize(
    ("answer", "exit_status"),
    [("y", 0), ("n", 1), ("invalid\ny", 0)],
    ids=["yes", "no", "invalid_input"],
)
def test_ask(script: Path, answer: str, exit_status: int):
    """Test fn ask.

    Execute a script that calls bashlib::ask. The script should print
    a prompt text and then read stdin. It should return 0 on reading 'y',
    and 1 on 'n' (corresponding to the fn return code). Other input should
    result in an error message and reading from stdin until a correct input
    is provided.

    I don't know how to test the prompt text. It is displayed only if the
    input is coming from a terminal.
    """
    proc = subprocess.run(
        [script], input=answer.encode(), check=False, capture_output=True
    )
    assert proc.returncode == exit_status
    assert not proc.stdout
    if "invalid" in answer:
        assert b"Invalid input." in proc.stderr
    else:
        assert not proc.stderr


@pytest.mark.script_append("bashlib::confirm_cmd 'touch my_file'")
@pytest.mark.parametrize(("answer"), ["y", "n"])
def test_confirm_cmd(tmp_path: Path, script: Path, answer: str):
    """Test fn confirm_cmd.

    Execute a script that calls bashlib::confirm_cmd. The script should print
    a prompt text (a command to be executed) and then read stdin. It should
    execute the command on reading 'y', or skipping it on reading 'n'. Invalid
    input is covered by the test_ask test.
    """
    proc = subprocess.run(
        [script], input=answer.encode(), check=True, capture_output=True
    )
    assert b"touch my_file" in proc.stdout
    assert not proc.stderr
    new_file = tmp_path / "my_file"
    if answer == "y":
        assert new_file.exists()
    else:
        assert not new_file.exists()
