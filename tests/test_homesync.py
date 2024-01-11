"""Tests of homesync."""
import filecmp
import subprocess
from pathlib import Path

import pytest

from . import conftest

executable = conftest.tools_dir / "homesync"


@pytest.fixture(autouse=True)
def mock_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    mock_home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(mock_home))
    return mock_home


@pytest.fixture()
def mock_user_data(mock_home: Path) -> Path:
    """Populate mock user dir with some data and return path to the user dir."""
    mock_home.mkdir()
    user_dir = mock_home / "user"
    user_dir.mkdir()
    documents = user_dir / "Documents"
    documents.mkdir()
    document1 = documents / "document1"
    document1.touch()
    downloads = user_dir / "Downloads"
    downloads.mkdir()
    download1 = downloads / "download1"
    download1.touch()
    return user_dir


def test_no_args():
    """Test running homesync without arguments.

    Running homesync without arguments should fail with the exit status for
    incorrect usage. A help message should be printed to stderr.
    """
    proc = subprocess.run([executable], check=False, capture_output=True)
    assert proc.returncode == conftest.CmdExitStatus.INCORRECT_USAGE
    assert not proc.stdout
    assert b"usage: homesync" in proc.stderr


@pytest.mark.parametrize("help_option", ["-h", "--help"])
def test_help(help_option):
    """Test homesync help message.

    Help message should be printed to stdout. Homesync should exit with success.
    Both short (-h) and long (--help) help options should work.
    """
    proc = subprocess.run([executable, help_option], check=True, capture_output=True)
    assert not proc.stderr
    assert b"usage: homesync" in proc.stdout


@pytest.fixture()
def dest_dir(tmp_path: Path) -> Path:
    dest_dir = tmp_path / "dest_dir"
    dest_dir.mkdir()
    return dest_dir


def assert_dirs_equal(dcmp: filecmp.dircmp) -> None:
    """Compare files and dirs (recursively) in dcmp and assert they are equal.

    Notes:
        Makes only shallow comparison (if the os.stat() signatures (file type,
        size, and modification time) of both files are identical, the files
        are taken to be equal).

    Args:
        dcmp (filecmp.dircmp): directory comparison object

    Raises:
        AssertionError: if any of the compared dirs are not equal

    Returns:
        None
    """
    # The assertion message is currently not very informative, but at least
    # sufficient to detect an unexpected difference.
    assert not dcmp.left_only
    assert not dcmp.right_only
    assert not dcmp.diff_files
    assert not dcmp.funny_files
    for sub_dcmp in dcmp.subdirs.values():
        assert_dirs_equal(sub_dcmp)


@pytest.mark.usefixtures("mock_user_data")
def test_sync(mock_home: Path, dest_dir: Path):
    """Test a successful sync.

    Homesync should sync all files from a mock $HOME dir to the dest dir.
    All synced files should be printed to stdout.
    """
    proc = subprocess.run([executable, dest_dir], check=True, capture_output=True)
    assert_dirs_equal(filecmp.dircmp(mock_home, dest_dir))
    assert not proc.stderr
    assert b"user/Documents/document1" in proc.stdout


@pytest.fixture()
def exclude_patterns_file(mock_user_data: Path) -> Path:
    file = mock_user_data / ".homesync_exclude"
    with file.open("w") as f:
        f.write("Downloads/")
    return file


def test_sync_with_excluded_files(
    mock_home: Path, dest_dir: Path, exclude_patterns_file: Path
):
    """Test a successful sync with some files being excluded.

    Homesync should sync only non-excluded files from a mock $HOME dir to
    a dest dir.
    """
    proc = subprocess.run(
        [
            executable,
            dest_dir,
            "--exclude-from",
            exclude_patterns_file,
        ],
        check=True,
        capture_output=True,
    )
    assert_dirs_equal(filecmp.dircmp(mock_home, dest_dir, ignore=["Downloads"]))
    assert not (dest_dir / "user" / "Downloads").exists()
    assert not proc.stderr
    assert b"user/Downloads/" not in proc.stdout
