import os
import subprocess as sp
import sys

from nusex import CONFIG_DIR


def run(command):
    if sys.version_info >= (3, 7, 0):
        return sp.run(command, shell=True, capture_output=True)

    if os.name != "nt":
        return sp.run(f"{command} > /dev/null 2>&1", shell=True)

    # Windows users will have to put up with the output for 3.6 tests.
    return sp.run(command, shell=True)


def test_delete_singular():
    run("nsx delete testing")
    assert not os.path.isfile(CONFIG_DIR / "testing.nsx")


def test_delete_multiple():
    templates = ("renamed_template", "test420", "repo_test")
    for tn in templates:
        run(f"nsx delete {tn}")
        assert not os.path.isfile(CONFIG_DIR / f"{tn}.nsx")
