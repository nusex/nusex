from pathlib import Path

import nox

LIB_DIR = Path(__file__).parent / "nusex"
TEST_DIR = Path(__file__).parent / "tests"


def parse_requirements(path):
    with open(path, mode="r", encoding="utf-8") as f:
        deps = (d.strip() for d in f.readlines())
        return [d for d in deps if not d.startswith(("#", "-r"))]


@nox.session(python=["3.6", "3.7", "3.8", "3.9", "3.10"], reuse_venv=True)
def tests(session: nox.Session) -> None:
    deps = parse_requirements("./requirements-test.txt")
    session.install(*deps)
    session.run("pytest", "-s", "--verbose", "--log-level=INFO")


@nox.session(reuse_venv=True)
def check_formatting(session: nox.Session) -> None:
    black_version = next(
        filter(
            lambda d: d.startswith("black"),
            parse_requirements("./requirements-dev.txt"),
        )
    ).split("==")[1]
    session.install(f"black=={black_version}")
    session.run("black", ".", "--check")


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
