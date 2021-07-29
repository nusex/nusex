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

- :code:`name` (str): the name of the template to deploy

config
======

Change your user configuration. All optional arguments default to their previous values.

Optional:

- :code:`-v`, :code:`--default-version` (str): the version nusex initialises projects with
- :code:`-d`, :code:`--default-description` (str): the description nusex initialises projects with
- :code:`-r`, :code:`--repo-user-url` (str): your profile URL for your repository manager (for example, your GitHub profile URL)
- :code:`-a`, :code:`--author` (str): your name, or the name you want to use for your projects
- :code:`-e`, :code:`--author-email` (str): your email, or the email of your company/organisation
- :code:`-l`, :code:`--default-license` (str): the license nusex initialises projects with

rename
======

Rename a template.

Required:

- :code:`old_name` (str): the name of the template you want to rename
- :code:`new_name` (str): the new name for the template
