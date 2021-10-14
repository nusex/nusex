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

from nusex import TEMPLATE_DIR, Template
from nusex.errors import DeploymentError, DoesNotExist
from nusex.helpers import cprint


def run(name, force, no_installs):
    if not os.path.isfile(TEMPLATE_DIR / f"{name}.nsx"):
        raise DoesNotExist("No template with that name exists")

    if os.path.isfile("./.nusexmeta") and not force:
        raise DeploymentError("A template has already been deployed here")

    template = Template(name)
    template.deploy()
    if not no_installs:
        template.install_dependencies()

    cprint("aok", f"Template '{name}' deployed successfully!")


def setup(subparsers):
    s = subparsers.add_parser(
        "deploy", description="Deploy an existing template."
    )
    s.add_argument("name", help="the name of the template to deploy")
    s.add_argument(
        "--force",
        help=(
            "force a deployment, overwriting any existing files with the same "
            "names"
        ),
        action="store_true",
    )
    s.add_argument(
        "--no-installs",
        help="deploy the template without installing dependencies",
        action="store_true",
    )
    return subparsers
