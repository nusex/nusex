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

import pytest  # type: ignore

from nusex import CONFIG_DIR, PROFILE_DIR, Profile
from nusex.errors import *
from nusex.helpers import run


def test_create_profile():
    profile = Profile("__test__")
    assert profile.name == "__test__"
    assert profile.data["starting_version"] == "0.1.0"
    assert profile.data["default_description"] == "My project, made using nusex"
    assert profile.data["preferred_license"] == "unlicense"

    profile.save()
    assert os.path.isfile(PROFILE_DIR / "__test__.nsp")


def test_select_profile():
    profile = Profile("__test__")
    assert not profile.is_selected

    profile.select()
    assert profile.is_selected


def test_update_profile():
    profile = Profile("__test__")

    profile.update(
        author_name="Testy McTestface",
        author_email="testy@mcface.com",
    )
    assert profile.data["author_name"] == "Testy McTestface"

    profile.update(git_profile_url="https://github.com/testyface/")
    assert profile.data["git_profile_url"] == "https://github.com/testyface"

    with pytest.raises(InvalidConfiguration) as exc:
        profile.update(starting_version="test")
    assert f"{exc.value}" == "That version number does not conform to PEP 440 standards, or is not 'DATE'"

    profile.update(preferred_license="BSD Zero Clause License")
    assert profile.data["preferred_license"] == "0bsd"

    with pytest.raises(InvalidConfiguration) as exc:
        profile.update(preferred_license="test")
    assert f"{exc.value}" == "Your input could not be resolved to a valid license"


def test_rename_profile():
    profile = Profile("__test__")
    profile.rename("__test_profile__")
    assert os.path.isfile(PROFILE_DIR / "__test_profile__.nsp")

    # Before continue, copy the file for later tests.
    shutil.copyfile(PROFILE_DIR / "__test_profile__.nsp", PROFILE_DIR / "__test__.nsp")


def test_delete_profile():
    profile = Profile("__test_profile__")
    profile.delete()
    assert not os.path.isfile(PROFILE_DIR / "__test_profile__.nsp")
