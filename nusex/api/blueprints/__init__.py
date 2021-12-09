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

__all__ = ("Blueprint", "GenericBlueprint")

import logging
import re
import typing as t
from types import MethodType

import nusex

if t.TYPE_CHECKING:
    from nusex.api.profile import Profile

log = logging.getLogger(__name__)


class Blueprint:
    __slots__ = ("files", "project_name", "project_slug", "profile", "language")

    def __init__(
        self,
        files: dict[str, bytes],
        project_name: str,
        project_slug: str,
        profile: Profile | None = None,
    ) -> None:
        self.files = files
        self.project_name = project_name
        self.project_slug = project_slug
        self.profile = profile
        self.language = self.__class__.__name__[:-9].lower()
        log.debug(f"Set language as {self.language!r}")

    def __str__(self) -> str:
        return self.language

    def __call__(self) -> Blueprint:
        modifiers = []

        for name in dir(self):
            if not name.startswith("modify"):
                continue

            attr = getattr(self, name)
            if isinstance(attr, MethodType):
                modifiers.append(attr)

        log.debug(f"Collected {len(modifiers):,} modifier(s)")
        for m in modifiers:
            m()

        return self


BlueprintT = t.TypeVar("BlueprintT", bound=Blueprint)
_WT = t.Callable[[BlueprintT], None]
_FT = t.Callable[[BlueprintT, str], str]
_DT = t.Callable[[_FT[BlueprintT]], _WT[BlueprintT]]


def with_files(*exprs: str) -> _DT[BlueprintT]:
    def decorator(func: _FT[BlueprintT]) -> _WT[BlueprintT]:
        def wrapper(blueprint: BlueprintT) -> None:
            files = [
                file for file in blueprint.files if re.match("|".join(exprs), file)
            ]

            for file in files:
                contents = blueprint.files.get(file, None)

                if not contents:
                    # File isn't in template.
                    log.log(
                        nusex.TRACE,
                        f"Didn't process {file!r} as it's not in the manifest",
                    )
                    continue

                log.debug(f"Processing {file!r}")
                output = func(blueprint, contents.decode())
                blueprint.files[file] = output.encode()

        return wrapper

    return decorator


def resolve_mapping(mapping: dict[str, str], profile: Profile | None) -> dict[str, str]:
    if not profile:
        return mapping

    keep = []
    for k, v in mapping.items():
        if any(i in v for i in ("PROJECTNAME", "PROJECTSLUG")):
            keep.append(k)

    for kp, vp in profile.to_dict().items():
        if not vp:
            continue

        kp = kp.replace("_", "").upper()

        for km, vm in mapping.items():
            # We have to go through the mapping twice to prevent a bug
            # where non-profile variables would not get replaced when
            # passing an empty profile.
            if kp in vm:
                keep.append(km)

    return {k: mapping[k] for k in keep}


def apply_line_mapping(
    line: str, mapping: dict[str, str], *, delimiter: str = " = "
) -> str:
    try:
        k, v = line.split(delimiter)
        new_v = mapping.get(k, v)
        new_line = f"{k} = {new_v}"
        if new_line != line:
            log.log(nusex.TRACE, f"Modified line: {line!r} is now {new_line!r}")
        return new_line
    except ValueError:
        return line


from .generic import GenericBlueprint

REGISTERED: dict[str, type[Blueprint]] = {
    "generic": GenericBlueprint,
}
