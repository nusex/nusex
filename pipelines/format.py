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

import nox

from pipelines.config import (
    CHECK_PATHS,
    PIPELINE_DIR,
    PROJECT_DIR,
    PROJECT_NAME,
    TEST_DIR,
    D,
)


@nox.session(reuse_venv=True)
def check_formatting(session: nox.Session) -> None:
    session.install("-U", D["black"])
    session.run("black", ".", "--check")


@nox.session(reuse_venv=True)
def check_imports(session: nox.Session) -> None:
    session.install("-U", D["flake8"], D["isort"])
    # flake8 doesn't use the gitignore so we have to be explicit.
    session.run(
        "flake8",
        *CHECK_PATHS,
        "--select",
        "F4",
        "--extend-ignore",
        "E,F,W",
        "--extend-exclude",
        "__init__.py",
    )
    session.run("isort", ".", "-cq")


@nox.session(reuse_venv=True)
def check_typing(session: nox.Session) -> None:
    session.install("-U", D["mypy"], "-r", "requirements.txt")
    session.run("mypy", *CHECK_PATHS)


@nox.session(reuse_venv=True)
def check_line_lengths(session: nox.Session) -> None:
    session.install("-U", D["len8"])
    session.run("len8", *CHECK_PATHS, "-lx", "data")


@nox.session(reuse_venv=True)
def check_licensing(session: nox.Session) -> None:
    missing = []

    for p in [
        *(PROJECT_DIR / PROJECT_NAME).rglob("*.py"),
        *TEST_DIR.glob("*.py"),
        *PIPELINE_DIR.glob("*.py"),
        *PROJECT_DIR.glob("*.py"),
    ]:
        with open(p) as f:
            if not f.read().startswith("# Copyright (c)"):
                missing.append(p)

    if missing:
        session.error(
            f"\n{len(missing):,} file(s) are missing their licenses:\n"
            + "\n".join(f" - {file}" for file in missing)
        )


@nox.session(reuse_venv=True)
def check_spelling(session: nox.Session) -> None:
    session.install("-U", D["codespell"])
    session.run("codespell", *CHECK_PATHS)
