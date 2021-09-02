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
from nusex.errors import *
from nusex.helpers import validate_name
from nusex.spec import NSCDecoder, NSCEncoder, NSPDecoder, NSPEncoder

from .base import Entity


class Profile(Entity):
    __slots__ = Entity.__slots__

    def __init__(self, name="default"):
        super().__init__(PROFILE_DIR, name, "nsp")

    def create_new(self, name):
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
        self.data = NSPDecoder().read_data(self.path)

    def save(self):
        NSPEncoder().write_data(self.path, self.data)

    @classmethod
    def current(cls):
        return cls(NSCDecoder().read_data(CONFIG_DIR / "config.nsc")["profile"])

    @classmethod
    def from_nsc_file(cls, name="default"):
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
        return (
            NSCDecoder().read_data(CONFIG_DIR / "config.nsc")["profile"]
            == self.path.stem
        )

    def select(self):
        data = NSCDecoder().read_data(CONFIG_DIR / "config.nsc")
        data["profile"] = self.path.stem
        NSCEncoder().write_data(CONFIG_DIR / "config.nsc", data)

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
                raise InvalidConfiguration(
                    "That version number does not conform to PEP 440 "
                    "standards, or is not 'DATE'"
                )

        if key == "preferred_license":
            option = self._resolve_license(option)
            if not option:
                raise InvalidConfiguration(
                    "Your input could not be resolved to a valid license"
                )

        return option

    def setup(self):
        for k, v in self.data.items():
            kq = (k[0].upper() + k[1:].replace("_", " ")).replace("url", "URL")
            option = input(f"🎤 {kq} [{v}]: ").strip() or v.strip()
            option = self._validate_option(k, option)
            self.data[k] = option

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if v:
                v = self._validate_option(k, v)
                self.data[k] = v
