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

import pytest  # type: ignore

from nusex import CONFIG_DIR, PROFILE_DIR, Profile
from nusex.errors import AlreadyExists, ProfileError


def test_create_profile():
    profile = Profile("__test_profile__")
    assert profile.name == "__test_profile__"
    assert profile.data["starting_version"] == "0.1.0"
    assert (
        profile.data["default_description"]
        == "My project, created using nusex"
    )
    assert profile.data["preferred_license"] == "unlicense"

    profile.save()
    assert profile.exists


def test_load_profile():
    profile = Profile("default")
    assert profile.name == "default"
    assert profile.data["author_name"] == "Andy Koffman"
    assert profile.data["author_email"] == "wrestingbears@hotmail.com"
    assert (
        profile.data["git_profile_url"] == "https://github.com/wrestlingbears"
    )
    assert profile.data["starting_version"] == "0.1.0"
    assert (
        profile.data["default_description"]
        == "My project, created using nusex"
    )
    assert profile.data["preferred_license"] == "mit"


def test_select_profile():
    profile = Profile("__test_profile__")
    assert not profile.is_selected

    profile.select()
    assert profile.is_selected


def test_update_profile_author_info():
    profile = Profile("__test_profile__")
    profile.update(
        author_name="Testy McTestface",
        author_email="testy@mcface.com",
    )
    assert profile.data["author_name"] == "Testy McTestface"
    assert profile.data["author_email"] == "testy@mcface.com"


def test_update_profile_git_profile_url():
    profile = Profile("__test_profile__")
    profile.update(git_profile_url="https://github.com/testyface/")
    assert profile.data["git_profile_url"] == "https://github.com/testyface"


def test_update_profile_starting_version():
    profile = Profile("__test_profile__")
    profile.update(starting_version="0.2.0")
    assert profile.data["starting_version"] == "0.2.0"

    with pytest.raises(ProfileError) as exc:
        profile.update(starting_version="test")
    assert f"{exc.value}" == (
        "That version number does not conform to PEP 440 standards, or is "
        "not 'DATE'"
    )


def test_update_profile_default_description():
    profile = Profile("__test_profile__")
    profile.update(default_description="I do be a testy boi tho")
    assert profile.data["default_description"] == "I do be a testy boi tho"


def test_update_profile_preferred_license():
    profile = Profile("__test_profile__")
    profile.update(preferred_license="BSD Zero Clause License")
    assert profile.data["preferred_license"] == "0bsd"

    with pytest.raises(ProfileError) as exc:
        profile.update(preferred_license="test")
    assert (
        f"{exc.value}" == "Your input could not be resolved to a valid license"
    )


def test_rename_profile():
    profile = Profile("__test_profile__")
    profile.rename("__test_profile__")
    # Intentionally explicit.
    assert (PROFILE_DIR / "__test_profile__.nsp").is_file()


def test_delete_profile():
    profile = Profile("__test_profile__")
    profile.delete()
    # Again, intentionally explicit.
    assert not (PROFILE_DIR / "__test_profile__.nsp").is_file()


def test_create_from_legacy():
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

    profile = Profile.from_legacy()
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
    bad_profiles = ("test-profile", "TestProfile", "folder/test")
    good_profiles = ("test", "test_profile", "test69")

    for t in bad_profiles:
        with pytest.raises(ProfileError) as exc:
            Profile(t)
        assert f"{exc.value}" == (
            "Names can only contain lower case letters, numbers, and "
            "underscores"
        )

    for t in good_profiles:
        profile = Profile(t)
        assert profile.name == t

    with pytest.raises(ProfileError) as exc:
        Profile("this_is_a_really_long_profile_name")
    assert f"{exc.value}" == "Names are limited to 24 characters"


def test_reject_reserved_names():
    bad_profiles = ("nsx_simple_app", "nsx_simple_pkg", "nsx_complex_pkg")

    for t in bad_profiles:
        with pytest.raises(ProfileError) as exc:
            Profile(t)
        assert f"{exc.value}" == "That name is reserved"


def test_reject_taken_names():
    with pytest.raises(AlreadyExists) as exc:
        Profile("another_app")
    assert f"{exc.value}" == "A template is already using that name"


def test_select_default_profile():
    # Done to reset the config for other tests.
    profile = Profile()
    profile.select()
    assert profile.is_selected
    assert profile.name == "default"
