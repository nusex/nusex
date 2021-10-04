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

import logging
import re
from pathlib import Path

from nusex import Template


def test_create_template():
    template = Template("__test_template__")
    assert template.name == "__test_template__"
    assert template.data["files"] == {}
    assert template.data["installs"] == []
    assert template.data["as_extension_for"] == ""

    template.save()
    assert template.exists


def test_build_okay():
    template = Template.from_dir(
        "__test_build__", Path(__file__).parent / "data/testarosa"
    )
    assert template.name == "__test_build__"
    assert len(template.data["files"].keys()) == 21

    template.save()
    assert template.exists


def test_init_file_okay():
    template = Template("__test_build__")
    assert "PROJECTNAME/__init__.py" in template.data["files"]

    lines = re.split(
        "\r\n|[\r\n]",
        template.data["files"]["PROJECTNAME/__init__.py"].decode(),
    )
    assert lines[0] == '__productname__ = "PROJECTNAME"'
    assert lines[1] == '__version__ = "PROJECTVERSION"'
    assert lines[2] == '__description__ = "PROJECTDESCRIPTION"'
    assert lines[3] == '__url__ = "PROJECTURL"'
    assert (
        lines[4] == '__docs__ = "https://PROJECTNAME.readthedocs.io/en/latest"'
    )
    assert lines[5] == '__author__ = "PROJECTAUTHOR"'
    assert lines[6] == '__author_email__ = "PROJECTAUTHOREMAIL"'
    assert lines[7] == '__license__ = "PROJECTLICENSE"'
    assert lines[8] == '__bugtracker__ = "PROJECTURL/issues"'
    assert lines[9] == '__ci__ = "PROJECTURL/actions"'


def test_pyproject_file_okay():
    template = Template("__test_build__")
    assert "pyproject.toml" in template.data["files"]

    lines = re.split(
        "\r\n|[\r\n]", template.data["files"]["pyproject.toml"].decode()
    )
    assert lines[1] == 'name = "PROJECTNAME"'
    assert lines[2] == 'version = "PROJECTVERSION"'
    assert lines[3] == 'description = "PROJECTDESCRIPTION"'
    assert lines[4] == 'license = "PROJECTLICENSE"'
    assert lines[5] == 'authors = ["PROJECTAUTHOR <PROJECTAUTHOREMAIL>"]'
    assert lines[6] == 'maintainers = ["PROJECTAUTHOR <PROJECTAUTHOREMAIL>"]'
    assert lines[7] == 'homepage = "PROJECTURL"'
    assert lines[8] == 'repository = "PROJECTURL"'
    assert (
        lines[9]
        == 'documentation = "https://PROJECTNAME.readthedocs.io/en/latest"'
    )
    assert lines[12] == 'extend-exclude = "PROJECTNAME/__init__.py"'


def test_sphinx_conf_files_okay():
    template = Template("__test_build__")

    for file in ("docs/conf.py", "docs/source/conf.py"):
        logging.info(f"File: {file}")
        assert file in template.data["files"]

        lines = re.split("\r\n|[\r\n]", template.data["files"][file].decode())
        assert lines[15] == "import PROJECTNAME"
        assert lines[22] == 'project = "PROJECTNAME"'
        assert lines[23] == 'copyright = "PROJECTYEAR, PROJECTAUTHOR"'
        assert lines[24] == 'author = "PROJECTAUTHOR"'
        assert lines[27] == "release = PROJECTNAME.__version__"


def test_error_files_okay():
    template = Template("__test_build__")

    for file in ("PROJECTNAME/error.py", "PROJECTNAME/errors.py"):
        logging.info(f"File: {file}")
        assert file in template.data["files"]

        lines = re.split("\r\n|[\r\n]", template.data["files"][file].decode())
        assert lines[0] == "class PROJECTBASEEXC(Exception):"
        assert lines[4] == "class AnotherError(PROJECTBASEEXC):"


def test_manifest_file_okay():
    template = Template("__test_build__")
    assert "MANIFEST.in" in template.data["files"]

    lines = re.split(
        "\r\n|[\r\n]", template.data["files"]["MANIFEST.in"].decode()
    )
    assert lines[0] == "graft PROJECTNAME"


def test_setup_cfg_file_okay():
    template = Template("__test_build__")
    assert "setup.cfg" in template.data["files"]

    lines = re.split(
        "\r\n|[\r\n]", template.data["files"]["setup.cfg"].decode()
    )
    assert lines[1] == "name = PROJECTNAME"


def test_setup_py_file_okay():
    template = Template("__test_build__")
    assert "setup.py" in template.data["files"]

    lines = re.split(
        "\r\n|[\r\n]", template.data["files"]["setup.py"].decode()
    )
    assert lines[3] == '    name="PROJECTNAME",'


def test_readme_md_file_okay():
    template = Template("__test_build__")
    assert "README.md" in template.data["files"]

    lines = re.split(
        "\r\n|[\r\n]", template.data["files"]["README.md"].decode()
    )
    assert lines[0] == "# PROJECTNAME"
    assert lines[4] == "## Acknowledgements"
    assert lines[6] == (
        "This project was created in part by the [nusex project templating "
        "utility](https://github.com/nusex/nusex)."
    )


def test_readme_txt_file_okay():
    template = Template("__test_build__")
    assert "README.txt" in template.data["files"]

    lines = re.split(
        "\r\n|[\r\n]", template.data["files"]["README.txt"].decode()
    )
    assert lines[0] == "# PROJECTNAME"
    assert lines[10] == "### Acknowledgements"
    assert lines[14] == (
        "This project was created in part by the [nusex project templating "
        "utility](https://github.com/nusex/nusex)."
    )


def test_license_file_okay():
    template = Template("__test_build__")
    assert "LICENSE" in template.data["files"]

    lines = re.split("\r\n|[\r\n]", template.data["files"]["LICENSE"].decode())
    assert lines[0] == "LICENSEBODY"


def test_ignore_extensions():
    template = Template.from_dir(
        "__test_ignore_ext__",
        Path(__file__).parent / "data/testarosa",
        ignore_exts={"lol", "rofl"},
    )
    assert template.name == "__test_ignore_ext__"
    assert len(template.data["files"].keys()) == 19


def test_ignore_directories():
    template = Template.from_dir(
        "__test_ignore_dir__",
        Path(__file__).parent / "data/testarosa",
        ignore_dirs={"ignorethisdir"},
    )
    assert template.name == "__test_ignore_dir__"
    assert len(template.data["files"].keys()) == 19


def test_ignore_wildmatch_directories():
    template = Template.from_dir(
        "__test_ignore_w_dir__",
        Path(__file__).parent / "data/testarosa",
        ignore_dirs={"*setup"},
    )
    assert template.name == "__test_ignore_w_dir__"
    assert len(template.data["files"].keys()) == 17
