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

import nusex
from nusex.api import blueprints

DOCS_ATTR_MAPPING = {
    "project": '"$:project_name:"',
    "copyright": '"$:project_year:, $:author_name:"',
    "author": '"$:author_name:"',
    "release": "$:project_slug:.__version__",
}
ACK = (
    "This project was created in part by the [nusex project templating utility]"
    f"({nusex.__url__})"
)


class GenericBlueprint(blueprints.Blueprint):
    @blueprints.with_files("README")
    def modify_readme(self, body: str) -> str:
        lines = body.split("\n")
        last_line = len(lines) - 1
        found_acks = False

        for i, line in enumerate(lines[:]):
            if line.startswith("#"):
                if found_acks:
                    lines.insert(i, ACK)
                    lines.insert(i + 1, "")
                    break

                if "acknowledgements" in line.lower():
                    found_acks = True

            elif i == last_line and found_acks:
                lines.extend([ACK, ""])

        if not found_acks:
            lines.extend(["## Acknowledgements", "", ACK, ""])

        return (
            "\n".join(lines)
            .replace(self.project_name, "$:project_name:")
            .replace(self.project_slug, "$:project_slug:")
        )

    @blueprints.with_files("LICEN[SC]E", "COPYING")
    def modify_license(self, _: str) -> str:
        return "PROJECTLICENSE"

    @blueprints.with_files("CONTRIBUTING")
    def modify_contributing(self, body: str) -> str:
        return body.replace(self.project_name, "$:project_name:").replace(
            self.project_slug, "$:project_slug:"
        )

    @blueprints.with_files("docs/(source/)?conf.py$")
    def modify_docs_conf(self, body: str) -> str:
        lines = body.split("\n")
        docs_mapping = blueprints.resolve_mapping(DOCS_ATTR_MAPPING, self.profile)

        in_project_info = False

        for i, line in enumerate(lines):
            if in_project_info:
                if line.startswith("# --"):
                    in_project_info = False
                    continue

                lines[i] = blueprints.apply_line_mapping(line, docs_mapping)

            elif line.startswith("# -- Project information"):
                in_project_info = True

            elif line.strip() == f"import {self.project_slug}":
                lines[i] = "import $:project_slug:"

        return "\n".join(lines)
