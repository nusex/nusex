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

from nusex import TEMPLATE_DIR, Template
from nusex.errors import AlreadyExists
from nusex.helpers import cprint


def _options_as_set(values):
    s = set(values.split(","))

    if s == {""}:
        return {}

    return s


def _options_as_list(values):
    l = values.split(",")

    if l == [""]:
        return []

    return l


def _check(template):
    cprint("inf", "Showing template manifest (incl. changes):")
    manifest = template.check()
    for file, meta in manifest.items():
        print(file)
        max_meta = len(meta) - 1
        for i, (ln, line) in enumerate(meta):
            if i == max_meta:
                print(f"└── Line {ln}: {line}")
            else:
                print(f"├── Line {ln}: {line}")

    installs = template.data["installs"]
    if installs:
        print()
        cprint("inf", "Showing dependencies:")
        max_dep = len(installs) - 1
        for i, dep in enumerate(installs):
            if i == max_dep:
                print(f"└── {dep}")
            else:
                print(f"├── {dep}")
        return


def run(
    name,
    overwrite,
    check,
    from_repo,
    with_installs,
    with_requirements_file,
    ignore_exts,
    extend_ignore_exts,
    ignore_dirs,
    extend_ignore_dirs,
):
    if os.path.isfile(TEMPLATE_DIR / f"{name}.nsx") and not overwrite:
        raise AlreadyExists(
            "That template already exists (use -o to overwrite)"
        )

    ignore_exts = ignore_exts.union(extend_ignore_exts)
    ignore_dirs = ignore_dirs.union(extend_ignore_dirs)

    if with_requirements_file:
        with open(with_requirements_file) as f:
            d = f.read().split("\n")
            d.remove("")
            with_installs.extend(d)

    # TODO: Make so when overwriting a template, it doesn't have to
    # load the previous one first.
    if from_repo:
        template = Template.from_repo(
            name,
            from_repo,
            installs=with_installs,
            ignore_exts=ignore_exts,
            ignore_dirs=ignore_dirs,
        )
    else:
        template = Template.from_cwd(
            name,
            installs=with_installs,
            ignore_exts=ignore_exts,
            ignore_dirs=ignore_dirs,
        )

    if check:
        return _check(template)

    template.save()
    cprint("aok", f"Template '{name}' built successfully!")


def setup(subparsers):
    s = subparsers.add_parser(
        "build",
        description="Build a new template.",
    )
    s.add_argument("name", help="the name for the new template")
    s.add_argument(
        "-o",
        "--overwrite",
        help="overwrite an existing template should it already exist",
        action="store_true",
    )
    s.add_argument(
        "-c",
        "--check",
        help="check the build manifest without building the template",
        action="store_true",
    )
    s.add_argument(
        "-r",
        "--from-repo",
        help=(
            "a repository URL to build a template from (Git must be "
            "installed)"
        ),
        metavar="URL",
        default="",
    )
    s.add_argument(
        "-i",
        "--with-installs",
        help=(
            "a comma-separated list of dependencies to install when deploying"
        ),
        metavar="DEPS",
        default="",
        type=_options_as_list,
    )
    s.add_argument(
        "-I",
        "--with-requirements-file",
        help=(
            "a file within the template to install dependencies from when "
            "deploying"
        ),
        metavar="FILENAME",
        default="",
    )
    s.add_argument(
        "--ignore-exts",
        help=(
            "a comma-separated list of file extensions to ignore (default: "
            "pyc,pyd,pyo)"
        ),
        metavar="EXTS",
        default="pyc,pyd,pyo",
        type=_options_as_set,
    )
    s.add_argument(
        "--extend-ignore-exts",
        help=(
            "a comma-separated list of file extensions to ignore on top of "
            "the defaults"
        ),
        metavar="EXTS",
        default="",
        type=_options_as_set,
    )
    s.add_argument(
        "--ignore-dirs",
        help=(
            "a comma-separated list of directories to ignore; look at the "
            "docs for more information about advanced ignoring syntaxes "
            "(default: .direnv,.eggs,.git,.hg,.mypy_cache,.nox,.tox,.venv,"
            "venv,.svn,_build,build,dist,buck-out,.pytest-cache,*.egg-info)"
        ),
        metavar="DIRS",
        default=(
            ".direnv,.eggs,.git,.hg,.mypy_cache,.nox,.tox,.venv,venv,.svn,"
            "_build,build,dist,buck-out,.pytest-cache,*.egg-info"
        ),
        type=_options_as_set,
    )
    s.add_argument(
        "--extend-ignore-dirs",
        help=(
            "a comma-separated list of directories to ignore on top of the "
            "defaults"
        ),
        metavar="DIRS",
        default="",
        type=_options_as_set,
    )
    return subparsers
