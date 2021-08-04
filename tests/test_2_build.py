import json
import os
import shutil
import subprocess as sp
import sys

from nusex import CONFIG_DIR, TEMP_DIR


def run(command):
    if sys.version_info >= (3, 7, 0):
        return sp.run(command, shell=True, capture_output=True)

    if os.name != "nt":
        return sp.run(f"{command} > /dev/null 2>&1", shell=True)

    # Windows users will have to put up with the output for 3.6 tests.
    return sp.run(command, shell=True)


def test_validate_template_names():
    os.chdir("./tests/example_test_pkg")

    bad_templates = ("test-template", "TestTemplate", "folder/test")
    good_templates = ("test", "test_template", "test69")

    # This test locks up if the files already exist, so let's remove
    # them.
    try:
        for tn in good_templates:
            os.remove(CONFIG_DIR / f"{tn}.nsx")
    except FileNotFoundError:
        # If they don't exist, no need to worry.
        pass

    for tn in bad_templates:
        output = run(f"nsx build {tn}")
        if sys.version_info < (3, 7, 0):
            assert output.returncode == 1
        else:
            error = output.stderr.decode().split("\n")[-2].strip()
            assert (
                error
                == "nusex.errors.TemplateBuildError: template names can only contain lower case letters, numbers, and underscores"
            )

    for tn in good_templates:
        output = run(f"nsx build {tn}")
        if output.returncode != 0:
            assert False, output.stderr.decode().split("\n")[-2].strip()

    for tn in good_templates:
        assert os.path.isfile(CONFIG_DIR / f"{tn}.nsx")


def test_correct_manifest():
    with open(CONFIG_DIR / "test.nsx") as f:
        data = json.load(f)

    files = data["files"].keys()
    assert not any(f.endswith(".pyc") for f in files)
    assert not any(".venv" in f for f in files)
    assert ".editorconfig" in files
    assert ".gitignore" in files
    assert "LICENSE" in files
    assert "pyproject.toml" in files
    assert "README.md" in files
    assert "requirements-dev.txt" in files
    assert "requirements.txt" in files
    assert "setup.py" in files


def test_variables_implanted_correctly():
    with open(CONFIG_DIR / "test.nsx") as f:
        data = json.load(f)
    with open(CONFIG_DIR / "user.nsc") as f:
        config = json.load(f)

    assert (
        data["files"]["LICENSE"].split("\n")[2]
        == "Copyright (c) 2021, PROJECTAUTHOR"
    )
    assert data["files"]["MANIFEST.in"].split("\n")[0] == "graft PROJECTNAME"
    assert (
        data["files"]["pyproject.toml"].split("\n")[8]
        == 'extend-exclude = "PROJECTNAME/__init__.py"'
    )
    assert data["files"]["README.md"].split("\n")[0] == "# PROJECTNAME"
    setup = data["files"]["setup.py"].split("\n")
    assert (
        setup[4]
        == '        "PROJECTNAME only supports Python versions 3.6.0 or greater.",'
    )
    assert (
        setup[18]
        == 'with open("PROJECTNAME/__init__.py", mode="r", encoding="utf-8") as f:'
    )
    init = data["files"]["PROJECTNAME/__init__.py"].split("\n")
    assert init[0] == '__productname__ = "PROJECTNAME"'
    assert init[1] == '__version__ = "PROJECTVERSION"'
    assert init[2] == '__description__ = "PROJECTDESCRIPTION"'
    assert init[3] == '__url__ = "PROJECTURL"'
    assert (
        init[4] == '__docs__ = "https://PROJECTNAME.readthedocs.io/en/latest/"'
    )
    assert init[5] == '__author__ = "PROJECTAUTHOR"'
    assert init[6] == '__author_email__ = "PROJECTAUTHOREMAIL"'
    assert init[7] == '__license__ = "PROJECTLICENSE"'
    assert init[8] == '__bugtracker__ = "PROJECTURL/issues"'


def test_from_repo():
    # Same lock up issue as before.
    try:
        os.remove(CONFIG_DIR / "repo_test.nsx")
        shutil.rmtree(TEMP_DIR / "nusex")
    except FileNotFoundError:
        # If they don't exist, no need to worry.
        pass

    run(f"nsx build repo_test -r https://github.com/parafoxia/nusex")

    with open(CONFIG_DIR / "repo_test.nsx") as f:
        data = json.load(f)

    # The nusex repo has all of these, so it's fine to just test this.
    files = data["files"].keys()
    assert not any(f.endswith(".pyc") for f in files)
    assert not any(".venv" in f for f in files)
    assert ".editorconfig" in files
    assert ".gitignore" in files
    assert "CONTRIBUTING.md" in files
    assert "LICENSE" in files
    assert "pyproject.toml" in files
    assert "README.md" in files
    assert "requirements-dev.txt" in files
    assert "requirements-test.txt" in files
    assert "setup.py" in files
