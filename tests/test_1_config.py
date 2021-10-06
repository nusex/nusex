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
import os
import subprocess as sp
import sys

from nusex import CONFIG_DIR

# Load defaults to revert changes when done
with open(CONFIG_DIR / "user.nsc") as f:
    defaults = json.load(f)


def run(command):
    if sys.version_info >= (3, 7, 0):
        return sp.run(command, shell=True, capture_output=True)

    if os.name != "nt":
        return sp.run(f"{command} > /dev/null 2>&1", shell=True)

    # Windows users will have to put up with the output for 3.6 tests.
    return sp.run(command, shell=True)


def test_version():
    run("nsx config -v 0.2.0")
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)
    assert data["default_version"] == "0.2.0"


def test_description():
    run("nsx config -d 'My awesome project!'")
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)
    assert data["default_description"] == "My awesome project!"


def test_repo_user():
    run("nsx config -r https://gitlab.com/tester")
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)
    assert data["repo_user_url"] == "https://gitlab.com/tester"


def test_author():
    run("nsx config -a 'John Smith'")
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)
    assert data["author"] == "John Smith"


def test_author_email():
    run("nsx config -e johnsmith@example.com")
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)
    assert data["author_email"] == "johnsmith@example.com"


def test_default_license():
    run('nsx config -l "Don\'t steal pls"')
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)
    assert data["default_license"] == "Don't steal pls"


def test_multiple_changes():
    run(
        "nsx config -v '{}' -d '{}' -r '{}' -a '{}' -e '{}' -l '{}'".format(
            *defaults.values()
        )
    )
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)
    assert data == defaults
