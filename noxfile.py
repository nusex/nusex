from pathlib import Path

import nox

LIB_DIR = Path(__file__).parent / "nusex"
TEST_DIR = Path(__file__).parent / "tests"
PY_VERSIONS = [f"3.{v}" for v in range(6, 11)]  # 3.6 - 3.10


def parse_requirements(path):
    with open(path, mode="r", encoding="utf-8") as f:
        deps = (d.strip() for d in f.readlines())
        return [d for d in deps if not d.startswith(("#", "-r"))]


DEPS = {
    name: install
    for name, install in (
        r.split("~=") for r in parse_requirements("./requirements-dev.txt")
    )
}


@nox.session(python=PY_VERSIONS, reuse_venv=True)
def tests(session: nox.Session) -> None:
    deps = parse_requirements("./requirements-test.txt")
    session.install(*deps)
    session.run("pytest", "-s", "--verbose", "--log-level=INFO")


@nox.session(reuse_venv=True)
def check_formatting(session: nox.Session) -> None:
    session.install(f"black~={DEPS['black']}")
    session.run("black", ".", "--check")


@nox.session(reuse_venv=True)
def check_imports(session: nox.Session) -> None:
    session.install(f"flake8~={DEPS['flake8']}", f"isort~={DEPS['isort']}")
    # flake8 doesn't use the gitignore so we have to be explicit.
    session.run(
        "flake8",
        "nusex",
        "tests",
        "--select",
        "F4",
        "--extend-ignore",
        "E,F,W",
        "--extend-exclude",
        "__init__.py",
    )
    session.run("isort", ".", "-cq", "--profile", "black")


@nox.session(reuse_venv=True)
def check_line_lengths(session: nox.Session) -> None:
    too_long = []
    exclude = [LIB_DIR / "__init__.py"]
    files = [p for p in LIB_DIR.rglob("*.py") if p not in exclude]
    files.extend([p for p in TEST_DIR.rglob("*.py")])

    in_docs = False

    for file in files:
        in_license = True

        with open(file) as f:
            for i, l in enumerate(f):
                if in_license:
                    if l.lstrip().startswith("#"):
                        continue

                    in_license = False

                if l.lstrip().startswith('"""') or l.lstrip().startswith(
                    'r"""'
                ):
                    in_docs = True

                limit = 72 if in_docs or l.lstrip().startswith("#") else 79
                chars = len(l.rstrip("\n"))
                if chars > limit:
                    too_long.append(
                        (
                            f"{file}".replace(f"{LIB_DIR.parent}", "..."),
                            i + 1,
                            chars,
                            limit,
                        )
                    )

                if in_docs and '"""' in l:
                    in_docs = False

    if too_long:
        session.error(
            f"\n{len(too_long):,} line(s) are too long:\n"
            + "\n".join(
                f" - {file}, line {line:,} ({chars}/{limit})"
                for file, line, chars, limit in too_long
            )
        )


@nox.session(reuse_venv=True)
def check_licensing(session: nox.Session) -> None:
    missing = []

    for p in [*LIB_DIR.rglob("*.py"), *TEST_DIR.rglob("*.py")]:
        with open(p) as f:
            if not f.read().startswith("# Copyright (c)"):
                missing.append(p)

    if missing:
        session.error(
            f"\n{len(missing):,} file(s) are missing their licenses:\n"
            + "\n".join(f" - {file}" for file in missing)
        )
