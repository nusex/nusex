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
from pathlib import Path

import pytest

from nusex import errors
from nusex.api import Profile
from tests import DATA_DIR


@pytest.fixture()  # type: ignore
def blank_profile() -> Profile:
    return Profile("blank")


@pytest.fixture()  # type: ignore
def loaded_profile() -> Profile:
    return Profile(
        "loaded",
        author_name="Barney",
        author_nick="purplebarney",
        author_email="purplebarney@example.com",
        preferred_language="python",
        starting_version="0.1.0",
        preferred_license="mit",
        version_control_url="https://github.com/purplebarney",
        docs_url="https://PROJECTNAME.readthedocs.io",
        ci_url="https://github.com/purplebarney/PROJECTNAME/actions",
    )


def test_blank_attrs(blank_profile: Profile) -> None:
    assert blank_profile.name == "blank"
    assert blank_profile.author_name is None
    assert blank_profile.author_nick is None
    assert blank_profile.author_email is None
    assert blank_profile.preferred_language is None
    assert blank_profile.starting_version is None
    assert blank_profile.preferred_license is None
    assert blank_profile.version_control_url is None
    assert blank_profile.docs_url is None
    assert blank_profile.ci_url is None


def test_loaded_attrs(loaded_profile: Profile) -> None:
    assert loaded_profile.name == "loaded"
    assert loaded_profile.author_name == "Barney"
    assert loaded_profile.author_nick == "purplebarney"
    assert loaded_profile.author_email == "purplebarney@example.com"
    assert loaded_profile.preferred_language == "python"
    assert loaded_profile.starting_version == "0.1.0"
    assert loaded_profile.preferred_license == "mit"
    assert loaded_profile.version_control_url == "https://github.com/purplebarney"
    assert loaded_profile.docs_url == "https://PROJECTNAME.readthedocs.io"
    assert (
        loaded_profile.ci_url == "https://github.com/purplebarney/PROJECTNAME/actions"
    )


def test_edit_attrs(blank_profile: Profile) -> None:
    blank_profile.name = "not_so_blank"
    blank_profile.author_name = "Barney"
    blank_profile.author_nick = "purplebarney"
    blank_profile.preferred_license = "unlicense"

    assert blank_profile.name == "not_so_blank"
    assert blank_profile.author_name is "Barney"
    assert blank_profile.author_nick is "purplebarney"
    assert blank_profile.author_email is None
    assert blank_profile.preferred_language is None
    assert blank_profile.starting_version is None
    assert blank_profile.preferred_license is "unlicense"
    assert blank_profile.version_control_url is None
    assert blank_profile.docs_url is None
    assert blank_profile.ci_url is None


def test_dunders(blank_profile: Profile, loaded_profile: Profile) -> None:
    assert str(blank_profile) == "blank"
    assert repr(blank_profile) == (
        "Profile("
        "name='blank', "
        "author_name=None, "
        "author_nick=None, "
        "author_email=None, "
        "preferred_language=None, "
        "starting_version=None, "
        "preferred_license=None, "
        "version_control_url=None, "
        "docs_url=None, "
        "ci_url=None"
        ")"
    )

    assert not blank_profile == loaded_profile
    assert blank_profile != loaded_profile
    assert not blank_profile == object()
    assert blank_profile != object()


def test_from_disk() -> None:
    profile = Profile.from_disk("stored_profile", from_dir=DATA_DIR)
    assert profile.name == "stored_profile"

    profile = Profile.from_disk("stored_profile", from_dir=str(DATA_DIR))
    assert profile.name == "stored_profile"

    with pytest.raises(NotADirectoryError) as exc1:
        Profile.from_disk("stored_profile", from_dir=Path(__file__))
    assert f"{exc1.value}" == "Not a directory"

    with pytest.raises(FileNotFoundError) as exc2:
        Profile.from_disk("doesnt_exist", from_dir=DATA_DIR)
    assert (
        f"{exc2.value}"
        == "No profile named 'doesnt_exist' exists in the given directory"
    )


def test_path_not_saved(blank_profile: Profile) -> None:
    assert blank_profile.path is None


def test_path_saved() -> None:
    profile = Profile.from_disk("stored_profile", from_dir=DATA_DIR)
    assert profile.path == DATA_DIR / "stored_profile.json"


def test_as_dict(loaded_profile: Profile) -> None:
    assert loaded_profile.to_dict() == {
        "author_name": "Barney",
        "author_nick": "purplebarney",
        "author_email": "purplebarney@example.com",
        "preferred_language": "python",
        "starting_version": "0.1.0",
        "preferred_license": "mit",
        "version_control_url": "https://github.com/purplebarney",
        "docs_url": "https://PROJECTNAME.readthedocs.io",
        "ci_url": "https://github.com/purplebarney/PROJECTNAME/actions",
    }


def test_save(loaded_profile: Profile) -> None:
    loaded_profile.save(to_dir=DATA_DIR)
    assert isinstance(loaded_profile.path, Path)
    assert loaded_profile.path.is_file()

    # TODO: Test conflictions

    with pytest.raises(FileExistsError) as exc1:
        loaded_profile.save(to_dir=str(DATA_DIR))
    assert (
        f"{exc1.value}"
        == "A profile called 'loaded' already exists in the given directory"
    )

    loaded_profile.save(to_dir=str(DATA_DIR), overwrite=True)
    assert isinstance(loaded_profile.path, Path)
    assert loaded_profile.path.is_file()

    with pytest.raises(NotADirectoryError) as exc2:
        loaded_profile.save(to_dir=Path(__file__))
    assert f"{exc2.value}" == "Not a directory"

    loaded_profile.name = "InvalidName"
    with pytest.raises(errors.InvalidName) as exc3:
        loaded_profile.save(to_dir=DATA_DIR)
    assert (
        f"{exc3.value}"
        == "Profile names cannot be longer than 32 characters, which all must be lower-case letters, numbers, or underscores"
    )


def test_delete() -> None:
    # We have to load it in like this.
    profile = Profile.from_disk("loaded", from_dir=DATA_DIR)
    assert isinstance(profile.path, Path)
    assert profile.path.is_file()
    profile.delete()
    assert profile.path is None
    assert not os.path.isfile(DATA_DIR / "loaded.json")

    with pytest.raises(FileNotFoundError) as exc1:
        profile.delete()
    assert f"{exc1.value}" == "This profile has not been saved"
    profile.delete(missing_ok=True)

    # Just ignore the crime I'm about to commit.
    profile._path = Path(__file__).parent
    with pytest.raises(FileNotFoundError) as exc2:
        profile.delete()
    assert f"{exc2.value}" == "This profile was saved, but could not be found"
    profile._path = Path(__file__).parent
    profile.delete(missing_ok=True)


def test_copy(loaded_profile: Profile) -> None:
    profile = loaded_profile.copy()
    assert profile.name == "loaded_copy"
    assert profile != loaded_profile
    assert profile.to_dict() == loaded_profile.to_dict()
