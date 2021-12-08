# nusex

[![PyPi version](https://img.shields.io/pypi/v/nusex.svg)](https://pypi.python.org/pypi/nusex/)
[![PyPI - Status](https://img.shields.io/pypi/status/nusex)](https://pypi.python.org/pypi/nusex/)
[![Downloads](https://pepy.tech/badge/nusex)](https://pepy.tech/project/nusex)
[![GitHub last commit](https://img.shields.io/github/last-commit/nusex/nusex)](https://github.com/nusex/nusex)
[![License](https://img.shields.io/github/license/nusex/nusex.svg)](https://github.com/nusex/nusex/blob/main/LICENSE)

[![CI](https://github.com/nusex/nusex/actions/workflows/ci.yml/badge.svg)](https://github.com/nusex/nusex/actions/workflows/ci.yml)
[![Read the Docs](https://img.shields.io/readthedocs/nusex)](https://nusex.readthedocs.io/en/latest/index.html)
[![Maintainability](https://api.codeclimate.com/v1/badges/5122e8a19a45b39f8945/maintainability)](https://codeclimate.com/github/nusex/nusex/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/5122e8a19a45b39f8945/test_coverage)](https://codeclimate.com/github/nusex/nusex/test_coverage)

A dynamic, multi-language project templating utility.

CPython 3.7 through 3.11-dev and PyPy 3.7 and 3.8 are officially supported on all operating systems.

## Features

- An easy-to-use CLI (command-line interface)
- Dynamic templating using placeholder variables
- Template add-ons for use during the whole development lifecycle
- A profile system for those who maintain personal and organisation-owned projects
- Automatic dependency installation
- Premade templates for applications and packages
- Minimal dependencies

## Installation

**You need Python 3.7.0 or greater to run nusex.** If you need support for Python 3.6, you'll need to install nusex 1.2. No other Python versions were ever supported.

To install the latest stable version of nusex, use the following command:
```sh
pip install nusex
```

You can also install the latest development version using the following command:
```sh
pip install git+https://github.com/nusex/nusex
```

You may need to prefix these commands with a call to the Python interpreter depending on your OS and Python configuration.

## Quickstart

Before you can build and deploy templates with nusex, you need to initialise it. You only need to do this once, and not for every new project. To initialise nusex, use the following command:

```sh
nusex init
```

Some premade templates will be downloaded for you to experiment with. You can deploy these templates with the following command(s):
```sh
# For general applications
nusex deploy nsx_simple_app

# For PyPI packages
nusex deploy nsx_simple_pkg
```

To learn how to build templates of your own, [read the documentation](https://nusex.readthedocs.io/en/latest/).

## Contributing

nusex is open to contributions. To find out where to get started, have a look at the [contributing guide](https://github.com/nusex/nusex/blob/main/CONTRIBUTING.md).

## License

The nusex module for Python is licensed under the [BSD 3-Clause License](https://github.com/nusex/nusex/blob/main/LICENSE).
