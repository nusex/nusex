# Copyright (c) 2021, Ethan Henderson
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import datetime as dt
import logging
import os
import shutil
import typing as t
from pathlib import Path
from platform import python_implementation

import pytest  # type: ignore

from nusex import Profile, Template
from nusex.constants import CONFIG_DIR, LICENSE_DIR

DEPLOY_DIR = Path(__file__).parent / "my_app"


def test_deploy_okay():
    os.makedirs(DEPLOY_DIR, exist_ok=True)

    template = Template.from_dir(
        "__test_deploy__",
        Path(__file__).parent / "data/testarosa_py",
        installs=["analytix", "sqlite2pg"],
    )
    template.save()

    template.deploy(destination=DEPLOY_DIR)
    assert os.path.isfile(DEPLOY_DIR / "docs/source/conf.py")
    assert os.path.isfile(DEPLOY_DIR / "docs/conf.py")
    assert os.path.isfile(DEPLOY_DIR / "ignorethisdir/goodbye.everyone")
    assert os.path.isfile(DEPLOY_DIR / "ignorethisdir/hello.world")
    assert os.path.isfile(DEPLOY_DIR / "setup/config.1")
    assert os.path.isfile(DEPLOY_DIR / "setup/token.0")
    assert os.path.isfile(DEPLOY_DIR / "my_app/__init__.py")
    assert os.path.isfile(DEPLOY_DIR / "my_app/error.py")
    assert os.path.isfile(DEPLOY_DIR / "my_app/errors.py")
    assert os.path.isfile(DEPLOY_DIR / "COPYING")
    assert os.path.isfile(DEPLOY_DIR / "COPYING.txt")
    assert os.path.isfile(DEPLOY_DIR / "ignoreme_too.rofl")
    assert os.path.isfile(DEPLOY_DIR / "ignoreme.lol")
    assert os.path.isfile(DEPLOY_DIR / "LICENSE")
    assert os.path.isfile(DEPLOY_DIR / "LICENSE.txt")
    assert os.path.isfile(DEPLOY_DIR / "MANIFEST.in")
    assert os.path.isfile(DEPLOY_DIR / "pyproject.toml")
    assert os.path.isfile(DEPLOY_DIR / "README.md")
    assert os.path.isfile(DEPLOY_DIR / "README.txt")
    assert os.path.isfile(DEPLOY_DIR / "setup.cfg")
    assert os.path.isfile(DEPLOY_DIR / "setup.py")
    assert os.path.isfile(DEPLOY_DIR / ".nusexmeta")


def test_init_file_okay():
    profile = Profile.current()

    with open(DEPLOY_DIR / "my_app/__init__.py", "r") as f:
        lines = f.read().split("\n")

    with open(
        CONFIG_DIR / f"licenses/{profile['preferred_license']}.txt"
    ) as f:
        lic_name = f.read().split("\n")[1][7:]

    assert lines[0] == '__productname__ = "my_app"'
    assert lines[1] == f'__version__ = "{profile["starting_version"]}"'
    assert lines[2] == f'__description__ = "{profile["default_description"]}"'
    assert lines[3] == f'__url__ = "{profile["git_profile_url"]}/my_app"'
    assert lines[4] == '__docs__ = "https://my_app.readthedocs.io/en/latest"'
    assert lines[5] == f'__author__ = "{profile["author_name"]}"'
    assert lines[6] == f'__author_email__ = "{profile["author_email"]}"'
    assert lines[7] == f'__license__ = "{lic_name}"'
    assert (
        lines[8]
        == f'__bugtracker__ = "{profile["git_profile_url"]}/my_app/issues"'
    )
    assert (
        lines[9] == f'__ci__ = "{profile["git_profile_url"]}/my_app/actions"'
    )


def test_pyproject_file_okay():
    profile = Profile.current()

    with open(DEPLOY_DIR / "pyproject.toml", "r") as f:
        lines = f.read().split("\n")

    with open(LICENSE_DIR / f"{profile['preferred_license']}.txt") as f:
        lic_name = f.read().split("\n")[1][7:]

    assert lines[1] == 'name = "my_app"'
    assert lines[2] == f'version = "{profile["starting_version"]}"'
    assert lines[3] == f'description = "{profile["default_description"]}"'
    assert lines[4] == f'license = "{lic_name}"'
    assert lines[5] == (
        f'authors = ["{profile["author_name"]} '
        f'<{profile["author_email"]}>"]'
    )
    assert lines[6] == (
        f'maintainers = ["{profile["author_name"]} '
        f'<{profile["author_email"]}>"]'
    )
    assert lines[7] == f'homepage = "{profile["git_profile_url"]}/my_app"'
    assert lines[8] == f'repository = "{profile["git_profile_url"]}/my_app"'
    assert (
        lines[9] == 'documentation = "https://my_app.readthedocs.io/en/latest"'
    )
    assert lines[12] == 'extend-exclude = "my_app/__init__.py"'


def test_sphinx_conf_files_okay():
    profile = Profile.current()

    for file in ("docs/conf.py", "docs/source/conf.py"):
        logging.info(f"File: {file}")

        with open(DEPLOY_DIR / file, "r") as f:
            lines = f.read().split("\n")

        assert lines[15] == "import my_app"
        assert lines[22] == 'project = "my_app"'
        assert lines[23] == (
            f'copyright = "{dt.date.today().year}, '
            f'{profile["author_name"]}"'
        )
        assert lines[24] == f'author = "{profile["author_name"]}"'
        assert lines[27] == "release = my_app.__version__"


def test_error_files_okay():
    for file in ("my_app/error.py", "my_app/errors.py"):
        logging.info(f"File: {file}")

        with open(DEPLOY_DIR / file, "r") as f:
            lines = f.read().split("\n")

        assert lines[0] == "class MyAppError(Exception):"
        assert lines[4] == "class AnotherError(MyAppError):"


def test_manifest_file_okay():
    with open(DEPLOY_DIR / "MANIFEST.in", "r") as f:
        lines = f.read().split("\n")

    assert lines[0] == "graft my_app"


def test_setup_cfg_file_okay():
    with open(DEPLOY_DIR / "setup.cfg", "r") as f:
        lines = f.read().split("\n")

    assert lines[1] == "name = my_app"


def test_setup_py_file_okay():
    with open(DEPLOY_DIR / "setup.py", "r") as f:
        lines = f.read().split("\n")

    assert lines[3] == '    name="my_app",'


def test_readme_md_file_okay():
    with open(DEPLOY_DIR / "README.md", "r") as f:
        lines = f.read().split("\n")

    assert lines[0] == "# my_app"
    assert lines[4] == "## Acknowledgements"
    assert lines[6] == (
        "This project was created in part by the [nusex project templating "
        "utility](https://github.com/nusex/nusex)."
    )


def test_readme_txt_file_okay():
    with open(DEPLOY_DIR / "README.txt", "r") as f:
        lines = f.read().split("\n")

    assert lines[0] == "# my_app"
    assert lines[10] == "### Acknowledgements"
    assert lines[14] == (
        "This project was created in part by the [nusex project templating "
        "utility](https://github.com/nusex/nusex)."
    )


def test_license_file_okay():
    profile = Profile.current()

    with open(LICENSE_DIR / f"{profile['preferred_license']}.txt") as f:
        lines = f.read().split("\n")

        header = [i for i, line in enumerate(lines) if line == "---"][-1] + 2
        header = lines[header]

    for file in ("LICENSE", "COPYING", "LICENSE.txt", "COPYING.txt"):
        logging.info(f"File: {file}")

        with open(DEPLOY_DIR / file, "r") as f:
            lines = f.read().split("\n")

        assert lines[0] == header


@t.no_type_check
@pytest.mark.skipif(
    python_implementation() == "PyPy",
    reason="Dependency installs do not work with PyPy",
)
def test_installs_okay():
    template = Template("__test_deploy__")
    assert template.data["installs"] == ["analytix", "sqlite2pg"]
    template.install_dependencies()

    import analytix  # noqa: F401
    import sqlite2pg  # noqa: F401


def test_clean_up():
    shutil.rmtree(Path(__file__).parent / "my_app")
