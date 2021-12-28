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

from __future__ import annotations

import datetime as dt
import logging
import os
import re
import typing as t
from pathlib import Path

from pathspec import PathSpec

import nusex
from nusex import checks
from nusex.api import blueprints
from nusex.api.data import TemplateData, TemplateIO
from nusex.errors import InvalidName, NotSupported, TemplateError

if t.TYPE_CHECKING:
    from nusex.api.profile import Profile

log = logging.getLogger(__name__)


class Template:
    """A class representing a template.

    Args:
        name (:obj:`str`):
            The name of the template.
    """

    __slots__ = ("name", "_path", "_data")

    def __init__(self, name: str) -> None:
        self.name = name
        self._path: Path | None = None
        self._data = TemplateData()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Template(name={self.name!r})"

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.name == other.name

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.name != other.name

    @classmethod
    def from_disk(cls, name: str, *, from_dir: Path | str) -> Template:
        """Load a saved template.

        Args:
            name (:obj:`str`):
                The name of the template to load.

        Keyword Args:
            from_dir (:obj:`pathlib.Path` | :obj:`str`):
                The directory to load the template from.

        Returns:
            :obj:`Template`:
                A template instance.
        """
        if not isinstance(from_dir, Path):
            from_dir = Path(from_dir)

        if not from_dir.is_dir():
            raise NotADirectoryError("Not a directory")

        path = from_dir / f"{name}.nsx"
        if not path.is_file():
            raise FileNotFoundError(
                f"No template named '{name}' exists in the given directory"
            )

        c = cls(name)
        with TemplateIO(path, "rb") as t:
            c._data = t.read()

        log.info(f"Template '{name}' loaded")
        log.log(nusex.TRACE, f"Manifest: {c._data.filenames}")
        c._path = path
        return c

    @property
    def path(self) -> Path | None:
        """The filepath to this template. This is :obj:`None` if the
        template has not been saved.

        Returns:
            :obj:`pathlib.Path`:
                The filepath to this template, or :obj:`None` if it has
                not been saved.
        """
        return self._path

    @property
    def files(self) -> dict[str, bytes]:
        """The files stored in this template. If there are none, this
        is an empty dict.

        Returns:
            :obj:`dict` [:obj:`str`, :obj:`bytes`]:
                This template's files, with the filename as the key, and
                the file's contents as the value.
        """
        return self._data.files

    @property
    def profile_data(self) -> dict[str, str | None]:
        """The profile data stored in this template. If there is none,
        this is an empty dict.

        .. warning::
            This returns the profile data, *not* a profile instance. To
            get a profile instance, use :obj:`Profile.from_template`.

        Returns:
            :obj:`dict` [:obj:`str`, :obj:`str`]:
                This template's profile data.
        """
        return self._data.profile_data

    @property
    def dependencies(self) -> list[str]:
        """The list of dependencies stored in this template. If there
        are none, this is an empty list.

        Returns:
            :obj:`list` [:obj:`str`]:
                This template's dependencies.
        """
        return self._data.dependencies

    @property
    def language(self) -> str | None:
        """The language this template is for, or :obj:`None` if it has
        not been set.

        Returns:
            :obj:`str`:
                The language this template is for, or :obj:`None` if it
                has not been set.
        """
        return self._data.language

    def _to_slug(self, text: str) -> str:
        return re.sub(
            "[^a-z0-9_]",
            "",
            re.sub("[- ]", "_", text.casefold()),
        )

    def _to_absolute_path(self, path: Path | str) -> Path:
        if not isinstance(path, Path):
            path = Path(path)

        if not path.is_dir():
            raise NotADirectoryError("Not a directory")

        if not path.is_absolute():
            path = path.resolve()

        return path

    def find_files(self, in_dir: Path | str) -> set[Path]:
        """Recursively search the given directory for files.

        Args:
            in_dir (:obj:`pathlib.Path` | :obj:`str`):
                The directory to search through.

        Returns:
            :obj:`set` [:obj:`pathlib.Path`]:
                The set of all files found.
        """
        log.debug("Searching for files")
        in_dir = self._to_absolute_path(in_dir)
        files = set(filter(lambda p: p.is_file(), in_dir.rglob("*")))
        log.info(f"Found {len(files):,} file(s)")
        return files

    def process_excludes(
        self,
        files: set[Path],
        *,
        use_defaults: bool = False,
        sources: list[Path | str] | None = None,
        patterns: list[str] | None = None,
    ) -> set[Path]:
        """Compile a series of files to exclude from all given sources
        and expressions.

        Args:
            files (:obj:`set` [:obj:`pathlib.Path`]):
                A list of files to compare against exclude patterns.
                This should generally be obtained through
                :obj:`find_files`.

        Keyword Args:
            use_defaults (:obj:`bool`):
                Whether to use the default set of exclude patterns
                employed by the command-line interface.
            sources \
            (:obj:`list` [:obj:`pathlib.Path` | :obj:`str`] \
            | :obj:`None`):
                A list of files containing glob exclude patterns.
            patterns (:obj:`list` [:obj:`str`]):
                A list of glob exclude patterns.

        Returns:
            :obj:`set` [:obj:`pathlib.Path`]:
                The files to exclude from the template.
        """
        log.debug("Processing exclude patterns")
        lines = ""

        if use_defaults:
            lines += "\n".join(nusex.DEFAULT_EXCLUDE_PATTERNS) + "\n"

        if patterns:
            lines += "\n".join(patterns) + "\n"

        for source in sources or []:
            if not isinstance(source, Path):
                source = Path(source)

            if not source.is_file():
                raise FileNotFoundError(f"Source '{source.resolve()}' not found")

            with open(source, encoding="utf-8") as f:
                lines += f.read()

        all_patterns = [l for l in lines.splitlines() if not l.startswith("#")]
        log.debug(f"Matching based on {len(all_patterns):,} pattern(s)")
        log.log(nusex.TRACE, f"Patterns: {all_patterns}")

        spec = PathSpec.from_lines("gitwildmatch", all_patterns)
        excludes = set(spec.match_files(files))
        log.info(f"Found {len(excludes):,} file(s) to exclude")
        return excludes

    def build(
        self,
        files: set[Path],
        project_name: str,
        *,
        project_slug: str | None = None,
        blueprint: type[blueprints.Blueprint] | str | None = None,
        profile: Profile | None = None,
        store_profile: bool = False,
        only_replace_profile_data: bool = False,
    ) -> None:
        """Build this template.

        Args:
            files (:obj:`set` [:obj:`pathlib.Path`]):
                The files to include in the template. This should
                generally obtained using :obj:`find_files` and
                :obj:`process_excludes`.
            project_name (:obj:`str`):
                The name of the project.

        Keyword Args:
            project_slug (:obj:`str` | :obj:`None`):
                The name to use as the project slug. If this is
                :obj:`None`, a project slug is automatically created. In
                the vast majority of cases, it's best to leave this
                alone.
            blueprint (:obj:`type` [:obj:`blueprints.Blueprint`]):
                The blueprint class to use when building this template.
                This must be either :obj:`type` [:obj:`Blueprint`] or a
                subclass thereof. If no blueprint is passed, nusex will
                build a static template.
            profile (:obj:`Profile`):
                A profile instance.
            store_profile (:obj:`bool`):
                Whether to store the given profile's attributes within
                the template. This effectively provides a series of
                default profile attributes that can be used if a profile
                is not provided during deployment, or if the profile is
                missing some attributes. A profile must be passed to use
                this.
            only_replace_profile_data (:obj:`bool`):
                Whether to only replace variables explicitly set as
                attributes in the given profile. If this is :obj:`True`,
                profile attributes set to :obj:`None` will not be
                replaced with placeholder variables when building. This
                is only really useful when storing the profile in the
                template itself. A profile must be passed to use this.
        """
        nfiles = len(files)
        if not nfiles:
            raise TemplateError("No files provided")

        log.info(f"Template will contain {nfiles:,} file(s)")
        if nfiles > nusex.MAX_FILES:
            log.warning(
                "You will not be able to save this template -- "
                f"there are more than {nusex.MAX_FILES:,} files"
            )

        if not project_slug:
            log.debug("Setting project slug")
            project_slug = self._to_slug(project_name)
            log.info(f"Using {project_slug!r} as project slug")

        if profile and store_profile:
            log.info(f"Storing profile '{profile}' in this template")
            self._data.profile_data = profile.to_dict()
            log.debug(f"Profile data to be stored: {self._data.profile_data}")

        log.debug("Loading files into memory")
        cplen = len(os.path.commonpath(files)) + 1  # type: ignore
        self._data.files = {
            f"{path}"[cplen:].replace(project_slug, "PROJECTSLUG"): path.read_bytes()
            for path in files
        }

        if len(max(self._data.files.keys(), key=len)) > nusex.MAX_FILE_KEY_LEN:
            log.warning(
                "You will not be able to save this template -- "
                f"a file name is longer than {nusex.MAX_FILE_KEY_LEN:,} characters"
            )

        if len(max(self._data.files.keys(), key=len)) > nusex.MAX_FILE_SIZE:
            log.warning(
                "You will not be able to save this template -- "
                "a file is larger than 4 GiB"
            )

        if os.name == "nt":
            # Do some stupid unifications to make this work on Windows.
            log.debug("Converting template to work on POSIX systems")
            self._data.files = dict(
                map(
                    lambda kv: (
                        kv[0].replace("\\", "/"),
                        kv[1].replace(b"\r\n", b"\n"),
                    ),
                    self._data.files.items(),
                )
            )

        size = sum(len(v) for v in self._data.files.values())
        log.info(f"Loaded ~{size / 1_048_576:,.0f} MiB into memory")
        log.log(nusex.TRACE, f"Template manifest: {self._data.filenames}")

        # This is damn messy, yikes.
        if isinstance(blueprint, str):
            log.debug("Attempting to resolve blueprint")
            blueprint = blueprints.REGISTERED.get(blueprint, blueprint)
            if isinstance(blueprint, str):
                raise TemplateError(
                    f"{blueprint!r} is not a registered blueprint "
                    "(choose between: " + ", ".join(blueprints.REGISTERED.keys()) + ")"
                )
        elif isinstance(blueprint, type):
            if not issubclass(blueprint, blueprints.Blueprint):
                raise TemplateError("Blueprint class must be a subclass of `Blueprint`")
        elif blueprint:
            raise TemplateError("Invalid blueprint object")

        if blueprint:
            log.debug("Modifying files")
            bp = blueprint(
                self._data.files,
                project_name,
                project_slug,
                profile=profile if only_replace_profile_data else None,
            )
            self._data.language = bp.language
            self._data.files = bp().files

        log.info("Build successful!")

    def set_dependencies(self, *args: str) -> None:
        """Set the dependencies for this template.

        .. note::
            Dependency installations are only supported for Python
            projects.

        Args:
            *args (:obj:`str`):
                A sequence of libraries to store as dependencies.
        """
        if self._data.language != "python":
            raise NotSupported(
                "Dependency installations are only supported for Python projects"
            )

        self._data.dependencies = list(args)
        log.info("Dependencies set")

    def deploy(
        self,
        to_dir: Path | str,
        *,
        project_name: str | None = None,
        project_slug: str | None = None,
        profile: Profile | None = None,
        force: bool = False,
    ) -> None:
        """Deploy this template.

        Args:
            to_dir (:obj:`pathlib.Path` | :obj:`str`):
                The directory to deploy this template into.

        Keyword Args:
            project_name (:obj:`str` | :obj:`None`):
                The name of the project. If this is :obj:`None`, the
                project name is set to the name of the directory the
                template is being deployed to.
            project_slug (:obj:`str` | :obj:`None`):
                The name to use as the project slug. If this is
                :obj:`None`, a project slug is automatically created. In
                the vast majority of cases, it's best to leave this
                alone.
            profile (:obj:`Profile` | :obj:`None`):
                The profile to use when deploying this template.
                Attributes in this profile will override any profile
                attributes stored within the template.
            force (:obj:`bool`):
                Whether to forcibly deploy this template, overwriting
                any existing files.
        """
        to_dir = self._to_absolute_path(to_dir)

        if not project_name:
            if project_slug:
                raise TemplateError(
                    "You cannot specify a project slug without a project name"
                )
            log.debug("Setting project slug")
            project_name = to_dir.parts[-1]
            log.info(f"Using {project_name!r} as project name")

        if not project_slug:
            log.debug("Setting project slug")
            project_slug = self._to_slug(project_name)
            log.info(f"Using {project_slug!r} as project slug")

        log.debug("Setting final filenames")
        self._data.files = dict(
            map(
                lambda kv: (
                    kv[0].replace("PROJECTSLUG", project_slug),  # type: ignore
                    kv[1],
                ),
                self._data.files.items(),
            )
        )

        tdlen = len(f"{to_dir}") + 1
        present_files = [f"{p}"[tdlen:] for p in Path(to_dir).rglob("*")]
        if any(f in present_files for f in self._data.files):
            if not force:
                raise FileExistsError("Template would overwrite existing files")

            log.warning(
                "Some existing files will be overwritten during this deployment"
            )

        profile_data = self._data.profile_data
        if profile:
            log.info("Using data from provided profile")
            profile_data.update(profile.to_dict())
        log.log(nusex.TRACE, f"Profile data being used: {profile_data}")

        def _calver(key: str) -> str:
            v = profile_data.get(key, None) or "$:NULL:"
            if v == "$:NULL:":
                return v
            if v == "CALVER":
                return dt.date.today().strftime("%Y.%m.%d")
            return v

        def _url(key: str) -> str:
            v = profile_data.get(key, None) or "$:NULL:"
            if v == "$:NULL:":
                return v

            iv = v
            v = v.replace("PROJECTNAME", t.cast(str, project_name))
            if v == iv:
                return v.rstrip("/") + f"/{project_name}"
            return v

        project_error = project_slug.replace("_", "").title().replace(" ", "")
        var_mapping = {
            b"$:project_name:": project_name,
            b"$:project_slug:": project_slug,
            b"$:project_year:": f"{dt.date.today().year}",
            b"$:project_license:": "LICENSE",
            b"$:project_error:": f"{project_error}Error",
            **{
                f"$:{k}:".encode(): v or "$:NULL:"
                for k, v in list(profile_data.items())[:5]
            },
            b"$:starting_version:": _calver("starting_version"),
            b"$:version_control_url:": _url("version_control_url"),
            b"$:docs_url:": _url("docs_url"),
            b"$:ci_url:": _url("ci_url"),
        }
        log.debug(f"Variable mapping: {var_mapping}")

        log.info(f"Deploying {len(self._data.files):,} file(s)")
        for file, data in self._data.files.items():
            log.debug(f"Processing {file!r}")
            subdirs = file.split("/")[:-1]
            if subdirs:
                log.log(nusex.TRACE, "File has subdirs -- creating if necessary")
                os.makedirs(to_dir / "/".join(subdirs), exist_ok=True)

            for k, v in var_mapping.items():
                data = data.replace(k, v.encode())

            if b"$:NULL:" in data:
                log.warning(
                    f"File {file!r} deployed with null data -- make sure your profile "
                    "has all the attributes it needs"
                )

            with open(to_dir / file, "wb") as f:
                log.log(nusex.TRACE, f"Writing to {to_dir / file}")
                f.write(data)

        log.info("Deployment successful!")

    def install_dependencies(self) -> None:
        ...

    def save(self, *, to_dir: Path | str, overwrite: bool = False) -> Path:
        """Save this template to disk.

        Keyword Args:
            to_dir (:obj:`pathlib.Path`, :obj:`str`):
                The directory to save the template to.
            overwrite (:obj:`bool`):
                Whether to overwrite an existing template. If this is
                :obj:`False`, an :obj:`FileExistsError` error will be
                raised if a template with the same name already exists.
                Defaults to :obj:`False`.

        Returns:
            :obj:`pathlib.Path`:
                A :obj:`pathlib.Path` object with the full path to the
                template.
        """
        if not checks.name_is_valid(self.name):
            raise InvalidName(
                "Template names must comprise entirely of lower-case "
                "letters, numbers, and underscores"
            )

        if not isinstance(to_dir, Path):
            to_dir = Path(to_dir)

        if not to_dir.is_dir():
            raise NotADirectoryError("Not a directory")

        path = to_dir / f"{self.name}.nsx"
        if path.is_file() and not overwrite:
            raise FileExistsError(
                f"A template called '{self.name}' already exists in the given directory"
            )

        with TemplateIO(path, "wb") as t:
            t.write(self._data)

        log.info(f"Template '{self.name}' saved to {path.resolve()}")
        self._path = path
        return path

    def copy(self, *, name: str | None = None) -> Template:
        """Create a new instance of this template with the same data.

        Keyword Args:
            name (:obj:`str` | :obj:`None`):
                The name to attribute to the copy. If this is
                :obj:`None`, "_copy" will be appended to the name.
                Defaults to :obj:`None`.

        Returns:
            :obj:`Template`
                The copied template.
        """
        t = Template(name or f"{self.name}_copy")
        t._data = self._data
        return t
