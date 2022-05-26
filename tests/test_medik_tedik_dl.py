"""Tests of medik-tedik-dl."""

import os
import subprocess
from filecmp import cmp

working_dir: str = os.path.dirname(os.path.realpath(__file__))
prog_path: str = f"{working_dir}/../medik-tedik-dl"
data_dir: str = f"{working_dir}/data/medik_tedik_dl"

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


def test_img_download(tmp_path):
    """Test prog downloads requested image."""
    env = {
        "TEDIK_MEDIK_DL_CONTENT_LOCATION": f"file://{data_dir}/"
    }  # notice the trailing slash
    image = {
        "gallery_url": f"file://{data_dir}/index.php?foto=202201",
        "number": "1",
        "local_path": f"{data_dir}/fotogalerie/atletika/2022/202201/b74a1489.jpg",
    }

    proc = subprocess.run(
        [prog_path, "--dest-dir", tmp_path, image["gallery_url"], image["number"]],
        capture_output=True,
        env=env,
    )
    assert proc.returncode == 0
    dest_subdir = tmp_path / "atletika"
    assert dest_subdir.exists()
    dest_subdir_content = list(dest_subdir.iterdir())
    assert len(dest_subdir_content) == 1
    assert cmp(dest_subdir_content[0], image["local_path"])
