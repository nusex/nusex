import argparse
import os

from . import CONFIG_DIR, commands
from .errors import NotInitialised

CMD_MAP = {
    "init": commands.init,
    "build": commands.build,
    "deploy": commands.deploy,
}


def main():
    parser = argparse.ArgumentParser(
        description="A project templating utility for Python."
    )
    subparsers = parser.add_subparsers(dest="subparser")

    parser_init = subparsers.add_parser(
        "init", description="Initialise nusex."
    )

    parser_new = subparsers.add_parser(
        "build",
        description="Create a new template.",
    )
    parser_new.add_argument("name", help="the name for the new template")
    parser_new.add_argument(
        "--ignore-exts",
        help="a comma separated list of file types to ignore when scanning for files",
        default="pyc,pyo,pyd,pyi",
    )
    parser_new.add_argument(
        "--ignore-dirs",
        help="a comma separated list of directories to ignore when scanning for files",
        default=".git,.venv,.egg-info,.nox,dist",
    )

    parser_use = subparsers.add_parser(
        "deploy",
        description="Deploy an already existing template.",
    )
    parser_use.add_argument("name", help="the name of the template to use.")

    args = parser.parse_args()

    if args.subparser != "init":
        if not os.path.isdir(CONFIG_DIR):
            raise NotInitialised(
                "that command cannot be run before nusex has been initialised. Run `nsx init` to resolve."
            )

    CMD_MAP[args.subparser](
        **{k: v for k, v in args.__dict__.items() if k != "subparser"}
    )


if __name__ == "__main__":
    main()
