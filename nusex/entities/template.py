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

from nusex import TEMP_DIR, TEMPLATE_DIR
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
    def from_cwd(cls, name):
        c = cls(name)
        c.build(Path(".").resolve().parts[-1])
        return c

    @classmethod
    def from_dir(cls, name, path):
        cur_path = Path(".").resolve()
        os.chdir(path)
        c = cls.from_cwd(name)
        os.chdir(cur_path)
        return c

    @classmethod
    def from_repo(cls, name, url):
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

    def get_file_listing(self):
        # TODO: Do ignore stuff.
        # Look up pathspec wildmatch.
        files = filter(lambda p: p.is_file(), Path(".").rglob("*"))
        return list(files)

    def build(self, project_name, files=[]):
        def get_file_text(key):
            b = self.data["files"].get(key, None)

            if not b:
                return None

            return b.decode()

        def set_file_text(key, value):
            # Return True is key was written to (if it exists).
            if not self.data["files"].get(key, None):
                return False

            self.data["files"][key] = value.encode()
            return True

        if not files:
            files = self.get_file_listing()

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
            in_project_info = False

            if docs_text:
                lines = docs_text.split("\n")

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
        for sf in ("MANIFEST.in", "pyproject.toml", "README.md", "setup.py"):
            text = get_file_text(sf)
            if text:
                set_file_text(sf, text.replace(project_name, "PROJECTNAME"))

        # LICENSE needs to be handles separately.
        set_file_text("LICENSE", "LICENSEBODY")
