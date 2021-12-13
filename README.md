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

## Features

* An easy-to-use command-line interface
* A powerful API for application developers
* Smart templating to populate projects with relevant information
* A profile system for those who maintain personal and organisation-owned projects
* Premade templates to get started with
* Minimal dependencies, unlike many other templating utilities
* Support for CPython and PyPy 3.7 and up on all OSes

## Installation

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
template.deploy("/path/to/deploy", project_name="New Project", profile=profile)
```

Have a look at the [documentation](https://nusex.readthedocs.io) to find out more.

## What is "smart templating"?

When building templates, *nusex* replaces various parts of specific files with placeholder variables, which are then replaced with profile data when deployed. The files checked are dependent on the blueprint used, so for example, using the Python blueprint would give different results than using the Rust one.

It is important to note that the source files are **not** modified; the files are loaded into memory beforehand.

Consider the following file:

```py
# mymodule/__init__.py

__productname__ = "My Module"
__version__ = "1.0.0"
__author__ = "Barney the Dinosaur"
```

*nusex* checks the main \_\_init\_\_.py file of the project, and looks out for specific dunder variables, such as the three above. Each dunder variable that has a suitable placeholder variable (things like \_\_all\_\_ do not have one, and so are left alone) has its value replaced. The above file would become this:

```py
# mymodule/__init__.py

__productname__ = "$:project_name:"
__version__ = "$:starting_version:"
__author__ = "$:author_name:"
```

When deploying, *nusex* simply replaces these placeholder variables with data from the given profile, or data it infers from the current environment.

## Contributing

Contributions are very much welcome! To get started:

* Familiarise yourself with the [code of conduct](https://github.com/nusex/nusex/blob/main/CODE_OF_CONDUCT.md)
* Have a look at the [contributing guide](https://github.com/nusex/nusex/blob/main/CONTRIBUTING.md)

## License

The *nusex* module for Python is licensed under the [BSD 3-Clause License](https://github.com/nusex/nusex/blob/main/LICENSE).
