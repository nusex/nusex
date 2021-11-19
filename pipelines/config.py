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

import re
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
TEST_DIR = PROJECT_DIR / "tests"
PIPELINE_DIR = PROJECT_DIR / "pipelines"

PROJECT_NAME = Path(__file__).parent.parent.stem

CHECK_PATHS = (
    str(PROJECT_DIR / PROJECT_NAME),
    str(TEST_DIR),
    str(PIPELINE_DIR),
    str(PROJECT_DIR / "noxfile.py"),
    str(PROJECT_DIR / "setup.py"),
)

DEP_PATTERN = re.compile("([a-zA-Z0-9-_]*)[=~<>,.0-9ab]*")


def resolve_requirements(*paths: str) -> dict[str, str]:
    deps = {}

    for path in paths:
        with open(path) as f:
            for line in f:
                if line.startswith(("#", "git")) or line == "\n":
                    continue

                if line.startswith("-r"):
                    deps.update(resolve_requirements(line[3:-1]))
                    continue

                match = DEP_PATTERN.match(line)
                if match:
                    deps.update({match.group(1): match.group(0)})

    return deps


D = resolve_requirements(
    PROJECT_DIR / "requirements-nox.txt", PROJECT_DIR / "requirements-rtd.txt"
)
