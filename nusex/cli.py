import argparse
import os

from . import CONFIG_DIR, commands
from .errors import NotInitialised

CMD_MAP = {
    "init": commands.init,
    "build": commands.build,
    "deploy": commands.deploy,
    "delete": commands.delete,
    "rename": commands.rename,
    "config": commands.config,
}


def main():
    parser = argparse.ArgumentParser(
        description="A project templating utility for Python."
    )
    subparsers = parser.add_subparsers(dest="subparser")

    # Init subcommand
    parser_init = subparsers.add_parser(
        "init", description="Initialise nusex."
    )

    # Build subcommand
    parser_build = subparsers.add_parser(
        "build",
        description="Build a new template.",
    )
    parser_build.add_argument("name", help="the name for the new template")
    parser_build.add_argument(
        "-o",
        "--overwrite",
        help="overwrite an existing template should it already exist",
        action="store_true",
    )
    parser_build.add_argument(
        "--ignore-exts",
        help=(
            "a comma separated list of file types to ignore when scanning for "
            "files (default: pyc,pyo,pyd,pyi)"
        ),
        default="pyc,pyo,pyd,pyi",
    )
    parser_build.add_argument(
        "--ignore-dirs",
        help=(
            "a comma separated list of directories to ignore when scanning "
            "for files (default: .git,.venv,.egg-info,.nox,dist)"
        ),
        default=".git,.venv,.egg-info,.nox,dist",
    )

    # Deploy subcommand
    parser_deploy = subparsers.add_parser(
        "deploy",
        description="Deploy an already existing template.",
    )
    parser_deploy.add_argument(
        "name", help="the name of the template to deploy"
    )

    # Delete subcommand
    parser_delete = subparsers.add_parser(
        "delete", description="Delete one or more templates."
    )
    parser_delete.add_argument(
        "names",
        help="the name(s) of the template(s) to delete",
        nargs="+",
    )

    # Rename subcommand
    parser_rename = subparsers.add_parser(
        "rename", description="Rename a template."
    )
    parser_rename.add_argument(
        "old_name", help="the name of the template to rename"
    )
    parser_rename.add_argument(
        "new_name", help="the new name for the template"
    )

    # Config subcommand
    parser_config = subparsers.add_parser(
        "config",
        description=(
            "Change your user configuration. All optional arguments default "
            "to their previous values.",
        ),
    )
    parser_config.add_argument(
        "-v",
        "--default-version",
        help="the version nusex initialises projects with",
        default="",
    )
    parser_config.add_argument(
        "-d",
        "--default-description",
        help="the description nusex initialises projects with",
        default="",
    )
    parser_config.add_argument(
        "-r",
        "--repo-user-url",
        help="your repository user URL (for example, your GitHub profile URL)",
        default="",
    )
    parser_config.add_argument(
        "-a",
        "--author",
        help="your name, or the name you want to use for your projects",
        default="",
    )
    parser_config.add_argument(
        "-e",
        "--author-email",
        help="your email, or the email of your company/organisation",
        default="",
    )
    parser_config.add_argument(
        "-l",
        "--default-license",
        help="the license nusex initialises projects with",
        default="",
    )

    # Parse
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

    CMD_MAP[args.subparser](
        **{k: v for k, v in args.__dict__.items() if k != "subparser"}
    )


if __name__ == "__main__":
    main()
