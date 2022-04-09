"""Tests of normname"""

import os
import re
import subprocess

# pytest is available via venv
import pytest  # pylint: disable=import-error

working_dir: str = os.path.dirname(os.path.realpath(__file__))
prog_path: str = f"{working_dir}/../normname"


@pytest.fixture
def files(tmp_path):
    """Provide test files with normalized and denormalized filename."""
    testdir = tmp_path / "normname"
    testdir.mkdir()
    filename_not_ok = testdir / "Incorrect Filename - ěščřžýáíéĚŠČŘŽÝÁÍÉ"
    filename_not_ok.touch()
    filename_ok = testdir / "correct_filename"
    filename_ok.touch()
    return (filename_not_ok, filename_ok)


# pylint: disable=subprocess-run-check,redefined-outer-name
# subprocess-run-check: Tests often make prog to exit with non-zero exit code, raising an error
# is not necessary.
# redefined-outer-name: Collides with the way pytest tests request fixtures

def test_no_args():
    """Test prog without arguments.

    prog must return non-zero exit status, print an error and help msg into
    STDERR and.
    """
    proc = subprocess.run([prog_path], capture_output=True)
    assert proc.returncode != 0
    for keyword in ("usage", "error"):
        assert keyword in proc.stderr.decode("utf-8").lower()


def run_normname(file):
    """Return normalized name of file.

    Uses platform dependent value of os.stat_result.st_ino .
    """
    inode = file.stat().st_ino
    proc = subprocess.run([prog_path, file], capture_output=True)
    assert proc.returncode == 0
    assert not file.exists()  # file was renamed
    new_path = proc.stdout.decode("utf-8").split("->")[-1].strip()
    new_name = new_path.split("/")[-1]
    for child in file.parent.iterdir():  # verify file was renamed
        if child.name == new_name and child.stat().st_ino == inode:
            break
    else:
        raise AssertionError(f"{new_path} not found.")
    return new_name



def test_upper_case(files):
    """Test prog converts upper case to lower case."""
    assert not re.search(r"[A-Z]", run_normname(files[0]))


def test_whitespace(files):
    """Test prog replaces whitespaces with underscores."""
    assert ' ' not in run_normname(files[0])


def test_czech_diacritics(files):
    """Test prog removes Czech diacritics."""
    re_czech_diacritics = r"[ěščřžýáíéĚŠČŘŽÝÁÍÉ]"
    assert not re.search(re_czech_diacritics, run_normname(files[0]))


def test_no_action_filename(files):
    """Test prog doesn't modify filename already conforming the conventions above."""
    filename_ok = files[1]
    proc = subprocess.run([prog_path, filename_ok], capture_output=True)
    assert proc.returncode == 0
    assert filename_ok.exists()  # file was NOT renamed
    assert proc.stdout.decode("utf-8") == ""
