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
import shutil

import pytest  # type: ignore

from nusex import CONFIG_DIR, PROFILE_DIR, Profile
from nusex.errors import *


def test_create_profile():
    profile = Profile("__test__")
    assert profile.name == "__test__"
    assert profile.data["starting_version"] == "0.1.0"
    assert (
        profile.data["default_description"]
        == "My project, created using nusex"
    )
    assert profile.data["preferred_license"] == "unlicense"

    profile.save()
    assert profile.exists


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
    assert f"{exc.value}" == (
        "That version number does not conform to PEP 440 standards, or is "
        "not 'DATE'"
    )

    profile.update(preferred_license="BSD Zero Clause License")
    assert profile.data["preferred_license"] == "0bsd"

    with pytest.raises(InvalidConfiguration) as exc:
        profile.update(preferred_license="test")
    assert (
        f"{exc.value}" == "Your input could not be resolved to a valid license"
    )


def test_rename_profile():
    profile = Profile("__test__")
    profile.rename("__test_profile__")
    # Intentionally explicit.
    assert os.path.isfile(PROFILE_DIR / "__test_profile__.nsp")

    # Before continue, copy the file for later tests.
    shutil.copyfile(
        PROFILE_DIR / "__test_profile__.nsp", PROFILE_DIR / "__test__.nsp"
    )


def test_delete_profile():
    profile = Profile("__test_profile__")
    profile.delete()
    assert not os.path.isfile(PROFILE_DIR / "__test_profile__.nsp")


def test_create_from_nsc_file():
    # Write the nsc file.
    with open(CONFIG_DIR / "user.nsc", "w") as f:
        data = {
            "default_version": "0.1.0",
            "default_description": "My project, created using nusex",
            "repo_user_url": "https://github.com/faceytest",
            "author": "Facey McFacetest",
            "author_email": "facey@mctest.com",
            "default_license": "BSD Zero Clause License",
        }
        json.dump(data, f)

    profile = Profile.from_nsc_file()
    assert tuple(profile.data.keys()) == (
        "author_name",
        "author_email",
        "git_profile_url",
        "starting_version",
        "default_description",
        "preferred_license",
    )
    assert profile.data["author_name"] == "Facey McFacetest"
    assert profile.data["author_email"] == "facey@mctest.com"
    assert profile.data["git_profile_url"] == "https://github.com/faceytest"
    assert profile.data["starting_version"] == "0.1.0"
    assert (
        profile.data["default_description"]
        == "My project, created using nusex"
    )
    assert profile.data["preferred_license"] == "0bsd"


def test_validate_profile_names():
    bad_templates = ("test-template", "TestTemplate", "folder/test")
    good_templates = ("test", "test_template", "test69")

    for t in bad_templates:
        with pytest.raises(InvalidConfiguration) as exc:
            Profile(t)
        assert f"{exc.value}" == (
            "Names can only contain lower case letters, numbers, and "
            "underscores"
        )

    for t in good_templates:
        profile = Profile(t)
        assert profile.name == t

    with pytest.raises(AlreadyExists) as exc:
        Profile("simple_pkg")
    assert f"{exc.value}" == "That name is already in use elsewhere"