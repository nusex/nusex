import json

from nusex import CONFIG_DIR


def _update_config(**kwargs):
    print("⌛ Updating config...", end="")
    with open(CONFIG_DIR / "user.nsc") as f:
        data = json.load(f)

    for k, v in kwargs.items():
        if v:
            data[k] = v

    with open(CONFIG_DIR / "user.nsc", "w") as f:
        json.dump(data, f, ensure_ascii=False)
    print(" done")


def run(**kwargs):
    _update_config(**kwargs)
    print("🎉 User config updated!")


def setup(subparsers):
    s = subparsers.add_parser(
        "config",
        description=(
            "Change your user configuration. All optional arguments default "
            "to their previous values."
        ),
    )
    s.add_argument(
        "-v",
        "--default-version",
        help="the version nusex initialises projects with",
        default="",
    )
    s.add_argument(
        "-d",
        "--default-description",
        help="the description nusex initialises projects with",
        default="",
    )
    s.add_argument(
        "-r",
        "--repo-user-url",
        help="your repository user URL (for example, your GitHub profile URL)",
        default="",
    )
    s.add_argument(
        "-a",
        "--author",
        help="your name, or the name you want to use for your projects",
        default="",
    )
    s.add_argument(
        "-e",
        "--author-email",
        help="your email, or the email of your company/organisation",
        default="",
    )
    s.add_argument(
        "-l",
        "--default-license",
        help="the license nusex initialises projects with",
        default="",
    )
    return subparsers
