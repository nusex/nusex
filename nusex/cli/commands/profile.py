import os

from nusex import PROFILE_DIR, Profile
from nusex.errors import *
from nusex.helpers import cprint


def _build_profile(name):
    if os.path.isfile(PROFILE_DIR / f"{name}.nsp"):
        raise AlreadyExists("A profile with that name already exists")

    profile = Profile(name)
    profile.setup()
    profile.save()
    profile.select()
    cprint("aok", f"Profile '{profile.name}' successfully created!")


def run(show_current, create_new, switch, **kwargs):
    if show_current:
        return print(Profile.current().name)

    if create_new:
        return _build_profile(create_new)

    if switch:
        profile = Profile(switch)
        profile.select()
        return cprint("aok", f"Switched to profile '{profile}'!")

    profile = Profile.current()

    if any(kwargs.values()):
        profile.update(**kwargs)
        profile.save()
        return cprint("aok", f"Profile '{profile}' updated!")

    profile.setup()
    profile.save()
    cprint("aok", f"Profile '{profile}' updated!")


def setup(subparsers):
    s = subparsers.add_parser(
        "profile",
        description="Create, modify and switch user profiles.",
    )
    s.add_argument(
        "-c",
        "--show-current",
        help="show the currently selected profile",
        action="store_true",
    )
    s.add_argument(
        "-n",
        "--create-new",
        help="create a new profile",
        metavar="PROFILE_NAME",
        default="",
    )
    s.add_argument(
        "-s",
        "--switch",
        help="switch to a different profile",
        metavar="PROFILE_NAME",
        default="",
    )
    s.add_argument(
        "-a",
        "--author-name",
        help="change your author name",
        default="",
    )
    s.add_argument(
        "-e",
        "--author-email",
        help="change your author email",
        default="",
    )
    s.add_argument(
        "-g",
        "--git-profile-url",
        help="change your Git profile URL",
        default="",
    )
    s.add_argument(
        "-v",
        "--starting-version",
        help="change your starting version",
        default="",
    )
    s.add_argument(
        "-d",
        "--default-description",
        help="change your default description",
        default="",
    )
    s.add_argument(
        "-l",
        "--preferred-license",
        help="change your preferred license",
        default="",
    )
    return subparsers
