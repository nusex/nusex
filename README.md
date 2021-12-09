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

## Installation

*nusex* is officially supported on:

* CPython 3.7 and up (incl. 3.11 development versions)
* PyPy 3.7 and up
* Windows, macOS, and Linux

To install the latest stable version of *nusex*:

```sh
pip install nusex
```

To install the latest development version:

```sh
pip install git+https://github.com/nusex/nusex
```

You may need to prefix these commands with a call to the Python interpreter
depending on your OS and Python configuration.

## Using the CLI

The CLI provides a simple and user-friendly way to use *nusex*, and is ideal for
those wishing to use *nusex* to enhance their own development experience. It
abstracts a fair amount away from you, so you may wish to use the API if you
want something more powerful.

**The CLI is not available in version 2 yet.**

## Using the API

The API provides a more powerful interface to build templates and profiles
with, and is ideal for those wishing to utilise *nusex*'s capabilities in their
own applications.

Building a basic template would look something like this:

```py
from nusex.api import Template

template = Template("template_name")
files = template.find_files(".")
excludes = template.process_excludes(files, sources=[".gitignore"])
template.build(files - excludes, "Project Name", blueprint="generic")
```

From there, you can create a profile to deploy the template with:

```py
from nusex.api import Profile

profile = Profile(
    "profile_name",
    author_name="Author Name",
    author_email="author@email.com",
    ...
)
```

Finally, you can deploy the template:

```py
template.deploy("/path/to/deploy", "New Project", profile=profile)
```

Have a look at the [documentation](https://nusex.readthedocs.io) to find out more.

## Contributing

Contributions are very much welcome! To get started:

* Familiarise yourself with the [code of conduct](https://github.com/nusex/nusex/blob/main/CODE_OF_CONDUCT.md)
* Have a look at the [contributing guide](https://github.com/nusex/nusex/blob/main/CONTRIBUTING.md)

## License

The *nusex* module for Python is licensed under the [BSD 3-Clause License](https://github.com/nusex/nusex/blob/main/LICENSE).
