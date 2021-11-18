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

import runpy
from importlib import import_module
from pathlib import Path

import nox
from nox import options

from pipelines.config import D

options.sessions = []

for p in (Path(__file__).parent / "pipelines").glob("*.py"):
    if p.stem == "config":
        continue

    mod = import_module(f"pipelines.{p.stem}")
    for name in dir(mod):
        if name.startswith("_"):
            continue

        attr = getattr(mod, name)
        if isinstance(attr, nox._decorators.Func):
            options.sessions.append(name)

    runpy.run_path(f"{p}")


# The following sessions are only ever run manually, as they are
# generally either perform actions (which automatic checks shouldn't
# do), or just display something to the console that isn't useful during
# CI sessions.


@nox.session(reuse_venv=True)
def show_coverage(session: nox.Session) -> None:
    session.install("-U", D["coverage"])

    if not (Path(__file__).parent / ".coverage").is_file():
        session.skip("No coverage to check")

    session.run("coverage", "report", "-m")


@nox.session(reuse_venv=True)
def format(session: nox.Session) -> None:
    session.install("-U", D["black"], D["isort"])
    session.run("isort", ".")
    session.run("black", ".")


@nox.session(reuse_venv=True)
def build_docs(session: nox.Session) -> None:
    session.install("-U", D["sphinx"], D["furo"], ".")
    session.cd("./docs")
    session.run("make", "html")


@nox.session(reuse_venv=True)
def build_package(session: nox.Session) -> None:
    session.install("build==0.7.0")
    session.run("python", "-m", "build")
