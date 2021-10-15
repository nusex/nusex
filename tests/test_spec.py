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

import re
from pathlib import Path

from nusex import CONFIG_DIR, PROFILE_DIR, TEMPLATE_DIR, __version__
from nusex.spec import NSCSpecIO, NSPSpecIO, NSXSpecIO


def test_nsc_spec():
    data = {
        "profile": "default",
        "last_update": re.match(r"[0-9]+.[0-9]+.[0-9]+", __version__).group(),
        "use_wildmatch_ignore": False,
        "auto_update": True,
    }
    NSCSpecIO().write(CONFIG_DIR / "config.nsc", data)

    data2 = NSCSpecIO().read(CONFIG_DIR / "config.nsc")
    assert data == data2


def test_nsp_spec():
    data = {
        "author_name": "John Smith",
        "author_email": "thedoctor@email.com",
        "git_profile_url": "https://github.com/shakespearecode",
        "starting_version": "0.1.0",
        "default_description": "My project, made using nusex",
        "preferred_license": "mit",
    }
    NSPSpecIO().write(PROFILE_DIR / "__nsp_spec_test__.nsp", data)

    data2 = NSPSpecIO().read(PROFILE_DIR / "__nsp_spec_test__.nsp")
    assert data == data2


def test_nsx_spec():
    data = {
        "files": {
            f"{p}".split("/")[-1]: p.read_bytes()
            for p in (Path(__file__).parent / "data/nsx").glob("*")
        },
        "installs": ["analytix", "nusex"],
        "as_extension_for": "template",
    }
    NSXSpecIO().write(TEMPLATE_DIR / "__nsx_spec_test__.nsx", data)

    data2 = NSXSpecIO().read(TEMPLATE_DIR / "__nsx_spec_test__.nsx")
    assert data == data2
