import json
import os
import subprocess as sp
import sys

from nusex import CONFIG_DIR

# Load defaults to revert changes when done
with open(CONFIG_DIR / "user.nsc") as f:
    defaults = json.load(f)


def run(command):
    if sys.version_info >= (3, 7, 0):
        return sp.run(command, shell=True, capture_output=True)

    if os.name != "nt":
        return sp.run(f"{command} > /dev/null 2>&1", shell=True)

    # Windows users will have to put up with the output for 3.6 tests.
    return sp.run(command, shell=True)


def test_version():
    run("nsx config -v 0.2.0")
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)
    assert data["default_version"] == "0.2.0"


def test_description():
    run("nsx config -d 'My awesome project!'")
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)
    assert data["default_description"] == "My awesome project!"


def test_repo_user():
    run("nsx config -r https://gitlab.com/tester")
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)
    assert data["repo_user_url"] == "https://gitlab.com/tester"


def test_author():
    run("nsx config -a 'John Smith'")
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)
    assert data["author"] == "John Smith"


def test_author_email():
    run("nsx config -e johnsmith@example.com")
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)
    assert data["author_email"] == "johnsmith@example.com"


def test_default_license():
    run('nsx config -l "Don\'t steal pls"')
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)
    assert data["default_license"] == "Don't steal pls"


def test_multiple_changes():
    run(
        "nsx config -v '{}' -d '{}' -r '{}' -a '{}' -e '{}' -l '{}'".format(
            *defaults.values()
        )
    )
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)
    assert data == defaults
