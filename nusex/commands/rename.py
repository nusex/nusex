import os
import re

from nusex import CONFIG_DIR

from ..errors import NoMatchingTemplates, TemplateRenameError

NAME_REGEX = re.compile("[^a-z0-9_]+")


def run(old_name, new_name):
    if not os.path.isfile(CONFIG_DIR / f"{old_name}.nsx"):
        raise NoMatchingTemplates(f"no template named '{old_name}' exists")
    if NAME_REGEX.search(new_name):
        raise TemplateRenameError(
            "template names can only contain lower case letters, numbers, "
            "and underscores"
        )

    os.rename(CONFIG_DIR / f"{old_name}.nsx", CONFIG_DIR / f"{new_name}.nsx")
    print(
        f"🎉 Template successfully renamed from '{old_name}' to '{new_name}'!"
    )


def setup(subparsers):
    s = subparsers.add_parser("rename", description="Rename a template.")
    s.add_argument("old_name", help="the name of the template to rename")
    s.add_argument("new_name", help="the new name for the template")
    return subparsers
