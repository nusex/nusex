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
import sys
import traceback
from importlib import import_module
from pathlib import Path

from nusex import CONFIG_DIR, __description__, __version__
from nusex.errors import NusexError, NusexUserError
from nusex.helpers import cprint

COMMAND_MAPPING = {
    p.stem: import_module(f".cli.commands.{p.stem}", package="nusex")
    for p in Path(__file__).parent.glob("commands/*.py")
    if p.stem != "__init__"
}

parser = argparse.ArgumentParser(description=__description__)
parser.add_argument(
    "-v",
    "--version",
    help="show nusex's version and exit",
    action="store_true",
)
subparsers = parser.add_subparsers(dest="subparser")
for module in COMMAND_MAPPING.values():
    subparsers = module.setup(subparsers)  # type: ignore


def main():
    args = parser.parse_args()

    # NOTE: Remove in v1.1.
    if parser.prog == "nsx":
        cprint(
            "war",
            (
                "The 'nsx' command is deprecated, and will be removed in v1.1 "
                "(use 'nusex' instead)."
            ),
        )

    if args.version:
        return print(__version__)

    if not args.subparser:
        return parser.parse_args(("-h",))

    # Setup checks.
    if (CONFIG_DIR / "user.nsc").exists() and args.subparser != "migrate":
        cprint(
            "err",
            "It looks like you still have an old nusex configuration. Use "
            "`nusex migrate` to fix this.",
        )
        sys.exit(2)
    elif not (CONFIG_DIR / "config.nsc").exists() and args.subparser not in (
        "init",
        "migrate",
    ):
        cprint(
            "err",
            "That command cannot be run before nusex has been initialised.",
        )
        sys.exit(2)

    # Command runs.
    try:
        COMMAND_MAPPING[args.subparser].run(
            **{
                k: v
                for k, v in args.__dict__.items()
                if k not in ("subparser", "version")
            }
        )
    except NusexUserError as exc:
        cprint("err", f"{exc}.")
        sys.exit(2)
    except NusexError as exc:
        cprint("err", f"{exc}.")
        sys.exit(1)
    except KeyboardInterrupt as exc:
        sys.exit(130)
    except Exception as exc:
        cprint(
            "err",
            f"Oh no! Something went wrong.\n\n{traceback.format_exc()}",
            end="",
        )


if __name__ == "__main__":
    main()
