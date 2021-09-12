# nusex

[![PyPi version](https://img.shields.io/pypi/v/nusex.svg)](https://pypi.python.org/pypi/nusex/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/nusex.svg)](https://pypi.python.org/pypi/nusex/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/nusex)](https://pypi.python.org/pypi/nusex/)
[![PyPI - Status](https://img.shields.io/pypi/status/nusex)](https://pypi.python.org/pypi/nusex/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/nusex)](https://pypistats.org/packages/nusex)

[![Maintenance](https://img.shields.io/maintenance/yes/2021)](https://github.com/nusex/nusex)
[![GitHub Release Date](https://img.shields.io/github/release-date/nusex/nusex)](https://github.com/nusex/nusex)
[![GitHub last commit](https://img.shields.io/github/last-commit/nusex/nusex)](https://github.com/nusex/nusex)
[![Read the Docs](https://img.shields.io/readthedocs/nusex)](https://nusex.readthedocs.io/en/latest/index.html)
[![License](https://img.shields.io/github/license/nusex/nusex.svg)](https://github.com/nusex/nusex/blob/main/LICENSE)

A project templating utility for Python.

## Important note

v1.0.0.dev0 is only available as a preview/evaluation build, and **CAN NOT** be used in development environments. It is recommended that you back up your current nusex config before experimenting with this version.

## Features

- An easy-to-use CLI (command-line interface)
- Dynamic templating using placeholder variables
- Template extensions for use during the whole development lifecycle
- A profile system for those who maintain personal and organisation-owned projects
- Automatic dependency installation
- Premade templates for applications and packages
- No dependencies!

## Installation

**You need Python 3.6.0 or greater to run nusex.**

To install the latest stable version of nusex, use the following command:
```sh
pip install nusex
```

You can also install the latest development version using the following command:
```sh
pip install git+https://github.com/nusex/nusex@develop
```

You may need to prefix these commands with a call to the Python interpreter depending on your OS and Python configuration.

## Quickstart

Before you can build and deploy templates with nusex, you need to initialise it. You only need to do this once, and not for every new project. To initialise nusex, use the following command:

```sh
nsx init
```

Some premade templates will be downloaded for you to experiment with. You can deploy these templates with the following command(s):
```sh
# For general applications
nsx deploy simple_app

# For PyPI packages
nsx deploy simple_pkg
```

To learn how to build templates of your own, [read the documentation](https://nusex.readthedocs.io/en/latest/).

## Contributing

nusex is open to contributions. To find out where to get started, have a look at the [contributing guide](https://github.com/nusex/nusex/blob/main/CONTRIBUTING.md).

## License

The nusex module for Python is licensed under the [BSD 3-Clause License](https://github.com/nusex/nusex/blob/main/LICENSE).
