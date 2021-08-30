from pathlib import Path

import nox


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
def check_licensing(session: nox.Session) -> None:
    missing = []

    for p in (Path(__file__).parent / "nusex").rglob("*.py"):
        with open(p) as f:
            if not f.read().startswith("# Copyright (c)"):
                missing.append(p)

    if missing:
        session.error(
            f"\n{len(missing):,} file(s) are missing their licenses:\n"
            + "\n".join(f" - {file}" for file in missing)
        )
