import os

from nusex import CONFIG_DIR


def run(old_name, new_name):
    os.rename(CONFIG_DIR / f"{old_name}.nsx", CONFIG_DIR / f"{new_name}.nsx")
    print(
        f"🎉 Template successfully renamed from '{old_name}' to '{new_name}'!"
    )


def setup(subparsers):
    s = subparsers.add_parser("rename", description="Rename a template.")
    s.add_argument("old_name", help="the name of the template to rename")
    s.add_argument("new_name", help="the new name for the template")
    return subparsers
