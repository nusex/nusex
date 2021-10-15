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

from nusex import TEMPLATE_DIR
from nusex.errors import DoesNotExist, TemplateError
from nusex.helpers import cprint


def run(names, strict):
    count = 0

    for name in names:
        if not (TEMPLATE_DIR / f"{name}.nsx").exists():
            if strict:
                raise DoesNotExist(f"Template '{name}' not found") from None

            cprint("war", f"Template '{name}' not found, skipping...")
            continue

        os.remove(TEMPLATE_DIR / f"{name}.nsx")
        count += 1

    if not count:
        raise TemplateError("No templates deleted")

    cprint("aok", f"Successfully deleted {count:,} templates!")


def setup(subparsers):
    s = subparsers.add_parser(
        "delete", description="Delete one or more templates."
    )
    s.add_argument(
        "names",
        help="the name(s) of the template(s) to delete",
        nargs="+",
    )
    s.add_argument(
        "--strict",
        help=(
            "throw an error instead of a warning if a template does not exist",
        ),
        action="store_true",
    )
    return subparsers
