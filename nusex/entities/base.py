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

from nusex.errors import EntityError


class Entity:
    """A base entity class in containing shared methods and attributes.

    Args:
        dir_ (pathlib.Path): The directory the entity is or will be
            contained in.
        name (str): The name of the entity.
        ext (str): The file extension of the entity.

    Attributes:
        path (pathlib.Path): The complete filepath to the entity.
        data (dict[str, Any]): The data for the entity.
    """

    __slots__ = ("path", "data")

    def __new__(cls, *args, **kwargs):
        if not cls.__bases__[0].__bases__:
            raise EntityError("You cannot create a raw entity")

        return super().__new__(cls)

    def __init__(self, dir_, name, ext):
        self.path = dir_ / f"{name}.{ext}"

        if not os.path.isfile(self.path):
            return self.create_new(name)

        self.load()

    def __str__(self):
        return self.path.stem

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name!r}>"

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __getitem__(self, key):
        return self.data[key]

    @property
    def name(self):
        """The name of the entity.

        Returns:
            str
        """
        return self.path.stem

    @property
    def exists(self):
        """Whether the entity exists on disk.

        Returns:
            bool
        """
        return self.path.is_file()

    def delete(self):
        """Delete this entity.

        Raises:
            FileNotFoundError: The entity does not exist on disk.
        """
        os.remove(self.path)

    def rename(self, new_name):
        """Rename this entity.

        Args:
            new_name (str): The new name for the entity.

        Raises:
            FileNotFoundError: The entity does not exist on disk.
        """
        new_path = f"{self.path}".replace(self.path.stem, new_name)
        self.path = self.path.rename(new_path)
