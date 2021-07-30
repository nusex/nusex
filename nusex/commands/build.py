import os
import json
import re
from pathlib import Path

from nusex import CONFIG_DIR

from ..errors import TemplateBuildError

NAME_REGEX = re.compile("[^a-z0-9_]+")
PNAME_SPECIAL_FILES = (
    "MANIFEST.in",
    "pyproject.toml",
    "README.md",
    "setup.py",
)
INIT_VAR_MAPPING = {
    "__productname__": '"PROJECTNAME"',
    "__version__": '"PROJECTVERSION"',
    "__description__": '"PROJECTDESCRIPTION"',
    "__url__": '"PROJECTURL"',
    "__docs__": '"https://PROJECTNAME.readthedocs.io/en/latest/"',
    "__author__": '"PROJECTAUTHOR"',
    "__author_email__": '"PROJECTAUTHOREMAIL"',
    "__license__": '"PROJECTLICENSE"',
    "__bugtracker__": '"PROJECTURL/issues"',
}


def _gather_files(path, ignore_exts, ignore_dirs):
    print("⌛ Gathering files...", end="")

    def _check(p):
        return (
            p.is_file()
            and p.suffix[1:] not in ignore_exts
            and not any(d in f"{p}".split("/")[:-1] for d in ignore_dirs)
        )

    files = filter(lambda p: _check(p), path.rglob("*"))
    print(" done")
    return list(files)


def _build_template(files):
    print("⌛ Building template...", end="")
    project_name = Path(".").resolve().parts[-1]
    template = {
        "files": {
            f"{f}".replace(project_name, "PROJECTNAME"): f.read_text()
            for f in files
        },
    }

    with open(CONFIG_DIR / "user.nsc") as f:
        user_config = json.load(f)

    # Handle the __init__ file, if present
    init_text = template["files"].get("PROJECTNAME/__init__.py", None)
    if init_text:
        init_data = template["files"]["PROJECTNAME/__init__.py"].split("\n")
        init = {}
        for i, line in enumerate(init_data[:]):
            if line.startswith("__"):
                key, value = line.split(" = ")
                init.update({key: value.strip('"').strip("'")})

        for k, v in INIT_VAR_MAPPING.items():
            data = init.get(k, None)
            if data:
                init[k] = v

        var_data = "\n".join(f"{k} = {v}" for k, v in init.items())
        init_text = f"{var_data}\n" + "\n".join(init_data[len(init) :])
        template["files"]["PROJECTNAME/__init__.py"] = init_text

    # Handle other files, if present
    for fname in PNAME_SPECIAL_FILES:
        data = template["files"].get(fname, None)
        if data:
            template["files"][fname] = template["files"][fname].replace(
                project_name, "PROJECTNAME"
            )

    # Handle license separately
    data = template["files"].get("LICENSE", None)
    if data:
        template["files"]["LICENSE"] = template["files"]["LICENSE"].replace(
            user_config["author"], "PROJECTAUTHOR"
        )

    print(" done")
    return template


def run(name, overwrite, ignore_exts, ignore_dirs):
    if NAME_REGEX.search(name):
        raise TemplateBuildError(
            "template names can only contain lower case letters, numbers, "
            "and underscores"
        )
    if os.path.isfile(CONFIG_DIR / f"{name}.nsx"):
        if not overwrite:
            overwrite = input(
                "🎤 A template with that name already exists. Overwrite? "
            )
            if overwrite.lower() not in ("y", "yes"):
                print("💥 Build aborted.")
                return

    ignore_exts = [x for x in ignore_exts.split(",") if x]
    ignore_dirs = [x for x in ignore_dirs.split(",") if x]
    path = Path(".")

    files = _gather_files(path, ignore_exts, ignore_dirs)
    if not files:
        raise TemplateBuildError("no usable files were found")
    template = _build_template(files)

    name = name.lower()
    with open(CONFIG_DIR / f"{name}.nsx", "w") as f:
        json.dump(template, f, ensure_ascii=False)

    print(f"🎉 Template '{name}' built successfully!")


def setup(subparsers):
    s = subparsers.add_parser(
        "build",
        description="Build a new template.",
    )
    s.add_argument("name", help="the name for the new template")
    s.add_argument(
        "-o",
        "--overwrite",
        help="overwrite an existing template should it already exist",
        action="store_true",
    )
    s.add_argument(
        "--ignore-exts",
        help=(
            "a comma separated list of file types to ignore when scanning for "
            "files (default: pyc,pyo,pyd,pyi)"
        ),
        default="pyc,pyo,pyd,pyi",
    )
    s.add_argument(
        "--ignore-dirs",
        help=(
            "a comma separated list of directories to ignore when scanning "
            "for files (default: .git,.venv,.egg-info,.nox,dist)"
        ),
        default=".git,.venv,.egg-info,.nox,dist",
    )
    return subparsers
