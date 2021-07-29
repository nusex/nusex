Command reference
#################

init
====

Initialise nusex.

build
=====

Build a new template.

Required:

- :code:`name` (str): the name for the new template

Optional:

- :code:`-o`, :code:`--overwrite` (flag): overwrite an existing template should it already exist
- :code:`--ignore-exts` (str): a comma separated list of file types to ignore when scanning for files (default: pyc,pyo,pyd,pyi)
- :code:`--ignore-dirs` (str): a comma separated list of directories to ignore when scanning for files (default: .git,.venv,.egg-info,.nox,dist)

deploy
======

Deploy an already existing template.

Required:

- :code:`name` (str): the name of the template to use
