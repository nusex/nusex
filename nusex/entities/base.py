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
import os
from pathlib import Path

from nusex.errors import *
from nusex.helpers import is_valid_name


class Entity:
    __slots__ = ("path", "data")

    def __new__(cls, *args, **kwargs):
        if not cls.__bases__[0].__bases__:
            raise InvalidRequest("You cannot create a raw entity")

        return super().__new__(cls)

    def __init__(self, dir_, name, ext):
        self.path = dir_ / f"{name}.{ext}"

        if not os.path.isfile(self.path):
            return self.create_new(name)

        with open(self.path) as f:
            self.data = json.load(f)

    def __str__(self):
        return self.path.stem

    @property
    def exists(self):
        return os.path.isfile(self.path)

    def create_new(self, name):
        if not is_valid_name(name):
            raise InvalidConfiguration(
                "Names can only contain lower case letters, numbers, "
                "and underscores"
            )

        self.data = {}

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f)

    def delete(self):
        os.remove(self.path)

    def rename(self, new_name):
        new_path = f"{self.path}".replace(self.path.stem, new_name)
        self.path = self.path.rename(new_path)
