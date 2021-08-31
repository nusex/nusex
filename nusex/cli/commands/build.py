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

from nusex import PROFILE_DIR, Profile
from nusex.errors import *
from nusex.helpers import cprint


def _build_profile(name, overwrite):
    if os.path.isfile(PROFILE_DIR / f"{name}.nsp") and not overwrite:
        raise AlreadyExists(
            "A profile with that name already exists (use -o to ignore this)"
        )

    profile = Profile(name)
    profile.setup()
    profile.save()
    profile.select()
    cprint("aok", f"Profile '{profile.name}' successfully created!")


def run(name, extension, profile, overwrite, check, from_repo):
    if profile:
        return _build_profile(name, overwrite)


def setup(subparsers):
    s = subparsers.add_parser(
        "build",
        description="Build a new template, profile, or extension.",
    )
    s.add_argument(
        "name", help="the name for the new template, profile, or extension"
    )
    s.add_argument(
        "-p",
        "--profile",
        help="build an profile instead of a template (overrides -e)",
        action="store_true",
    )
    s.add_argument(
        "-e",
        "--extension",
        help="build an extension instead of a template",
        action="store_true",
    )
    s.add_argument(
        "-o",
        "--overwrite",
        help=(
            "overwrite an existing template, profile, or extension should it "
            "already exist"
        ),
        action="store_true",
    )
    s.add_argument(
        "-c",
        "--check",
        help=(
            "check the build manifest before building the template "
            "or extension"
        ),
        action="store_true",
    )
    s.add_argument(
        "-r",
        "--from-repo",
        help="a repo URL to build a template from",
        metavar="REPO_URL",
        default="",
    )
    return subparsers
