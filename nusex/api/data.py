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
import sys
import typing as t
from dataclasses import dataclass, field
from pathlib import Path
from types import TracebackType

import nusex
from nusex.errors import TemplateIOError

if sys.version_info >= (3, 10):
    # Gotta take advantage of it, right?
    kwargs = {"slots": True}
else:
    kwargs: dict[str, t.Any] = {}

log = logging.getLogger(__name__)

ID = b"\x99\x88"


@dataclass(**kwargs)
class TemplateData:
    files: dict[str, bytes] = field(init=False, default_factory=dict)
    profile_data: dict[str, str | None] = field(init=False, default_factory=dict)
    dependencies: list[str] = field(init=False, default_factory=list)
    language: str = field(init=False, default_factory=lambda: "none")

    @property
    def filenames(self) -> list[str]:
        return list(self.files.keys())


class TemplateIO:
    __slots__ = ("_path", "_mode", "_file")

    def __init__(self, path: Path, mode: str = "rb") -> None:
        if path.is_dir():
            raise IsADirectoryError("Template path cannot be a directory")

        if mode not in ("rb", "wb"):
            raise TemplateIOError(
                f"Invalid mode '{mode}' (choose between 'rb' and 'wb')"
            )

        self._path = path
        self._mode = mode
        self._file: t.IO[bytes] | None = None

    def __enter__(self) -> TemplateIO:
        self.open()
        return self

    def __exit__(
        self,
        exc_type: t.Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def open(self) -> None:
        self._file = open(self._path, self._mode)

    def close(self) -> None:
        if not self._file:
            raise TemplateIOError("No open file to close")

        self._file.close()
        self._file = None

    def read(self) -> TemplateData:
        if not self._file:
            raise TemplateIOError("No open file to read from")

        if self._mode != "rb":
            raise TemplateIOError("Not in read mode")

        f = self._file

        _id = f.read(2)
        if _id != ID:
            if _id == b"\x99\x78":
                raise TemplateIOError(
                    "Wrong template specification version -- use `read_legacy` instead"
                )
            raise TemplateIOError("Invalid template specification")

        # Skip headers for now.
        f.read(4)

        # Create object.
        data = TemplateData()

        # Language.
        size = int(f.read(4), base=16)
        log.debug(f"Reading language ({size:,} bytes)")
        data.language = f.read(size).decode()

        # Profile data + dependencies.
        for attr in ("profile_data", "dependencies"):
            size = int(f.read(4), base=16)
            log.debug(f"Reading {attr} ({size:,} bytes)")
            setattr(data, attr, json.loads(f.read(size).decode()))

        # Files.
        nfiles = int(f.read(4), base=16)
        log.debug(f"Reading {nfiles:,} files")

        # Can't use dict comp here due to a weird bug(?) in Python 3.7.
        data.files = dict(
            (f.read(int(f.read(4), base=16)).decode(), f.read(int(f.read(8), base=16)))
            for _ in range(nfiles)
        )

        return data

    # def read_legacy(self) -> TemplateData:
    #     ...

    def write(self, data: TemplateData) -> None:
        if not self._file:
            raise TemplateIOError("No open file to write to")

        if self._mode != "wb":
            raise TemplateIOError("Not in write mode")

        f = self._file

        # Identifier.
        f.write(ID)

        # Headers.
        f.write(b"0000")

        # Language.
        f.write((f"{hex(len(data.language))[2:]:>04}" + data.language).encode())

        # Profile data + dependencies.
        for attr in ("profile_data", "dependencies"):
            value = json.dumps(getattr(data, attr))
            len_v = len(value)

            if len_v > 0xFFFF:
                raise TemplateIOError(f"Too much data ({attr})")

            f.write((f"{hex(len_v)[2:]:>04}" + value).encode())

        # Files.
        len_f = len(data.files)

        if len_f > nusex.MAX_FILES:
            raise TemplateIOError(f"Maximum file limit ({nusex.MAX_FILES:,}) exceeded")

        f.write(f"{hex(len_f)[2:]:>04}".encode())

        for k, v in data.files.items():
            len_k = len(k)
            len_v = len(v)

            if len_k > nusex.MAX_FILE_KEY_LEN:
                raise TemplateIOError(
                    f"Maximum file key length ({nusex.MAX_FILE_KEY_LEN:,}) exceeded"
                )

            if len_v > nusex.MAX_FILE_SIZE:
                raise TemplateIOError(f"Maximum file size (4 GiB) exceeded")

            f.write((f"{hex(len_k)[2:]:>04}" + k).encode())
            f.write(f"{hex(len_v)[2:]:>08}".encode() + v)
