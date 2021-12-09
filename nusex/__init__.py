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

__all__ = (
    "TRACE",
    "CONFIG_DIR",
    "TEMP_DIR",
    "CONFIG_FILE",
    "LICENSES_FILE",
    "PROFILE_DIR",
    "TEMPLATE_DIR",
    "VALID_NAME_PATTERN",
    "BLUEPRINT_MAPPING",
    "api",
    "checks",
    "errors",
    "ux",
)

__productname__ = "nusex"
__version__ = "2.0.0a2"
__description__ = "A dynamic, multi-language project templating utility."
__url__ = "https://github.com/nusex/nusex"
__docs__ = "https://nusex.readthedocs.io"
__author__ = "Ethan Henderson"
__author_email__ = "ethan.henderson.1998@gmail.com"
__license__ = "BSD 3-Clause 'New' or 'Revised' License"
__bugtracker__ = "https://github.com/nusex/nusex/issues"
__ci__ = "https://github.com/nusex/nusex/actions"

import os
import re
import sys
from pathlib import Path

from . import api, checks, errors, ux
from .ux import TRACE


# Ger paths for important files and dirs.
def _suffix() -> str:
    # Determine whether this is a production copy or not. This
    # prevents actual user configs from getting messed up.
    parts = Path(__file__).parts
    if "nox" in " ".join(sys.argv) or ".nox" in parts:
        return "nusex-test"
    if "site-packages" not in parts:
        return "nusex-dev"
    return "nusex"


CONFIG_DIR = Path.home() / (
    f".{_suffix()}" if os.name == "nt" else f".config/{_suffix()}"
)
CONFIG_FILE = CONFIG_DIR / "config.nsc"
LICENSES_FILE = CONFIG_DIR / "licenses.json"
PROFILE_DIR = CONFIG_DIR / "profiles"
TEMPLATE_DIR = CONFIG_DIR / "templates"

# Name validation.
VALID_NAME_PATTERN = re.compile("[a-z0-9_]{,32}$")

# Excludes
DEFAULT_EXCLUDE_PATTERNS = [
    ".direnv",
    ".eggs",
    ".git",
    ".hg",
    ".mypy_cache",
    ".nox",
    ".tox",
    ".venv",
    "venv",
    ".svn",
    "_build",
    "build",
    "dist",
    "buck-out",
    ".pytest_cache",
    ".coverage",
    "*.egg-info",
    ".nusexmeta",
]
