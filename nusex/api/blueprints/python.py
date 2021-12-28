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

from nusex.api import blueprints

INIT_ATTR_MAPPING = {
    "__productname__": '"$:project_name:"',
    "__version__": '"$:starting_version:"',
    "__description__": '"My project, created using nusex."',
    "__url__": '"$:version_control_url:"',
    "__docs__": '"$:docs_url:"',
    "__author__": '"$:author_name:"',
    "__author_email__": '"$:author_email:"',
    "__license__": '"$:preferred_license:"',
    "__bugtracker__": '"$:version_control_url:/issues"',
    "__ci__": '"$:ci_url:"',
}
PYPROJECT_ATTR_MAPPING = {
    "name": '"$:project_name:"',
    "version": '"$:starting_version:"',
    "description": '"My project, created using nusex."',
    "license": '"$:preferred_license:"',
    "authors": '["$:author_name: <$:author_email:>"]',
    "maintainers": '["$:author_name: <$:author_email:>"]',
    "homepage": '"$:version_control_url:"',
    "repository": '"$:version_control_url:"',
    "documentation": '"$:docs_url:"',
}


class PythonBlueprint(blueprints.GenericBlueprint):
    """A blueprint for building Python templates.

    This makes multiple additional modifications on top of the ones the
    generic blueprint makes that allow for the easy creation of Python
    projects.
    """

    @blueprints.with_files("PROJECTSLUG/__init__.py$")
    def modify_init(self, body: str) -> str:
        """Modify the project's "\_\_init\_\_.py" file.

        Args:
            body (:obj:`str`):
                The raw contents of the file.

        Returns:
            :obj:`str`:
                The new file contents.
        """
        lines = body.splitlines()
        mapping = blueprints.resolve_mapping(INIT_ATTR_MAPPING, self.profile)

        for i, line in enumerate(lines):
            if not line.startswith("__"):
                continue

            lines[i] = blueprints.apply_line_mapping(line, mapping)

        return self.replace_names("\n".join(lines))

    @blueprints.with_files("pyproject.toml$")
    def modify_pyproject(self, body: str) -> str:
        """Modify the "pyproject.toml" file in the root directory.

        Args:
            body (:obj:`str`):
                The raw contents of the file.

        Returns:
            :obj:`str`:
                The new file contents.
        """
        lines = body.splitlines()
        mapping = blueprints.resolve_mapping(PYPROJECT_ATTR_MAPPING, self.profile)

        in_tool_poetry = False

        for i, line in enumerate(lines):
            if in_tool_poetry:
                if line.startswith("["):
                    in_tool_poetry = False
                    continue

                lines[i] = blueprints.apply_line_mapping(line, mapping)

            elif line.strip() == "[tool.poetry]":
                in_tool_poetry = True

        return self.replace_names("\n".join(lines))

    @blueprints.with_files("MANIFEST.in$", "setup.(cfg|py)$")
    def modify_other_files(self, body: str) -> str:
        """Modify the "MANIFEST.in" file, and any setup files.

        Args:
            body (:obj:`str`):
                The raw contents of the file.

        Returns:
            :obj:`str`:
                The new file contents.
        """
        # TODO: Make the setup files more complete:
        # https://docs.python.org/3/distutils/setupscript.html
        return self.replace_names(body)

    @blueprints.with_files("requirements.*\.txt$")
    def modify_requirements_files(self, body: str) -> str:
        """Modify any requirements files.

        Args:
            body (:obj:`str`):
                The raw contents of the file.

        Returns:
            :obj:`str`:
                The new file contents.
        """
        lines = body.splitlines()

        for i, line in enumerate(lines):
            if line.startswith("git+") and (
                self.project_name in line or self.project_slug in line
            ):
                lines[i] = "git+$:version_control_url:"

        return self.replace_names("\n".join(lines))

    @blueprints.with_files("PROJECTSLUG/errors?.py$")
    def modify_error_files(self, body: str) -> str:
        """Modify the errors file.

        Args:
            body (:obj:`str`):
                The raw contents of the file.

        Returns:
            :obj:`str`:
                The new file contents.
        """
        lines = body.splitlines()

        for line in lines:
            if line.startswith("class"):
                base_exc = line.split("(")[0][6:]
                break

        return "\n".join(lines).replace(base_exc, "$:project_error:")
