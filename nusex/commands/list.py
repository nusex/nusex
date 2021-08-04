import os
import sys

from nusex import CONFIG_DIR

# Yeet!
_filter = filter


def run(filter):
    files = [
        f.split(".")[0]
        for f in _filter(
            lambda g: g.endswith(".nsx") and filter in g,
            os.listdir(CONFIG_DIR),
        )
    ]
    if not files:
        print("💥 No templates found!")
        sys.exit(1)

    print(
        "🔔 Your templates:\n   "
        + "\n   ".join(sorted(files))
        + f"\n\n🎉 Showing {len(files):,} templates."
    )


def setup(subparsers):
    s = subparsers.add_parser(
        "list", description="Display a list of your templates."
    )
    s.add_argument(
        "-f",
        "--filter",
        help="a term to filter your templates by",
        default="",
    )
    return subparsers
