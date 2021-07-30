import os

from nusex import CONFIG_DIR


def _delete_templates(names):
    print("⌛ Deleting templates... 0%", end="\r")
    step = 100 / len(names)

    for i, name in enumerate(names):
        try:
            os.remove(CONFIG_DIR / f"{name}.nsx")
        except FileNotFoundError:
            print(f"💥 WARNING: no template named '{name}' exists")
        print(f"⌛ Deleting templates... {step * (i + 1):.0f}%", end="\r")


def run(names):
    _delete_templates(names)
    print("\n🎉 Template(s) deleted successfully!")


def setup(subparsers):
    s = subparsers.add_parser(
        "delete", description="Delete one or more templates."
    )
    s.add_argument(
        "names",
        help="the name(s) of the template(s) to delete",
        nargs="+",
    )
    return subparsers
