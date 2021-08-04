# nusex

[![PyPi version](https://img.shields.io/pypi/v/nusex.svg)](https://pypi.python.org/pypi/nusex/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/nusex.svg)](https://pypi.python.org/pypi/nusex/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/nusex)](https://pypi.python.org/pypi/nusex/)
[![PyPI - Status](https://img.shields.io/pypi/status/nusex)](https://pypi.python.org/pypi/nusex/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/nusex)](https://pypistats.org/packages/nusex)

[![Maintenance](https://img.shields.io/maintenance/yes/2021)](https://github.com/parafoxia/nusex)
[![GitHub Release Date](https://img.shields.io/github/release-date/parafoxia/nusex)](https://github.com/parafoxia/nusex)
[![GitHub last commit](https://img.shields.io/github/last-commit/parafoxia/nusex)](https://github.com/parafoxia/nusex)
[![Read the Docs](https://img.shields.io/readthedocs/nusex)](https://nusex.readthedocs.io/en/latest/index.html)
[![License](https://img.shields.io/github/license/parafoxia/nusex.svg)](https://github.com/parafoxia/nusex/blob/main/LICENSE)

A project templating utility for Python.

## Features

- An easy-to-use CLI (command-line interface)
- Premade templates for applications and packages
- The ability to use context clues to dynamically generate files
- Options to ignore file extensions and directories when building templates
- No dependencies!

## Installation

**You need Python 3.6.0 or greater to run nusex.**

To install the latest stable version of nusex, use the following command:
```sh
pip install nusex
```

You can also install the latest development version using the following command:
```sh
pip install git+https://github.com/parafoxia/nusex.git@develop
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

nusex is open to contributions. To find out where to get started, have a look at the [contributing guide](https://github.com/parafoxia/nusex/blob/main/CONTRIBUTING.md).

## License

The nusex module for Python is licensed under the [BSD 3-Clause License](https://github.com/parafoxia/nusex/blob/main/LICENSE).
