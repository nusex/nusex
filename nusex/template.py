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
from nusex.errors import BuildError, TemplateError
from nusex.helpers import run, validate_name
from nusex.spec import NSXDecoder, NSXEncoder

INIT_ATTR_MAPPING = {
    "__productname__": '"PROJECTNAME"',
    "__version__": '"PROJECTVERSION"',
    "__description__": '"PROJECTDESCRIPTION"',
    "__url__": '"PROJECTURL"',
    "__docs__": '"https://PROJECTNAME.readthedocs.io/en/latest"',
    "__author__": '"PROJECTAUTHOR"',
    "__author_email__": '"PROJECTAUTHOREMAIL"',
    "__license__": '"PROJECTLICENSE"',
    "__bugtracker__": '"PROJECTURL/issues"',
    "__ci__": '"PROJECTURL/actions"',
}
PYPROJECT_ATTR_MAPPING = {
    "name": '"PROJECTNAME"',
    "version": '"PROJECTVERSION"',
    "description": '"PROJECTDESCRIPTION"',
    "license": '"PROJECTLICENSE"',
    "authors": '["PROJECTAUTHOR <PROJECTAUTHOREMAIL>"]',
    "maintainers": '["PROJECTAUTHOR <PROJECTAUTHOREMAIL>"]',
    "homepage": '"PROJECTURL"',
    "repository": '"PROJECTURL"',
    "documentation": '"https://PROJECTNAME.readthedocs.io/en/latest"',
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
    "PROJECTBASEEXC",
)


class Template:
    """A class in which to create, load, modify, and save templates.

    Args:
        name (str): The name of the template. If the template does not
            exist, a new one is created, otherwise an existing one is
            loaded.

    Keyword Args:
        installs (list[str]): A list of dependancies to be installed
            when the template is deployed.

    Attributes:
        path (pathlib.Path): The complete filepath to the template.
        data (dict[str, Any]): The data for the template.
        installs (list[str]): A list of dependencies the template will
            install when deployed.
    """

    __slots__ = ("path", "data", "installs")

    def __init__(self, name, *, installs=[]):
        self.path = TEMPLATE_DIR / f"{name}.nsx"
        self.installs = installs

        if not os.path.isfile(self.path):
            return self.create_new(name)

        self.load()

    def __str__(self):
        return self.path.stem

    def __repr__(self):
        return (
            f"<Template name={self.name!r} files={len(self.data['files'])!r}>"
        )

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __getitem__(self, key):
        return self.data["files"][key]

    @property
    def name(self):
        """The name of the template.

        Returns:
            str
        """
        return self.path.stem

    @property
    def exists(self):
        """Whether the template exists on disk.

        Returns:
            bool
        """
        return self.path.is_file()

    def create_new(self, name):
        """Create a new template.

        Args:
            name (str): The name of the template.
        """
        validate_name(name, self.__class__.__name__)
        self.data = {
            "files": {},
            "installs": [],
            "as_extension_for": "",
        }

    def load(self):
        """Load an existing template. This should never need to be
        called as templates are loaded automatically when necessary upon
        object creation.

        Raises:
            FileNotFoundError: The template does not exist on disk.
        """
        self.data = NSXDecoder().read(self.path)

    def save(self):
        """Save this profile.

        Raises:
            TemplateError: The profile data has been improperly
                modified.
        """
        try:
            NSXEncoder().write(self.path, self.data)
        except KeyError:
            raise TemplateError(
                "The template data has been improperly modified"
            ) from None

    def delete(self):
        """Delete this template.

        Raises:
            FileNotFoundError: The template does not exist on disk.
        """
        os.remove(self.path)

    def rename(self, new_name):
        """Rename this template.

        Args:
            new_name (str): The new name for the template.

        Raises:
            FileNotFoundError: The template does not exist on disk.
        """
        new_path = f"{self.path}".replace(self.path.stem, new_name)
        self.path = self.path.rename(new_path)

    @classmethod
    def from_cwd(cls, name, *, ignore_exts=set(), ignore_dirs=set()):
        """Create a template using files from the current working
        directory.

        Args:
            name (str): The name of the template.

        Keyword Args:
            ignore_exts (set[str]): A set of file extensions to ignore.
                Defaults to an empty set.
            ignore_dirs (set[str]): A set of directories to ignore.
                Defaults to an empty set.

        Returns:
            Template: The newly created template.
        """
        c = cls(name)
        c.build(
            ignore_exts=ignore_exts,
            ignore_dirs=ignore_dirs,
        )
        return c

    @classmethod
    def from_dir(cls, name, path, *, ignore_exts=set(), ignore_dirs=set()):
        """Create a template using files from a specific directory.

        Args:
            name (str): The name of the template.
            path (str | os.PathLike): The path to the files to build the
                template with.

        Keyword Args:
            ignore_exts (set[str]): A set of file extensions to ignore.
                Defaults to an empty set.
            ignore_dirs (set[str]): A set of directories to ignore.
                Defaults to an empty set.

        Returns:
            Template: The newly created template.
        """
        c = cls(name)
        c.build(
            root_dir=path,
            ignore_exts=ignore_exts,
            ignore_dirs=ignore_dirs,
        )
        return c

    @classmethod
    def from_repo(cls, name, url, *, ignore_exts=set(), ignore_dirs=set()):
        """Create a template using files from a GitHub repository.

        Args:
            name (str): The name of the template.
            url (str): The URL of the GitHub repository to clone.

        Keyword Args:n
            ignore_exts (set[str]): A set of file extensions to ignore.
                Defaults to an empty set.
            ignore_dirs (set[str]): A set of directories to ignore.
                Defaults to an empty set.

        Returns:
            Template: The newly created template.

        Raises:
            BuildError: Cloning the repository failed.
        """
        os.makedirs(TEMP_DIR, exist_ok=True)
        os.chdir(TEMP_DIR)

        output = run(f"git clone {url}")
        if output.returncode == 1:
            raise BuildError(
                "Cloning the repo failed. Is Git installed? Is the URL "
                "correct?"
            )

        os.chdir(TEMP_DIR / url.split("/")[-1].replace(".git", ""))
        return cls.from_cwd(
            name, ignore_exts=ignore_exts, ignore_dirs=ignore_dirs
        )

    def get_file_listing(
        self, root_dir, *, ignore_exts=set(), ignore_dirs=set()
    ):
        """Get a list of files to include in this template.

        Args:
            root_dir (str): The root directory that nusex will search
                from.

        Keyword Args:
            ignore_exts (set[str]): A set of file extensions to ignore.
                Defaults to an empty set.
            ignore_dirs (set[str]): A set of directories to ignore.
                Defaults to an empty set.

        Returns:
            list[Path]: A list of filepaths.
        """

        def is_valid(path):
            return (
                path.is_file()
                and all(i not in path.parts for i in true_dir_ignores)
                and all(i[1:] not in f"{path}" for i in wild_dir_ignores)
                and all(i != path.suffix[1:] for i in ignore_exts)
            )

        wild_dir_ignores = set(
            filter(lambda x: x.startswith("*"), ignore_dirs)
        )
        true_dir_ignores = ignore_dirs - wild_dir_ignores
        files = filter(lambda p: is_valid(p), Path(root_dir).rglob("*"))
        return list(files)

    def build(self, project_name=None, files=[], root_dir=".", **kwargs):
        """Build this template. View the
        :doc:`template guide <../guide/templates>` to see what this
        command does in more detail.

        Keyword Args:
            project_name (str): The name of the project. If this is None
                the project name is set to the name of the parent
                folder. Defaults to None.
            files (list[str]): The list of files to include in this
                template. If no files are specified, the file listing
                is automatically retrieved.
            root_dir (str): The root directory that nusex will search
                from. Defaults to the current directory.
            **kwargs (Any): Arguments for the :code:`get_file_listing`
                method.
        """

        def get_file_text(key):
            b = self.data["files"].get(key, None)

            if not b:
                return None

            return b.decode()

        def set_file_text(key, value):
            self.data["files"][key] = value.encode()

        def resolve_key(path):
            path = "/".join(f"{path.resolve()}".split(os.sep)[nparts:])
            return path.replace(project_name, "PROJECTNAME")

        if not project_name:
            project_name = Path(root_dir).resolve().parts[-1]

        if not files:
            files = self.get_file_listing(
                root_dir,
                ignore_exts=kwargs.pop("ignore_exts", set()),
                ignore_dirs=kwargs.pop("ignore_dirs", set()),
            )

        nparts = len(Path(root_dir).resolve().parts)
        self.data = {
            "files": {resolve_key(f): f.read_bytes() for f in files},
            "installs": self.installs,
            "as_extension_for": "",
        }

        # Handle __init__ file if present.
        text = get_file_text("PROJECTNAME/__init__.py")

        if text:
            lines = text.split("\n")

            for i, line in enumerate(lines[:]):
                # Modify dunder variables.
                if line.startswith("__"):
                    k, v = line.split(" = ")
                    v = v.strip('"').strip("'")
                    new_v = INIT_ATTR_MAPPING.get(k, v)
                    lines[i] = f"{k} = {new_v}"

            set_file_text("PROJECTNAME/__init__.py", "\n".join(lines))

        # Handle pyproject.toml file if present.
        text = get_file_text("pyproject.toml")

        if text:
            lines = text.split("\n")
            in_tool_poetry = False

            for i, line in enumerate(lines[:]):
                # Modify data variables.
                if in_tool_poetry:
                    if line.startswith("["):
                        in_tool_poetry = False
                        continue

                    try:
                        k, v = line.split(" = ")
                        v = v.strip('"').strip("'")
                        new_v = PYPROJECT_ATTR_MAPPING.get(k, v)
                        lines[i] = f"{k} = {new_v}"
                    except ValueError:
                        ...

                elif line.strip() == "[tool.poetry]":
                    in_tool_poetry = True

            set_file_text(
                "pyproject.toml",
                "\n".join(lines).replace(project_name, "PROJECTNAME"),
            )

        # Handle sphinx conf file if present.
        for sf in ("docs/conf.py", "docs/source/conf.py"):
            text = get_file_text(sf)

            if text:
                lines = text.split("\n")
                in_project_info = False

                for i, line in enumerate(lines[:]):
                    # Modify data variables.
                    if in_project_info:
                        if line.startswith("# --"):
                            in_project_info = False
                            continue

                        try:
                            k, v = line.split(" = ")
                            v = v.strip('"').strip("'")
                            new_v = DOCS_ATTR_MAPPING.get(k, v)
                            lines[i] = f"{k} = {new_v}"
                        except ValueError:
                            ...

                    elif line.startswith("# -- Project information"):
                        in_project_info = True

                    elif line.strip() == f"import {project_name}":
                        lines[i] = "import PROJECTNAME"

                set_file_text(sf, "\n".join(lines))

        # Handle the errors file, if present.
        for sf in ("PROJECTNAME/error.py", "PROJECTNAME/errors.py"):
            text = get_file_text(sf)

            if text:
                lines = text.split("\n")

                for i, line in enumerate(lines[:]):
                    if line.startswith("class"):
                        base_exc = line.split("(")[0][6:]
                        break

                set_file_text(sf, text.replace(base_exc, "PROJECTBASEEXC"))

        # These three files need the same changes.
        for sf in ("MANIFEST.in", "setup.cfg", "setup.py"):
            # TODO: Make the setup files more complete:
            # https://docs.python.org/3/distutils/setupscript.html
            text = get_file_text(sf)
            if text:
                set_file_text(sf, text.replace(project_name, "PROJECTNAME"))

        # README needs to be handled separately.
        for sf in ("README.md", "README.txt"):
            text = get_file_text(sf)

            if text:
                lines = text.split("\n")
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
                    sf,
                    "\n".join(lines).replace(project_name, "PROJECTNAME"),
                )

        # LICENSE (and others) also needs to be handles separately.
        for sf in ("LICENSE", "LICENSE.txt", "COPYING", "COPYING.txt"):
            if sf in self.data["files"].keys():
                set_file_text(sf, "LICENSEBODY")
                break

    def check(self):
        """Check the template manifest, including line changes.

        Returns:
            dict[str, list[tuple[int, str]]]: The template manifest. The
            keys are always file names, and the values are tuples
            of the line numbers and line values that have been changed.
            This may not always be present.
        """
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
