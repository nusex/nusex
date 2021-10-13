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
import json
import os
import sys
from pathlib import Path
from platform import python_implementation

from nusex import TEMP_DIR, TEMPLATE_DIR, Profile
from nusex.blueprints import PythonBlueprint
from nusex.constants import LICENSE_DIR
from nusex.errors import BuildError, IncompatibilityError, TemplateError
from nusex.helpers import run, validate_name
from nusex.spec import NSXSpecIO

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
    """

    __slots__ = ("path", "data", "_installs")

    def __init__(self, name, *, installs=[]):
        self.path = TEMPLATE_DIR / f"{name}.nsx"
        self._installs = installs

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
        """Create a new template. This should never need to be
        called as templates are created automatically when necessary
        upon object instantiation.

        Args:
            name (str): The name of the template.

        Raises:
            TemplateError: The provided name is invalid.
            AlreadyExists: The template already exists on disk.
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
        object instantiation.

        Raises:
            FileNotFoundError: The template does not exist on disk.
        """
        self.data = NSXSpecIO().read(self.path)

    def save(self):
        """Save this profile.

        Raises:
            TemplateError: The profile data has been improperly
                modified.
        """
        try:
            NSXSpecIO().write(self.path, self.data)
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
    def from_cwd(
        cls, name, *, installs=[], ignore_exts=set(), ignore_dirs=set()
    ):
        """Create a template using files from the current working
        directory.

        Args:
            name (str): The name of the template.

        Keyword Args:
            installs (list[str]): A list of dependencies to install when
                this template is deployed. Defaults to an empty list.
            ignore_exts (set[str]): A set of file extensions to ignore.
                Defaults to an empty set.
            ignore_dirs (set[str]): A set of directories to ignore.
                Defaults to an empty set.

        Returns:
            Template: The newly created template.
        """
        c = cls(name, installs=installs)
        c.build(
            ignore_exts=ignore_exts,
            ignore_dirs=ignore_dirs,
        )
        return c

    @classmethod
    def from_dir(
        cls, name, path, *, installs=[], ignore_exts=set(), ignore_dirs=set()
    ):
        """Create a template using files from a specific directory.

        Args:
            name (str): The name of the template.
            path (str | os.PathLike): The path to the files to build the
                template with.

        Keyword Args:
            installs (list[str]): A list of dependencies to install when
                this template is deployed. Defaults to an empty list.
            ignore_exts (set[str]): A set of file extensions to ignore.
                Defaults to an empty set.
            ignore_dirs (set[str]): A set of directories to ignore.
                Defaults to an empty set.

        Returns:
            Template: The newly created template.
        """
        c = cls(name, installs=installs)
        c.build(
            root_dir=path,
            ignore_exts=ignore_exts,
            ignore_dirs=ignore_dirs,
        )
        return c

    @classmethod
    def from_repo(
        cls, name, url, *, installs=[], ignore_exts=set(), ignore_dirs=set()
    ):
        """Create a template using files from a GitHub repository.

        Args:
            name (str): The name of the template.
            url (str): The URL of the GitHub repository to clone.

        Keyword Args:
            installs (list[str]): A list of dependencies to install when
                this template is deployed. Defaults to an empty list.
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
            name,
            installs=installs,
            ignore_exts=ignore_exts,
            ignore_dirs=ignore_dirs,
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
        data = {
            "files": {resolve_key(f): f.read_bytes() for f in files},
            "installs": self._installs,
            "as_extension_for": "",
        }

        blueprint = PythonBlueprint(project_name, data)
        self.data = blueprint().data

    def deploy(self, path="."):
        """Deploy this template.

        Keyword Args:
            path (str): The path to deploy this template to. Defaults to
                the current directory.
        """

        def resolve_version(key):
            if key != "CALVER":
                return key

            return dt.date.today().strftime("%Y.%m.%d")

        def resolve_license_info(key):
            with open(LICENSE_DIR / f"{key}.txt", encoding="utf-8") as f:
                lines = f.read().split("\n")

            start = [i for i, line in enumerate(lines) if line == "---"][
                -1
            ] + 2

            return (
                lines[1][7:],
                "\n".join(lines[start:])
                .replace("[year]", f"{dt.date.today().year}")
                .replace("[fullname]", profile["author_name"]),
            )

        profile = Profile.current()
        project_name = Path(path).resolve().parts[-1]
        lic_name, lic_body = resolve_license_info(profile["preferred_license"])
        project_error = project_name.replace("_", " ").title().replace(" ", "")

        var_mapping = {
            b"PROJECTNAME": project_name,
            b"PROJECTVERSION": resolve_version(profile["starting_version"]),
            b"PROJECTDESCRIPTION": profile["default_description"],
            b"PROJECTURL": f"{profile['git_profile_url']}/{project_name}",
            b"PROJECTAUTHOREMAIL": profile["author_email"],
            b"PROJECTAUTHOR": profile["author_name"],
            b"PROJECTLICENSE": lic_name,
            b"LICENSEBODY": lic_body,
            b"PROJECTYEAR": f"{dt.date.today().year}",
            b"PROJECTBASEEXC": f"{project_error}Error",
        }

        for name, data in self.data["files"].items():
            name = name.replace(
                "PROJECTNAME",
                project_name.lower().replace(" ", "_").replace("-", "_"),
            )

            dirs = name.split("/")[:-1]
            if dirs:
                os.makedirs(f"{path}/" + "/".join(dirs), exist_ok=True)

            for k, v in var_mapping.items():
                data = data.replace(k, v.encode())

            with open(f"{path}/{name}", "wb") as f:
                f.write(data)

        meta = {
            "template": self.name,
            "files": list(self.data["files"].keys()),
        }
        with open(f"{path}/.nusexmeta", "w") as f:
            json.dump(meta, f)

    def install_dependencies(self):
        """Install this template's dependencies. Note that this does not
        work on PyPy Python implementations."""
        if python_implementation() == "PyPy":
            raise IncompatibilityError(
                "Dependency installation is not supported on PyPy "
                "implementations"
            )

        if not self.data["installs"]:
            return

        run(
            f"{sys.executable} -m pip install "
            + " ".join(self.data["installs"])
        )

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
