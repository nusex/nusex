Command reference
#################

.. tip::

    You can use the :code:`-h` or :code:`--help` flags on any command to see help in the command line.

init
====

Initialise nusex.

Usage:

.. code-block:: bash

    nsx init [-h]

build
=====

Build a new template.

Usage:

.. code-block:: bash

    nsx build [-h] [-o] [--ignore-exts IGNORE_EXTS] [--ignore-dirs IGNORE_DIRS] name

Required:

- :code:`name`: the name for the new template

Optional:

- :code:`-o`, :code:`--overwrite` (flag): overwrite an existing template should it already exist
- :code:`--ignore-exts`: a comma separated list of file types to ignore when scanning for files (default: pyc,pyo,pyd,pyi)
- :code:`--ignore-dirs`: a comma separated list of directories to ignore when scanning for files (default: .git,.venv,.egg-info,.nox,dist)

.. versionchanged:: 0.2.0

    Added overwrite flag.

deploy
======

Deploy an already existing template.

Usage:

.. code-block:: bash

    nsx deploy [-h] name

Required:

- :code:`name`: the name of the template to deploy

list
====

Display a list of your templates.

Usage:

.. code-block:: bash

    nsx list [-h] [-f FILTER]

Required:

- :code:`-f`, :code:`--filter`: a term to filter your templates by

.. versionadded:: 0.3.0

delete
======

Delete one or more templates.

Usage:

.. code-block:: bash

    nsx delete [-h] names [names ...]

Required:

- :code:`names` (strs): the name(s) of the template(s) to delete

.. versionadded:: 0.2.0

rename
======

Rename a template.

Usage:

.. code-block:: bash

    nsx rename [-h] old_name new_name

Required:

- :code:`old_name`: the name of the template you want to rename
- :code:`new_name`: the new name for the template

.. versionadded:: 0.2.0

config
======

Change your user configuration.

Usage:

.. code-block:: bash

    nsx config [-h] [-v DEFAULT_VERSION] [-d DEFAULT_DESCRIPTION] [-r REPO_USER_URL] [-a AUTHOR] [-e AUTHOR_EMAIL] [-l DEFAULT_LICENSE]

Optional:

- :code:`-v`, :code:`--default-version`: the version nusex initialises projects with
- :code:`-d`, :code:`--default-description`: the description nusex initialises projects with
- :code:`-r`, :code:`--repo-user-url`: your profile URL for your repository manager (for example, your GitHub profile URL)
- :code:`-a`, :code:`--author`: your name, or the name you want to use for your projects
- :code:`-e`, :code:`--author-email`: your email, or the email of your company/organisation
- :code:`-l`, :code:`--default-license`: the license nusex initialises projects with

.. note::

    All optional arguments default to their previous values.

.. versionadded:: 0.2.0
