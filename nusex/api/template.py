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

import logging
import os
import re
import typing as t
from pathlib import Path

from pathspec import PathSpec

import nusex
from nusex.api import blueprints
from nusex.api.data import TemplateData
from nusex.errors import InvalidBlueprint

if t.TYPE_CHECKING:
    from nusex.api.profile import Profile

log = logging.getLogger(__name__)


class Template:
    __slots__ = ("name", "_path", "_data")

    def __init__(self, name: str) -> None:
        self.name = name
        self._path: Path | None = None
        self._data = TemplateData()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Template(name={self.name})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.name == other.name

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.name != other.name

    @property
    def path(self) -> Path | None:
        """The filepath to this template. This is :obj:`None` if the
        template has not been saved.

        Returns:
            :obj:`Path`:
                The filepath to this template.
            :obj:`None`:
                This profile has not been saved.
        """
        return self._path

    @property
    def files(self) -> dict[str, bytes]:
        """The files stored in this template. If there are none, this
        is an empty dict.

        Returns:
            :obj:`dict[:obj:`str`, :obj:`bytes`]`:
                This template's files, with the filename as the key, and
                the file's contents as the value.
        """
        return self._data.files

    @property
    def profile_data(self) -> dict[str, str]:
        """The profile data stored in this template. If there is none,
        this is an empty dict.

        .. note ::
            This returns the profile data, *not* a profile instance. To
            get a profile instance, use :obj:`Profile.from_template`.

        Returns:
            :obj:`dict[:obj:`str`, :obj:`str`]`:
                This template's profile data.
        """
        return self._data.profile_data

    @property
    def dependencies(self) -> list[str]:
        """The list of dependencies stored in this template. If there
        are none, this is an empty list.

        Returns:
            :obj:`list[:obj:`str`]`:
                This template's dependencies.
        """
        return self._data.dependencies

    @property
    def language(self) -> str | None:
        """The language this template is for. If no language was set,
        this will return :obj:`None`.
        """
        return self._data.language

    def find_files(self, in_dir: Path | str) -> set[Path]:
        """Recursively search the given directory for files to
        potentially include in the template.

        Args:
            in_dir (:obj:`Path` | :obj:`str`):
                The directory to search through.

        Returns:
            :obj:`set[:obj:`Path`]`:
                The files to potentially include in the template.
        """
        log.debug("Searching for files...")
        if not isinstance(in_dir, Path):
            in_dir = Path(in_dir)

        if not in_dir.is_dir():
            raise NotADirectoryError("Not a directory")

        if not in_dir.is_absolute():
            in_dir = in_dir.resolve()

        files = set(filter(lambda p: p.is_file(), in_dir.rglob("*")))
        log.info(f"Found {len(files):,} files")
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
            files (:obj:`set[:obj:`Path`]`):
                A list of files to compare against exclude patterns.
                This should generally be obtained through
                :obj:`find_files`.

        Keyword Args:
            use_defaults (:obj:`bool`):
                Whether to use the default set of exclude patterns
                employed by the command-line interface.
            sources (:obj:`list[:obj:`Path` | :obj:`str`]` | :obj:`None`):
                A list of files containing glob exclude patterns.
            patterns (:obj:`list[:obj:`str`]`):
                A list of glob exclude patterns.

        Returns:
            :obj:`set[:obj:`Path`]`:
                The files to exclude from the template.
        """
        log.debug("Processing exclude patterns...")
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
        log.debug(f"Matching based on {len(all_patterns):,} patterns")
        log.log(nusex.TRACE, f"Patterns: {all_patterns}")

        spec = PathSpec.from_lines("gitwildmatch", all_patterns)
        excludes = set(spec.match_files(files))
        log.info(f"Found {len(excludes):,} files to exclude")
        return excludes

    def build(
        self,
        files: set[Path],
        project_name: str,
        *,
        project_slug: str | None = None,
        profile: Profile | None = None,
        store_profile: bool = False,
        only_replace_profile_data: bool = False,
        dependencies: list[str] | None = None,
        blueprint: type[blueprints.Blueprint] | str | None = None,
    ) -> None:
        """Build this template.

        Args:
            files (:obj:`set[:obj:`Path`]`):
                The files to include in the template. This should
                generally obtained using :obj:`file_files` and
                :obj:`process_excludes`.
            project_name (:obj:`str`):
                The name of the project.

        Keyword Args:
            project_slug (:obj:`str` | :obj:`None`):
                The name to use as the project slug. If this is
                :obj:`None`, a project slug is automatically created. In
                the vast majority of cases, it's best to leave this
                alone.
            profile (:obj:`Profile`):
                A profile instance.
            store_profile (:obj:`bool`):
                Whether to store the given profile's attributes within
                the template. A profile must be passed to use this.
            only_replace_profile_data (:obj:`bool`):
                Whether to only replace variables explicitly set as
                attributes in the given profile. If this is :obj:`True`,
                profile attributes set to :obj:`None` will not be
                replaced with placeholder variables when building. This
                is only really useful when storing the profile in the
                template itself. A profile must be passed to use this.
            dependencies (:obj:`list[:obj:`str`]` | :obj:`None`):
                A list of dependencies to include in the template. If
                this is not :obj:`None`, then the dependencies will be
                installed during this template's deployment. Dependency
                installations are only supported for Python projects.
            blueprint (:obj:`type[:obj:`Blueprint`]`):
                The blueprint class to use when building this template.
                This must be either :obj:`type[:obj:`Blueprint`]` or a
                subclass thereof. If no blueprint is passed, nusex will
                use the default blueprint, which builds a static
                template.
        """
        nfiles = len(files)
        log.info(f"Template will contain {nfiles:,} files")
        if nfiles > 1000:
            log.warning(
                "You're creating a large template -- this might use a lot of memory"
            )

        if not project_slug:
            log.debug("Setting project slug...")
            project_slug = re.sub(
                "[^a-z0-9_]",
                "",
                re.sub("[- ]", "_", project_name.casefold()),
            )
            log.info(f"Using {project_slug!r} as project slug")

        if profile and store_profile:
            log.info(f"Storing profile '{profile}' in this template")
            self._data.profile_data = {
                k: v for k, v in profile.to_dict().items() if v is not None
            }
            log.debug(f"Profile data to be stored: {self._data.profile_data}")

        log.debug("Loading files into memory...")
        cplen = len(f"{os.path.commonpath(files)}/")  # type: ignore
        self._data.files = {
            f"{path}"[cplen:].replace(project_slug, "PROJECTSLUG"): path.read_bytes()
            for path in files
        }
        size = sum(len(v) for v in self._data.files.values())
        log.info(f"Loaded ~{size / 1_000_000:,.0f} MiB into memory")
        log.log(nusex.TRACE, f"Template manifest: {self._data.filenames}")

        if isinstance(blueprint, str):
            log.debug("Attempting to resolve blueprint...")
            blueprint = blueprints.REGISTERED.get(blueprint, None)
            if not blueprint:
                raise InvalidBlueprint("Cannot resolve key to blueprint class")
        elif isinstance(blueprint, type):
            if not issubclass(blueprint, blueprints.Blueprint):
                raise InvalidBlueprint("Invalid blueprint class provided")
        else:
            raise InvalidBlueprint("Invalid object as blueprint")

        if blueprint:
            # Mypy is bugged -- by this point, blueprint can only be
            # a Blueprint class or subclass, but Mypy still thinks it
            # can be a string.
            blueprint = t.cast(type[blueprints.Blueprint], blueprint)

            log.debug("Modifying files...")
            bp = blueprint(
                self._data.files,
                project_name,
                project_slug,
                profile=profile if only_replace_profile_data else None,
            )
            self._data.language = bp.language
            self._data.files = bp().files

        if dependencies:
            self._data.dependencies = dependencies
            log.info(
                f"Storing these dependencies: " + ", ".join(self._data.dependencies)
            )
            if not blueprint or str(blueprint) != "python":
                log.warning(
                    "Dependency installations are currently only supported on Python"
                )

        log.info("Build successful!")

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
