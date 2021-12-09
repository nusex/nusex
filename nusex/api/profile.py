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

import json
import logging
import os
from pathlib import Path

import nusex
from nusex import checks
from nusex.errors import InvalidName

log = logging.getLogger(__name__)


class Profile:
    """A class representing a profile.

    All keyword arguments are different attributes which nusex will use
    when deploying templates. They all default to :obj:`None` if not
    passed, which means nusex will not replace these values when
    building or deploying templates.

    Args:
        name (:obj:`str`):
            The name of the profile.

    Keyword Arguments:
        author_name (:obj:`str` | :obj:`None`):
            The name which you wish to be attributed in new projects.
            This should be your real name, a nickname, or your
            organisation's name.
        author_nick (:obj:`str` | :obj:`None`):
            The username you normally use for services related to your
            development projects.
        author_email (:obj:`str` | :obj:`None`):
            The email address through which users can contact you or
            your organisation.
        preferred_language (:obj:`str` | :obj:`None`):
            The language you would normally be developing using when
            using this profile.
        preferred_license (:obj:`str` | :obj:`None`):
            The name which you wish to be attributed in new projects.
            When deploying a project nusex will use this as a key, and
            attempt to resolve it against a list of open-source
            licenses.
        starting_version (:obj:`str` | :obj:`None`):
            The version to deploy projects with. By default nusex will
            use this value as-is, but if you set this to "CALVER" nusex
            will use the current date in YYYY.MM.DD format when
            deploying the project.
        version_control_url (:obj:`str` | :obj:`None`):
            The URL of your version control host (i.e. GitHub),
            including your username. By default nusex will append the
            name of the project to the end of this URL when deploying,
            but you can override this behaviour by including
            "PROJECTNAME" anywhere in this URL.
        docs_url (:obj:`str` | :obj:`None`):
            The URL of the documentation hosting service you normally
            use. Different documentation hosting services handles URLs
            differently -- by default nusex will append the name of the
            project to the end of the URL, but you can override this
            behaviour by inserting "PROJECTNAME" anywhere in the URL. If
            you use ReadTheDocs for example, you will need to do this.
        ci_url (:obj:`str` | :obj:`None`):
            The URL of the continuous integration suite you normally
            use. By default nusex will append the name of the project to
            the end of this URL when deploying, but you can override
            this behaviour by including "PROJECTNAME" anywhere in this
            URL.
    """

    __slots__ = (
        "name",
        "_path",
        "author_name",
        "author_nick",
        "author_email",
        "preferred_language",
        "preferred_license",
        "starting_version",
        "version_control_url",
        "docs_url",
        "ci_url",
    )

    def __init__(self, name: str, **kwargs: str) -> None:
        self.name = name
        self._path: Path | None = None

        self.author_name = kwargs.pop("author_name", None)
        self.author_nick = kwargs.pop("author_nick", None)
        self.author_email = kwargs.pop("author_email", None)
        self.preferred_language = kwargs.pop("preferred_language", None)
        self.preferred_license = kwargs.pop("preferred_license", None)
        self.starting_version = kwargs.pop("starting_version", None)
        self.version_control_url = kwargs.pop("version_control_url", None)
        self.docs_url = kwargs.pop("docs_url", None)
        self.ci_url = kwargs.pop("ci_url", None)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        attrs = (f"{s}={getattr(self, s)!r}" for s in Profile.__slots__ if s != "_path")
        return "Profile(" + ", ".join(attrs) + ")"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.name == other.name

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.name != other.name

    @classmethod
    def from_disk(cls, name: str, *, from_dir: Path | str) -> Profile:
        """Load a saved profile.

        Args:
            name (:obj:`str`):
                The name of the profile to load.

        Keyword Args:
            from_dir (:obj:`Path` | :obj:`str`):
                The directory to load the profile from.

        Returns:
            :obj:`Profile`:
                A profile instance.
        """
        if not isinstance(from_dir, Path):
            from_dir = Path(from_dir)

        if not from_dir.is_dir():
            raise NotADirectoryError("Not a directory")

        path = from_dir / f"{name}.json"
        if not path.is_file():
            raise FileNotFoundError(
                f"No profile named '{name}' exists in the given directory"
            )

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        log.info(f"Profile '{name}' loaded")
        log.log(nusex.TRACE, f"Data: {data}")
        c = cls(name, **data)
        c._path = path
        return c

    @property
    def path(self) -> Path | None:
        """The filepath to this profile. This is :obj:`None` if the
        profile has not been saved.

        Returns:
            :obj:`Path`:
                The filepath to this profile.
            :obj:`None`:
                This profile has not been saved.
        """
        return self._path

    def to_dict(self, *, default: str = "None") -> dict[str, str]:
        """Export this profile's attributes to a dict object.

        Returns:
            :obj:`dict[:obj:`str`, :obj:`str`]`:
                This profile's attributes, with the attribute name as
                the key, and the attribute value as the value.
        """
        return {s: getattr(self, s) or default for s in Profile.__slots__[2:]}

    def save(self, *, to_dir: Path | str, overwrite: bool = False) -> Path:
        """Save this profile to disk.

        Keyword Args:
            to_dir (:obj:`Path`, :obj:`str`):
                The directory to save the profile to.
            overwrite (:obj:`bool`):
                Whether to overwrite an existing profile. If this is
                ``False``, an :obj:`AlreadyExists` error will be raised
                if a profile with the same name already exists. Defaults
                to ``False``.

        Returns:
            :obj:`Path`:
                A :obj:`pathlib.Path` object with the full path to the
                profile.
        """
        if not checks.name_is_valid(self.name):
            raise InvalidName(
                "Profile names cannot be longer than 32 characters, which all "
                "must be lower-case letters, numbers, or underscores"
            )

        if to_dir == nusex.PROFILE_DIR:
            if not checks.does_not_conflict(self.name, nusex.TEMPLATE_DIR, "nsx"):
                raise InvalidName(
                    "This profile cannot be saved here while a template with the same "
                    "name exists in nusex's template directory"
                )

        if not isinstance(to_dir, Path):
            to_dir = Path(to_dir)

        if not to_dir.is_dir():
            raise NotADirectoryError("Not a directory")

        path = to_dir / f"{self.name}.json"
        if path.is_file() and not overwrite:
            raise FileExistsError(
                f"A profile called '{self.name}' already exists in the given directory"
            )

        with open(path, "w", encoding="utf-8") as f:
            log.debug("Now dumping data...")
            json.dump(self.to_dict(), f, ensure_ascii=False)

        log.info(f"Profile '{self.name}' saved to {path.resolve()}")
        self._path = path
        return path

    def delete(self, *, missing_ok: bool = False) -> Path | None:
        """Delete this profile from disk.

        Keyword Args:
            missing_ok (:obj:`bool`):
                Whether to ignore errors upon a missing profile. If this
                is ``False``, an :obj:`DoesNotExist` error will be
                raised if the profile has not been saved. Defaults to
                ``False``.

        Returns:
            :obj:`Path`:
                A :obj:`pathlib.Path` object with the full path to the
                profile.
            :obj:`None`:
                The profile was not saved and :obj:`missing_ok` is
                ``True``.
        """
        if not self._path:
            if not missing_ok:
                raise FileNotFoundError("This profile has not been saved")

            return None

        if not self._path.is_file():
            self._path = None

            if not missing_ok:
                raise FileNotFoundError(
                    "This profile was saved, but could not be found"
                )

            return None

        os.remove(self._path)
        path = self._path
        self._path = None
        return path

    def copy(self, *, name: str | None = None) -> Profile:
        """Create a new instance of this profile with the same
        attributes.

        Keyword Args:
            name (:obj:`str` | :obj:`None`):
                The name to attribute to the copy. If this is
                :obj:`None`, "_copy" will be appended to the name.
                Defaults to :obj:`None`.

        Returns:
            :obj:`Profile`:
                The copied profile.
        """
        return Profile(name or f"{self.name}_copy", **self.to_dict())
