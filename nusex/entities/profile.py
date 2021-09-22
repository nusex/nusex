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

import json

from nusex import CONFIG_DIR, LICENSE_DIR, PROFILE_DIR, VERSION_PATTERN
from nusex.errors import EntityError
from nusex.helpers import cprint, validate_name
from nusex.spec import NSCDecoder, NSCEncoder, NSPDecoder, NSPEncoder

from .base import Entity

VALID_CONFIG_KEYS = (
    "author_name",
    "author_email",
    "git_profile_url",
    "starting_version",
    "default_description",
    "preferred_license",
)


class Profile(Entity):
    """A class in which to create, load, modify, and save profiles.

    Args:
        name (str): The name of the profile. If the profile does not
            exist, a new one is created, otherwise an existing one is
            loaded. Defaults to "default".

    Attributes:
        path (pathlib.Path): The complete filepath to the profile.
        data (dict[str, Any]): The data for the profile.
    """

    __slots__ = ()

    def __init__(self, name="default"):
        super().__init__(PROFILE_DIR, name, "nsp")

    def create_new(self, name):
        """Create a new profile.

        Args:
            name (str): The name of the profile.
        """
        validate_name(name, self.__class__.__name__)
        self.data = {
            "author_name": "",
            "author_email": "",
            "git_profile_url": "",
            "starting_version": "0.1.0",
            "default_description": "My project, created using nusex",
            "preferred_license": "unlicense",
        }

    def load(self):
        """Load an existing profile. This should never need to be called
        as profiles are loaded automatically when necessary upon object
        creation.

        Raises:
            FileNotFoundError: The profile does not exist on disk.
        """
        self.data = NSPDecoder().read(self.path)

    def save(self):
        """Save this profile.

        Raises:
            EntityError: The profile data has been improperly modified.
        """
        try:
            NSPEncoder().write(self.path, self.data)
        except KeyError:
            raise EntityError(
                "The profile data has been improperly modified"
            ) from None

    @classmethod
    def current(cls):
        """Create an instance for the currently selected profile.

        Returns:
            Profile: The currently selected profile.
        """
        return cls(NSCDecoder().read(CONFIG_DIR / "config.nsc")["profile"])

    @classmethod
    def from_legacy(cls, name="default"):
        """Create a profile from a 0.x spec user.nsc file.

        Keyword Args:
            name (str): The name of the profile. Defaults to "default".

        Returns:
            Profile: The newly converted profile.

        Raises:
            FileNotFoundError: No user.nsc file exists in the config
                directory.
        """
        with open(CONFIG_DIR / "user.nsc") as f:
            data = json.load(f)

        c = cls(name)
        values = list(data.values())
        order = (3, 4, 2, 0, 1, 5)

        for i, k in enumerate(c.data.keys()):
            v = values[order[i]]

            if k == "starting_version":
                if v != "DATE" and not VERSION_PATTERN.match(v):
                    v = (
                        input(f"🎤 Starting version [0.1.0]: ").strip()
                        or "0.1.0"
                    )
                    v = c._validate_option(k, v)

            elif k == "preferred_license":
                v = c._resolve_license(v)
                if not v:
                    v = (
                        input(f"🎤 Preferred license [unlicense]: ").strip()
                        or "unlicense"
                    )

            c.data[k] = v

        return c

    @property
    def is_selected(self):
        """Whether this profile is currently selected.

        Returns:
            bool
        """
        return (
            NSCDecoder().read(CONFIG_DIR / "config.nsc")["profile"]
            == self.path.stem
        )

    def select(self):
        """Select this profile."""
        data = NSCDecoder().read(CONFIG_DIR / "config.nsc")
        data["profile"] = self.path.stem
        NSCEncoder().write(CONFIG_DIR / "config.nsc", data)

    def _resolve_license(self, value):
        for file in LICENSE_DIR.glob("*.txt"):
            if value == file.stem:
                return value

            attrs = {}
            with open(LICENSE_DIR / file) as f:
                for line in f:
                    if line == "---\n":
                        continue
                    if line == "\n":
                        break

                    k, v = line.split(": ")
                    attrs.update({k: v.strip()})

            # Provide as many chances for a match as possible.
            if (
                attrs.get("nickname", "") == value
                or attrs.get("spdx-id", "") == value
                or attrs.get("title", "") == value
                or (
                    attrs.get("title", "")
                    .replace("License", "")
                    .replace("  ", " ")
                    .strip()
                )
                == value
            ):
                return file.stem

    def _validate_option(self, key, option):
        if key == "git_profile_url":
            option = option.strip("/")

        if key == "starting_version":
            if option != "DATE" and not VERSION_PATTERN.match(option):
                raise EntityError(
                    "That version number does not conform to PEP 440 "
                    "standards, or is not 'DATE'"
                )

        if key == "preferred_license":
            option = self._resolve_license(option)
            if not option:
                raise EntityError(
                    "Your input could not be resolved to a valid license"
                )

        return option

    def setup(self):
        """Set up this profile. You will be prompted to input some
        information.

        Raises:
            EntityError: An invalid value was provided to one of the
                inputs.
        """
        for k, v in self.data.items():
            kq = (k[0].upper() + k[1:].replace("_", " ")).replace("url", "URL")
            option = input(f"🎤 {kq} [{v}]: ").strip() or v.strip()
            option = self._validate_option(k, option)
            self.data[k] = option

    def update(self, **kwargs):
        """Update this profile's configuration. All options must be
        passed through as kwargs. Invalid configuration keys raise
        warnings, not errors.

        Keyword Args:
            author_name (str): An author name.
            author_email (str): An author email.
            git_profile_url (str): Your GitHub/Gitlab/BitBucket/etc.
                profile link.
            starting_version (str): The version to initialise project
                with.
            default_description (str): The description to initialise
                projects with.
            preferred_license (str): Your preferred license.
        """
        for k, v in kwargs.items():
            if k not in VALID_CONFIG_KEYS:
                cprint("war", f"'{k}' is not a valid key, skipping...")
                continue

            if v:
                v = self._validate_option(k, v)
                self.data[k] = v
