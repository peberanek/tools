"""Tests of cnb-fxrates.

Notes:
    * STDOUT and STDERR encoding is system dependend (verify it by the `locale`
      program).
"""

import os
import re
import subprocess

# pytest is available via venv
import pytest  # pylint: disable=import-error

working_dir: str = os.path.dirname(os.path.realpath(__file__))
prog_path: str = f"{working_dir}/../fxrates"
decimal = re.compile(r"\d+\.\d{3}")
sample_fxrates = f"{working_dir}/daily.txt"

# Tests often make prog to exit with non-zero exit code, raising an error
# is not necessary.
# pylint: disable=subprocess-run-check


def test_no_args():
    """Test prog without arguments.

    prog must return non-zero exit status, print an error msg into STDERR and
    a help msg into STDOUT.
    """
    proc = subprocess.run([prog_path], capture_output=True)
    assert proc.returncode != 0
    for keyword in ("usage", "error"):
        assert keyword in proc.stderr.decode("utf-8").lower()


@pytest.mark.parametrize("query", ["mock", "online"])
class TestQuery:
    """Test prog queries a test file or CNB web service correctly."""

    mock_url = {"FXRATES_URL": f"file://{sample_fxrates}"}

    def test_currency_only(self, query):
        """Test prog with only the CURRENCY arg.

        prog must return zero exit status and print the latest FX rate as
        a decimal digit.
        """
        env = self.mock_url if query == "mock" else None
        proc = subprocess.run([prog_path, "EUR"], capture_output=True, env=env)
        assert proc.returncode == 0
        assert decimal.match(proc.stdout.decode("utf-8"))

    def test_currency_and_date(self, query):
        """Test prog with both the CURRENCY and the DATE args.

        prog must return zero exit status and print the FX rate for the given
        DATE as a decimal digit.
        """
        env = self.mock_url if query == "mock" else None
        proc = subprocess.run(
            [prog_path, "USD", "2022-02-01"], capture_output=True, env=env
        )
        assert proc.returncode == 0
        stdout = proc.stdout.decode("utf-8")
        assert decimal.match(stdout)
        assert stdout.strip() == "21.615"  # remove trailing newline

    @pytest.mark.parametrize("code", ["foo", "2022-01-01"])
    def test_invalid_currency_code(self, query, code):
        """Test prog fails with an invalid CURRENCY code.

        prog must return non-zero exit status and print an error msg into STDERR.
        """
        env = self.mock_url if query == "mock" else None
        proc = subprocess.run([prog_path, code], capture_output=True, env=env)
        assert proc.returncode == 1
        assert "error" in proc.stderr.decode("utf-8").lower()

    def test_flipped_currency_and_date(self, query):
        """Test prog fails when CURRENCY and DATE args are flipped.

        prog must return non-zero exit status and print an error msg into STDERR.
        """
        env = self.mock_url if query == "mock" else None
        proc = subprocess.run(
            [prog_path, "2022-02-01", "USD"], capture_output=True, env=env
        )
        assert proc.returncode == 1
        assert "error" in proc.stderr.decode("utf-8").lower()
