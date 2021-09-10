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

import os
from pathlib import Path

from nusex import TEMP_DIR, TEMPLATE_DIR, __url__
from nusex.errors import BuildError
from nusex.helpers import run, validate_name
from nusex.spec import NSXDecoder, NSXEncoder

from .base import Entity

SPECIAL_FILES = (
    "MANIFEST.in",
    "pyproject.toml",
    "README.md",
    "setup.py",
    "LICENSE",
    "PROJECTNAME/__init__.py",
)
INIT_ATTR_MAPPING = {
    "__productname__": '"PROJECTNAME"',
    "__version__": '"PROJECTVERSION"',
    "__description__": '"PROJECTDESCRIPTION"',
    "__url__": '"PROJECTURL"',
    "__docs__": '"https://PROJECTNAME.readthedocs.io/en/latest/"',
    "__author__": '"PROJECTAUTHOR"',
    "__author_email__": '"PROJECTAUTHOREMAIL"',
    "__license__": '"PROJECTLICENSE"',
    "__bugtracker__": '"PROJECTURL/issues"',
}
DOCS_ATTR_MAPPING = {
    "project": '"PROJECTNAME"',
    "copyright": '"PROJECTYEAR, PROJECTAUTHOR"',
    "author": '"PROJECTAUTHOR"',
    "release": "PROJECTNAME.__version__",
}
ATTRS = (
    "PROJECTNAME",
    "PROJECTAUTHOR",
    "PROJECTAUTHOREMAIL",
    "PROJECTURL",
    "PROJECTVERSION",
    "PROJECTDESCRIPTION",
    "PROJECTLICENSE",
    "PROJECTYEAR",
    "LICENSEBODY",
)
DEFAULT_EXCLUDE_DIRS = (
    r"(\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|venv|\.svn"
    r"|_build|buck-out|build|dist)"
)
DEFAULT_EXCLUDE_EXTS = r"(py[cod])"


class Template(Entity):
    __slots__ = Entity.__slots__ + ("installs", "as_extension_for")

    def __init__(self, name, *, installs=[], as_extension_for=""):
        super().__init__(TEMPLATE_DIR, name, "nsx")
        self.installs = installs
        self.as_extension_for = as_extension_for

    def __getitem__(self, key):
        return self.data["files"][key]

    def create_new(self, name):
        validate_name(name, self.__class__.__name__)
        self.data = {
            "files": {},
            "installs": [],
            "as_extension_for": "",
        }

    def load(self):
        self.data = NSXDecoder().read(self.path)

    def save(self):
        NSXEncoder().write(self.path, self.data)

    @classmethod
    def from_cwd(cls, name, ignores):
        c = cls(name)
        c.build(Path(".").resolve().parts[-1], ignores=ignores)
        return c

    @classmethod
    def from_dir(cls, name, path, ignores):
        cur_path = Path(".").resolve()
        os.chdir(path)
        c = cls.from_cwd(name)
        os.chdir(cur_path)
        return c

    @classmethod
    def from_repo(cls, name, url, ignores):
        os.makedirs(TEMP_DIR, exist_ok=True)
        os.chdir(TEMP_DIR)

        output = run(f"git clone {url}")
        if output.returncode == 1:
            raise BuildError(
                "Cloning the repo failed. Is Git installed? Is the URL "
                "correct?"
            )

        os.chdir(TEMP_DIR / url.split("/")[-1].replace(".git", ""))
        return cls.from_cwd(name)

    def get_file_listing(self, ignores):
        def is_valid(path):
            return (
                path.is_file()
                and all(i not in path.parts for i in true_dir_ignores)
                and all(i[1:] not in f"{path}" for i in wild_dir_ignores)
                and all(i != path.suffix[1:] for i in ignores["exts"])
            )

        wild_dir_ignores = set(
            filter(lambda x: x.startswith("*"), ignores["dirs"])
        )
        true_dir_ignores = ignores["dirs"] - wild_dir_ignores
        files = filter(lambda p: is_valid(p), Path(".").rglob("*"))
        return list(files)

    def build(self, project_name, files=[], **kwargs):
        def get_file_text(key):
            b = self.data["files"].get(key, None)

            if not b:
                return None

            return b.decode()

        def set_file_text(key, value):
            self.data["files"][key] = value.encode()

        if not files:
            ignores = kwargs.pop("ignores", {"exts": set(), "dirs": set()})
            files = self.get_file_listing(ignores)

        self.data = {
            "files": {
                f"{f}".replace(project_name, "PROJECTNAME"): f.read_bytes()
                for f in files
            },
            "installs": self.installs,
            "extension_for": self.as_extension_for,
        }

        # Handle __init__ file if present.
        init_text = get_file_text("PROJECTNAME/__init__.py")

        if init_text:
            lines = init_text.split("\n")

            for i, line in enumerate(lines[:]):
                # Modify dunder variables.
                if line.startswith("__"):
                    k, v = line.split(" = ")
                    v = v.strip('"').strip("'")
                    new_v = INIT_ATTR_MAPPING.get(k, v)
                    lines[i] = f"{k} = {new_v}"

            set_file_text("PROJECTNAME/__init__.py", "\n".join(lines))

        # Handle sphinx conf file if present.
        for sf in ("docs/conf.py", "docs/source/conf.py"):
            docs_text = get_file_text(sf)

            if docs_text:
                lines = docs_text.split("\n")
                in_project_info = False

                for i, line in enumerate(lines[:]):
                    # Modify data variables.
                    if in_project_info:
                        if line.startswith("# --"):
                            in_project_info = False
                            continue

                        if not line or line.startswith("#"):
                            continue

                        k, v = line.split(" = ")
                        v = v.strip('"').strip("'")
                        new_v = DOCS_ATTR_MAPPING.get(k, v)
                        lines[i] = f"{k} = {new_v}"

                    elif line.startswith("# -- Project information"):
                        in_project_info = True

                    elif line.strip() == f"import {project_name}":
                        lines[i] = "import PROJECTNAME"

                set_file_text(sf, "\n".join(lines))

        # These four files need the same changes.
        for sf in ("MANIFEST.in", "pyproject.toml", "setup.py"):
            text = get_file_text(sf)
            if text:
                set_file_text(sf, text.replace(project_name, "PROJECTNAME"))

        # README needs to be handled separately.
        readme_text = get_file_text("README.md")

        if readme_text:
            lines = readme_text.split("\n")
            last_line = len(lines) - 1
            found_acks = False
            ack = (
                "This project was created in part by the [nusex project "
                f"templating utility]({__url__})."
            )

            for i, line in enumerate(lines[:]):
                if line.startswith("#"):
                    if found_acks:
                        lines.insert(i, ack)
                        lines.insert(i + 1, "")
                        break

                    if "acknowledgements" in line.lower():
                        found_acks = True

                elif i == last_line and found_acks:
                    lines.extend([ack, ""])

            if not found_acks:
                lines.extend(["## Acknowledgements", "", ack, ""])

            set_file_text(
                "README.md",
                "\n".join(lines).replace(project_name, "PROJECTNAME"),
            )

        # LICENSE also needs to be handles separately.
        if "LICENSE" in self.data["files"].keys():
            set_file_text("LICENSE", "LICENSEBODY")

    def check(self):
        manifest = {}

        for file, data in self.data["files"].items():
            manifest.update({file: []})

            try:
                for i, line in enumerate(data.decode().split("\n")):
                    if any(a in line for a in ATTRS):
                        manifest[file].append((i + 1, line))
            except UnicodeDecodeError:
                # If it errors here, no modifications could have been
                # made.
                ...

        return manifest
