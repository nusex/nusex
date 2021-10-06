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

from nusex import CONFIG_DIR


def _update_config(**kwargs):
    print("⌛ Updating config...", end="")
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)

    for k, v in kwargs.items():
        if v:
            data[k] = v

    with open(CONFIG_DIR / "user.nsc", "w") as f:
        json.dump(data, f, ensure_ascii=False)
    print(" done")


def run(**kwargs):
    _update_config(**kwargs)
    print("🎉 User config updated!")


def setup(subparsers):
    s = subparsers.add_parser(
        "config",
        description=(
            "Change your user configuration. All optional arguments default "
            "to their previous values."
        ),
    )
    s.add_argument(
        "-v",
        "--default-version",
        help="the version nusex initialises projects with",
        default="",
    )
    s.add_argument(
        "-d",
        "--default-description",
        help="the description nusex initialises projects with",
        default="",
    )
    s.add_argument(
        "-r",
        "--repo-user-url",
        help="your repository user URL (for example, your GitHub profile URL)",
        default="",
    )
    s.add_argument(
        "-a",
        "--author",
        help="your name, or the name you want to use for your projects",
        default="",
    )
    s.add_argument(
        "-e",
        "--author-email",
        help="your email, or the email of your company/organisation",
        default="",
    )
    s.add_argument(
        "-l",
        "--default-license",
        help="the license nusex initialises projects with",
        default="",
    )
    return subparsers
