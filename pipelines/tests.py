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
import shutil
import zipfile
from pathlib import Path

import nox

from nusex import CONFIG_DIR

TEST_CONFIG_DIR = CONFIG_DIR.parent / (
    "nusex-test" if os.name != "nt" else ".nusex-test"
)
ZIP_PATH = Path(__file__).parent.parent / "tests/data/nusex-test.zip"


@nox.session(reuse_venv=True)
def tests(session: nox.Session) -> None:
    with zipfile.ZipFile(ZIP_PATH) as z:
        z.extractall(TEST_CONFIG_DIR)

    session.install("-Ur", "pipelines/requirements-tests.txt")
    session.run(
        "coverage",
        "run",
        "--omit",
        "tests/*",
        "-m",
        "pytest",
        "--testdox",
        "--log-level=INFO",
    )

    if TEST_CONFIG_DIR.is_dir():
        try:
            shutil.rmtree(TEST_CONFIG_DIR)
        except PermissionError:
            # Some weird permissions error with Windows we don't
            # care about.
            ...
