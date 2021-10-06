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
from pathlib import Path

from nusex import CONFIG_DIR

from ..errors import NoMatchingTemplates


def _construct_file_manifest(name):
    print("⌛ Constructing file manifest...", end="")
    with open(CONFIG_DIR / f"{name}.nsx") as f:
        template = json.load(f)
    print(" done")
    return template


def _deploy_template(template):
    def _replace_filename(text):
        return text.replace(
            "PROJECTNAME",
            project_name.lower().replace(" ", "_").replace("-", "_"),
        )

    def _replace_vars(text):
        for k, v in var_mapping.items():
            text = text.replace(k, v)
        return text

    print("⌛ Deploying template... 0%", end="\r")
    project_name = Path(".").resolve().parts[-1]
    step = 100 / len(template["files"])

    with open(CONFIG_DIR / "user.nsc") as f:
        user_config = json.load(f)
    var_mapping = {
        "PROJECTNAME": project_name,
        "PROJECTVERSION": user_config["default_version"],
        "PROJECTDESCRIPTION": user_config["default_description"],
        "PROJECTURL": user_config["repo_user_url"] + f"/{project_name}",
        "PROJECTAUTHOREMAIL": user_config["author_email"],
        "PROJECTAUTHOR": user_config["author"],
        "PROJECTLICENSE": user_config["default_license"],
    }

    for i, (file, data) in enumerate(template["files"].items()):
        file = _replace_filename(file)
        data = _replace_vars(data)

        dirs = file.split("/")[:-1]
        if dirs:
            os.makedirs("/".join(dirs), exist_ok=True)

        with open(file, "w") as f:
            f.write(data)

        print(f"⌛ Deploying template... {step * (i + 1):.0f}%", end="\r")


def run(name):
    if not os.path.isfile(CONFIG_DIR / f"{name}.nsx"):
        raise NoMatchingTemplates(f"no template named '{name}' exists")

    template = _construct_file_manifest(name)
    _deploy_template(template)
    print(f"\n🎉 Template '{name}' deployed successfully!")


def setup(subparsers):
    s = subparsers.add_parser(
        "deploy",
        description="Deploy an already existing template.",
    )
    s.add_argument("name", help="the name of the template to deploy")
    return subparsers
