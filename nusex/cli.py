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

import argparse
import os

from . import CONFIG_DIR, commands
from .errors import NotInitialised

COMMAND_MAPPING = {
    "init": commands.init,
    "build": commands.build,
    "deploy": commands.deploy,
    "list": commands.list,
    "delete": commands.delete,
    "rename": commands.rename,
    "config": commands.config,
}

parser = argparse.ArgumentParser(
    description="A project templating utility for Python."
)
subparsers = parser.add_subparsers(dest="subparser")
for module in COMMAND_MAPPING.values():
    subparsers = module.setup(subparsers)


def main():
    args = parser.parse_args()

    if not args.subparser:
        print(
            "💥 You need to provide a subcommand. Use `nsx -h` for more "
            "information."
        )
        return

    if args.subparser != "init":
        if not os.path.isdir(CONFIG_DIR):
            raise NotInitialised(
                "that command cannot be run before nusex has been "
                "initialised. Run `nsx init` to resolve."
            )

    COMMAND_MAPPING[args.subparser].run(
        **{k: v for k, v in args.__dict__.items() if k != "subparser"}
    )


if __name__ == "__main__":
    main()
