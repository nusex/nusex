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

import datetime as dt
import os
from pathlib import Path

import pytest

from nusex import errors
from nusex.api import Profile, Template, blueprints
from nusex.api.data import TemplateData
from tests import DATA_DIR, as_relative

TEMPLATE_DATA_DIR = DATA_DIR / "templates"
GENERIC_DATA_DIR = TEMPLATE_DATA_DIR / "testarossa_generic"
DEPLOY_DIR = DATA_DIR / "test_deploy"

FILENAMES = set(
    (
        ".gitignore",
        ".nusexmeta",
        "CONTRIBUTING",
        "CONTRIBUTING.md",
        "COPYING",
        "COPYING.md",
        "LICENCE",
        "LICENCE.txt",
        "LICENSE",
        "LICENSE.txt",
        "README",
        "README.md",
        "README.txt",
        "build/artefact",
        "docs/conf.py",
        "docs/source/conf.py",
        "ignore_dir/markdown.md",
        "ignore_dir/text.txt",
        "ignore_file.txt",
        "testarossa_generic/__init__.py",
    )
)

BUILT_FILENAMES = set(
    map(lambda x: x.replace("testarossa_generic", "PROJECTSLUG"), FILENAMES)
)

EXCLUDES = set(
    (
        ".nusexmeta",
        "build/artefact",
        "ignore_dir/markdown.md",
        "ignore_dir/text.txt",
        "ignore_file.txt",
    )
)

YEAR = dt.date.today().year


@pytest.fixture()  # type: ignore
def template() -> Template:
    return Template("noxtest")


@pytest.fixture()  # type: ignore
def profile() -> Profile:
    return Profile(
        "templatetest", author_name="Barney", author_email="purplebarney@example.com"
    )


@pytest.fixture()  # type: ignore
def generic_files() -> set[Path]:
    return set((GENERIC_DATA_DIR / f) for f in FILENAMES)


@pytest.fixture()  # type: ignore
def generic_excludes() -> set[Path]:
    return set((GENERIC_DATA_DIR / f) for f in EXCLUDES)


def test_vars(template: Template) -> None:
    assert template.name == "noxtest"
    assert template._path == None
    assert template._data == TemplateData()


def test_edit_name(template: Template) -> None:
    template.name = "ilovetests"
    assert template.name == "ilovetests"


def test_str(template: Template) -> None:
    assert str(template) == "noxtest"


def test_repr(template: Template) -> None:
    assert repr(template) == "Template(name='noxtest')"


def test_hash(template: Template) -> None:
    assert isinstance(hash(template), int)

    assert {template: "Template"}


def test_equal(template: Template) -> None:
    template2 = Template("another_template")
    assert template == template
    assert not template == template2
    assert not template == object()


def test_not_equal(template: Template) -> None:
    template2 = Template("another_template")
    assert not template != template
    assert template != template2
    assert template != object()


def test_copy(template: Template) -> None:
    template_copy = template.copy()
    assert template_copy.name == "noxtest_copy"
    assert template_copy != template
    assert template_copy._data == template._data


def test_initial_properties(template: Template) -> None:
    assert template.path == None
    assert template.files == {}
    assert template.profile_data == {}
    assert template.dependencies == []
    assert template.language == "none"


def test_find_files_absolute(template: Template, generic_files: set[Path]) -> None:
    files = template.find_files(in_dir=GENERIC_DATA_DIR)
    assert isinstance(files, set)
    assert files == generic_files


def test_find_files_relative(template: Template, generic_files: set[Path]) -> None:
    files = template.find_files(in_dir=as_relative(GENERIC_DATA_DIR))
    assert isinstance(files, set)
    assert files == generic_files


def test_find_files_not_directory(template: Template) -> None:
    with pytest.raises(NotADirectoryError) as exc:
        template.find_files(in_dir=Path(__file__))
    assert str(exc.value) == "Not a directory"


def test_process_excludes_none(template: Template, generic_files: set[Path]) -> None:
    excludes = template.process_excludes(generic_files)
    assert isinstance(excludes, set)
    assert len(excludes) == 0


def test_process_excludes_sources(template: Template, generic_files: set[Path]) -> None:
    excludes = template.process_excludes(
        generic_files,
        sources=[GENERIC_DATA_DIR / ".gitignore", str(GENERIC_DATA_DIR / ".gitignore")],
    )
    assert isinstance(excludes, set)
    assert len(excludes) == 3


def test_process_excludes_patterns(
    template: Template, generic_files: set[Path]
) -> None:
    excludes = template.process_excludes(
        generic_files, patterns=["ignore_dir/", "ignore_file.txt"]
    )
    assert isinstance(excludes, set)
    assert len(excludes) == 3


def test_process_excludes_defaults(
    template: Template, generic_files: set[Path]
) -> None:
    excludes = template.process_excludes(generic_files, use_defaults=True)
    assert isinstance(excludes, set)
    assert len(excludes) == 2


def test_process_excludes_errors(template: Template, generic_files: set[Path]) -> None:
    with pytest.raises(FileNotFoundError) as exc:
        template.process_excludes(generic_files, sources=["doesnt_exist"])
    # Can't rely on exact values cos this uses absolute directories.
    assert str(exc.value).startswith("Source '")
    assert str(exc.value).endswith("' not found")


def test_build_static(
    template: Template, generic_files: set[Path], generic_excludes: set[Path]
) -> None:
    template.build(generic_files - generic_excludes, "Testarossa Generic")
    # Using sorted just to get rid of any nonsense.
    assert sorted(template.files.keys()) == sorted(BUILT_FILENAMES - EXCLUDES)

    for key in ("README", "README.md", "README.txt"):
        lines = template.files[key].decode().splitlines()
        assert lines[0] == "# Testarossa Generic"


def test_build_blueprint_class(
    template: Template, generic_files: set[Path], generic_excludes: set[Path]
) -> None:
    template.build(
        generic_files - generic_excludes,
        "Testarossa Generic",
        blueprint=blueprints.GenericBlueprint,
    )
    assert sorted(template.files.keys()) == sorted(BUILT_FILENAMES - EXCLUDES)

    for key in ("README", "README.md", "README.txt"):
        lines = template.files[key].decode().splitlines()
        assert lines[0] == "# $:project_name:"
        assert lines[6 if key == "README" else -1] == blueprints.generic.ACK

    for key in ("CONTRIBUTING", "CONTRIBUTING.md"):
        body = template.files[key].decode()
        assert body == "Thanks for contributing to $:project_name:!\n"

    for key in ("docs/conf.py", "docs/source/conf.py"):
        lines = template.files[key].decode().splitlines()
        assert lines[15] == "import $:project_slug:"
        assert lines[22] == 'project = "$:project_name:"'
        assert lines[23] == 'copyright = "$:project_year:, $:author_name:"'
        assert lines[24] == 'author = "$:author_name:"'
        assert lines[27] == "release = $:project_slug:.__version__"


def test_build_blueprint_string(
    template: Template, generic_files: set[Path], generic_excludes: set[Path]
) -> None:
    template.build(
        generic_files - generic_excludes, "Testarossa Generic", blueprint="generic"
    )
    assert sorted(template.files.keys()) == sorted(BUILT_FILENAMES - EXCLUDES)

    for key in ("README", "README.md", "README.txt"):
        lines = template.files[key].decode().splitlines()
        assert lines[0] == "# $:project_name:"
        assert lines[6 if key == "README" else -1] == blueprints.generic.ACK

    for key in ("CONTRIBUTING", "CONTRIBUTING.md"):
        body = template.files[key].decode()
        assert body == "Thanks for contributing to $:project_name:!\n"

    for key in ("docs/conf.py", "docs/source/conf.py"):
        lines = template.files[key].decode().splitlines()
        assert lines[15] == "import $:project_slug:"
        assert lines[22] == 'project = "$:project_name:"'
        assert lines[23] == 'copyright = "$:project_year:, $:author_name:"'
        assert lines[24] == 'author = "$:author_name:"'
        assert lines[27] == "release = $:project_slug:.__version__"


def test_build_no_files(template: Template) -> None:
    with pytest.raises(errors.TemplateError) as exc:
        template.build(set(), "Testarossa Generic")
    assert str(exc.value) == "No files provided"


def test_build_store_profile(
    template: Template, generic_files: set[Path], profile: Profile
) -> None:
    template.build(
        generic_files, "Testarossa Generic", profile=profile, store_profile=True
    )
    assert template.profile_data == {
        "author_name": "Barney",
        "author_nick": "$:NULL:",
        "author_email": "purplebarney@example.com",
        "preferred_language": "$:NULL:",
        "starting_version": "$:NULL:",
        "preferred_license": "$:NULL:",
        "version_control_url": "$:NULL:",
        "docs_url": "$:NULL:",
        "ci_url": "$:NULL:",
    }


def test_build_non_registered_blueprint(
    template: Template, generic_files: set[Path]
) -> None:
    with pytest.raises(errors.InvalidBlueprint) as exc:
        template.build(generic_files, "Testarossa Generic", blueprint="invalid")
    assert str(exc.value).startswith(
        "'invalid' is not a registered blueprint (choose between:"
    )


def test_build_not_blueprint_subclass(
    template: Template, generic_files: set[Path]
) -> None:
    with pytest.raises(errors.InvalidBlueprint) as exc:
        template.build(generic_files, "Testarossa Generic", blueprint=Profile)  # type: ignore
    assert str(exc.value) == "Blueprint class must be a subclass of `Blueprint`"


def test_build_invalid_blueprint_object(
    template: Template, generic_files: set[Path], profile: Profile
) -> None:
    with pytest.raises(errors.InvalidBlueprint) as exc:
        template.build(generic_files, "Testarossa Generic", blueprint=profile)  # type: ignore
    assert str(exc.value) == "Invalid blueprint object"


def test_build_with_dependencies(template: Template, generic_files: set[Path]) -> None:
    d = ["nusex", "analytix", "len8"]
    template.build(
        generic_files, "Testarossa Generic", blueprint="generic", dependencies=d
    )
    assert template.dependencies == d


def test_deploy_no_slug(template: Template, generic_files: set[Path]) -> None:
    template.build(generic_files, "Testarossa Generic")
    template.deploy(to_dir=DEPLOY_DIR)

    for fn in FILENAMES:
        if "testarossa_generic" in fn:
            fn = fn.replace("testarossa_generic", "test_deploy")

        assert (DEPLOY_DIR / fn).is_file()
        os.remove(DEPLOY_DIR / fn)


def test_deploy_set_slug(template: Template, generic_files: set[Path]) -> None:
    template.build(generic_files, "Testarossa Generic")
    template.deploy(
        to_dir=DEPLOY_DIR, project_name="Test Deploy", project_slug="my_testing_app"
    )

    for fn in FILENAMES:
        if "testarossa_generic" in fn:
            fn = fn.replace("testarossa_generic", "my_testing_app")

        assert (DEPLOY_DIR / fn).is_file()
        # We don't remove here because the next test requires the files
        # there there.
        # os.remove(DEPLOY_DIR / fn)


def test_deploy_set_slug_no_name(template: Template, generic_files: set[Path]) -> None:
    template.build(generic_files, "Testarossa Generic")
    with pytest.raises(errors.TemplateError) as exc:
        template.deploy(to_dir=DEPLOY_DIR, project_slug="my_testing_app")
    assert str(exc.value) == "You cannot specify a project slug without a project name"


def test_deploy_exists(template: Template, generic_files: set[Path]) -> None:
    template.build(generic_files, "Testarossa Generic")
    with pytest.raises(FileExistsError) as exc:
        template.deploy(to_dir=DEPLOY_DIR)
    assert str(exc.value) == "Template would overwrite existing files"


def test_deploy_exists_force(template: Template, generic_files: set[Path]) -> None:
    template.build(generic_files, "Testarossa Generic")
    template.deploy(to_dir=DEPLOY_DIR, force=True)

    for fn in FILENAMES:
        if "testarossa_generic" in fn:
            fn = fn.replace("testarossa_generic", "test_deploy")

        assert (DEPLOY_DIR / fn).is_file()
        os.remove(DEPLOY_DIR / fn)


def test_deploy_static(template: Template, generic_files: set[Path]) -> None:
    template.build(generic_files, "Testarossa Generic")
    template.deploy(to_dir=DEPLOY_DIR)

    for fn in FILENAMES:
        if "testarossa_generic" in fn:
            fn = fn.replace("testarossa_generic", "test_deploy")

        assert (DEPLOY_DIR / fn).is_file()

    for key in ("README", "README.md", "README.txt"):
        lines = template.files[key].decode().splitlines()
        assert lines[0] == "# Testarossa Generic"
        assert lines[6 if key == "README" else -1] != blueprints.generic.ACK

    for key in ("CONTRIBUTING", "CONTRIBUTING.md"):
        body = template.files[key].decode()
        assert body == "Thanks for contributing to Testarossa Generic!\n"

    for key in ("docs/conf.py", "docs/source/conf.py"):
        lines = template.files[key].decode().splitlines()
        assert lines[15] == "import testarossa_generic"
        assert lines[22] == 'project = "Testarossa Generic"'
        assert lines[23] == f'copyright = "2021, Barney"'
        assert lines[24] == 'author = "Barney"'
        assert lines[27] == "release = testarossa_generic.__version__"


def test_deploy_generic_given_profile(
    template: Template, generic_files: set[Path]
) -> None:
    profile = Profile("test", author_name="Barney")
    template.build(generic_files, "Testarossa Generic", blueprint="generic")
    template.deploy(
        to_dir=DEPLOY_DIR, project_name="Test Deploy", profile=profile, force=True
    )

    for key in ("README", "README.md", "README.txt"):
        lines = Path(DEPLOY_DIR / key).read_text().splitlines()
        assert lines[0] == "# Test Deploy"
        assert lines[6 if key == "README" else -1] == blueprints.generic.ACK

    for key in ("CONTRIBUTING", "CONTRIBUTING.md"):
        body = Path(DEPLOY_DIR / key).read_text()
        assert body == "Thanks for contributing to Test Deploy!\n"

    for key in ("docs/conf.py", "docs/source/conf.py"):
        lines = Path(DEPLOY_DIR / key).read_text().splitlines()
        assert lines[15] == "import test_deploy"
        assert lines[22] == 'project = "Test Deploy"'
        assert lines[23] == f'copyright = "{YEAR}, Barney"'
        assert lines[24] == 'author = "Barney"'
        assert lines[27] == "release = test_deploy.__version__"

    for fn in FILENAMES:
        if "testarossa_generic" in fn:
            fn = fn.replace("testarossa_generic", "test_deploy")

        assert (DEPLOY_DIR / fn).is_file()
        os.remove(DEPLOY_DIR / fn)


def test_deploy_generic_stored_profile(
    template: Template, generic_files: set[Path]
) -> None:
    profile = Profile("test", author_name="Barney")
    template.build(
        generic_files,
        "Testarossa Generic",
        blueprint="generic",
        profile=profile,
        store_profile=True,
    )
    template.deploy(
        to_dir=DEPLOY_DIR, project_name="Test Deploy", use_stored_data=True, force=True
    )

    for key in ("README", "README.md", "README.txt"):
        lines = Path(DEPLOY_DIR / key).read_text().splitlines()
        assert lines[0] == "# Test Deploy"
        assert lines[6 if key == "README" else -1] == blueprints.generic.ACK

    for key in ("CONTRIBUTING", "CONTRIBUTING.md"):
        body = Path(DEPLOY_DIR / key).read_text()
        assert body == "Thanks for contributing to Test Deploy!\n"

    for key in ("docs/conf.py", "docs/source/conf.py"):
        lines = Path(DEPLOY_DIR / key).read_text().splitlines()
        assert lines[15] == "import test_deploy"
        assert lines[22] == 'project = "Test Deploy"'
        assert lines[23] == f'copyright = "{YEAR}, Barney"'
        assert lines[24] == 'author = "Barney"'
        assert lines[27] == "release = test_deploy.__version__"

    for fn in FILENAMES:
        if "testarossa_generic" in fn:
            fn = fn.replace("testarossa_generic", "test_deploy")

        assert (DEPLOY_DIR / fn).is_file()
        os.remove(DEPLOY_DIR / fn)
