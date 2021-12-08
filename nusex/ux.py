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

import logging
import platform
import typing as t

import nusex

BANNER = """
\33[38;5;1m      ::::    ::: :::    :::  ::::::::  :::::::::: :::    ::: \33[0m
\33[38;5;208m     :+:+:   :+: :+:    :+: :+:    :+: :+:        :+:    :+:\33[0m
\33[38;5;3m    :+:+:+  +:+ +:+    +:+ +:+        +:+         +:+  +:+    \33[0m
\33[38;5;2m   +#+ +:+ +#+ +#+    +:+ +#++:++#++ +#++:++#     +#++:+      \33[0m
\33[38;5;4m  +#+  +#+#+# +#+    +#+        +#+ +#+         +#+  +#+      \33[0m
\33[38;5;135m #+#   #+#+# #+#    #+# #+#    #+# #+#        #+#    #+#    \33[0m
\33[38;5;5m###    ####  ########   ########  ########## ###    ###       \33[0m

"""


def display_splash() -> None:
    print(
        f"{BANNER}"
        f"\33[3m{nusex.__description__}\33[0m\n\n"
        f"You're using version \33[1m{nusex.__version__}\33[0m.\n\n"
        "This is an alpha version of nusex v2, meaning it is still a "
        "work in progress.\n"
        f"If you encounter any issues, please open an issue at "
        f"\33[4m{nusex.__bugtracker__}\33[0m.\n"
        "If you need CLI functionality or additional features, try "
        "`pip install nusex<2`.\n\n"
        f"Visit \33[4m{nusex.__docs__}\33[0m to find out how to use nusex.\n\n"
        "\33[1mThanks for using nusex!\33[0m"
    )


def display_info() -> None:
    py_impl = platform.python_implementation()
    py_ver = platform.python_version()
    py_comp = platform.python_compiler()
    system = platform.system()
    release = platform.release()

    if system == "Linux":
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("PRETTY_NAME"):
                    d = line.split("=")[1].strip().replace('"', "")
                    distro = f"\n└──{d}"
                    break
    else:
        distro = ""

    print(
        f"nusex {nusex.__version__}\n"
        f"{py_impl} {py_ver} {py_comp}\n"
        f"{system} {release} {distro}"
    )


# Logging stuff.
TRACE = 1
logging.addLevelName(TRACE, "TRACE")


def init_logger(level: int = logging.INFO) -> logging.StreamHandler[t.TextIO]:
    FMT = "{relativeCreated:>05.0f} [{levelname:^7}] {name}: {message}"
    FORMATS = {
        nusex.TRACE: f"\33[38;5;243m{FMT}\33[0m",
        logging.DEBUG: f"\33[38;5;246m{FMT}\33[0m",
        logging.INFO: FMT,
        logging.WARNING: f"\33[1m\33[38;5;178m{FMT}\33[0m",
        logging.ERROR: f"\33[1m\33[38;5;202m{FMT}\33[0m",
        logging.CRITICAL: f"\33[1m\33[38;5;196m{FMT}\33[0m",
    }

    class CustomFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            log_fmt = FORMATS[record.levelno]
            formatter = logging.Formatter(log_fmt, style="{")
            return formatter.format(record)

    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    logging.basicConfig(
        level=level,
        handlers=[handler],
    )
    return handler
