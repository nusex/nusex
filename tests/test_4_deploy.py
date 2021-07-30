import os
import subprocess as sp
import sys


def run(command):
    if sys.version_info >= (3, 7, 0):
        return sp.run(command, shell=True, capture_output=True)

    if os.name != "nt":
        return sp.run(f"{command} > /dev/null 2>&1", shell=True)

    # Windows users will have to put up with the output for 3.6 tests.
    return sp.run(command, shell=True)


def test_check_template_exists():
    # This directory may not exist if it's been cloned.
    os.makedirs("../awesome_pkg", exist_ok=True)
    os.chdir("../awesome_pkg")
    output = run("nsx deploy this_template_doesnt_exist")
    if sys.version_info < (3, 7, 0):
        assert output.returncode == 1
    else:
        error = output.stderr.decode().split("\n")[-2].strip()
        assert (
            error
            == "nusex.errors.NoMatchingTemplates: no template named 'this_template_doesnt_exist' exists"
        )


def test_perfect_deployment():
    run("nsx deploy testing")

    assert os.path.isfile("./awesome_pkg/__init__.py")
    assert os.path.isfile("./awesome_pkg/errors.py")
    assert os.path.isfile("./.editorconfig")
    assert os.path.isfile("./.gitignore")
    assert os.path.isfile("./LICENSE")
    assert os.path.isfile("./MANIFEST.in")
    assert os.path.isfile("./pyproject.toml")
    assert os.path.isfile("./README.md")
    assert os.path.isfile("./requirements-dev.txt")
    assert os.path.isfile("./requirements.txt")
    assert os.path.isfile("./setup.py")

    with open("./LICENSE") as f:
        # This can't be precisely tested because of the user's config.
        assert f.read().split("\n")[2] != "Copyright (c) 2021, PROJECTAUTHOR"

    with open("./MANIFEST.in") as f:
        assert f.read().split("\n")[0] == "graft awesome_pkg"

    with open("./pyproject.toml") as f:
        assert (
            f.read().split("\n")[8]
            == 'extend-exclude = "awesome_pkg/__init__.py"'
        )

    with open("./README.md") as f:
        assert f.read().split("\n")[0] == "# awesome_pkg"

    with open("./setup.py") as f:
        data = f.read().split("\n")
        assert (
            data[4]
            == '        "awesome_pkg only supports Python versions 3.6.0 or greater.",'
        )
        assert (
            data[18]
            == 'with open("awesome_pkg/__init__.py", mode="r", encoding="utf-8") as f:'
        )

    with open("./awesome_pkg/__init__.py") as f:
        data = f.read().split("\n")
        assert data[0] == '__productname__ = "awesome_pkg"'
        assert data[1] == '__version__ = "0.1.0"'
        assert data[2] != '__description__ = "PROJECTDESCRIPTION"'
        assert data[3] != '__url__ = "PROJECTURL"'
        assert (
            data[4]
            == '__docs__ = "https://awesome_pkg.readthedocs.io/en/latest/"'
        )
        assert data[5] != '__author__ = "PROJECTAUTHOR"'
        assert data[6] != '__author_email__ = "PROJECTAUTHOREMAIL"'
        assert data[7] != '__license__ = "PROJECTLICENSE"'
        assert data[8] != '__bugtracker__ = "PROJECTURL/issues"'
