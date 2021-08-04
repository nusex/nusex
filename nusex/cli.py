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
