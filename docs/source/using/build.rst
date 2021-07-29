Building templates
##################

This section will run through how to build templates with nusex.

You can think of template building like screenshotting in a way -- nusex scans the current directory for files, and constructs a file manifest containing the names of the files and the data contained within them. You can either build a template from scratch, or use one of the :doc:`premade templates <./deploy>`.

To build a package, run the following command:

.. code-block:: bash

    nsx build template_name

where :code:`template_name` is what you wish to call your new template.

Ignoring files and directories
==============================

You can ignore certain file types or directories by using the respective options:

- :code:`--ignore-exts` -- a comma separated list of file types to ignore when scanning for files (default: pyc,pyo,pyd,pyi)
- :code:`--ignore-dirs` -- a comma separated list of directories to ignore when scanning for files (default: .git,.venv,.egg-info,.nox,dist)

Special files
=============

There are a number of so-called "special files" that nusex performs extra operations on. These operations replace certain variables, such as the project name and author name, with placeholder variables, which in turn can be replaced with the new information when the template is deployed.

nusex considers the following "special files":

- LICENSE
- MANIFEST.in
- pyproject.toml
- README.md
- setup.py
- [project_name]/__init__.py

The MANIFEST.in, pyproject.toml, README.md, and setup.py have the project name replaced with a placeholder variable, and the LICENSE file has the author name replaced. The __init__.py file, however, is a particularly special case.

The __init__.py file
--------------------

The __init__.py file in the project directory (not the root directory) generally stores project information, especially in the case of PyPI packages. This information is usually referenced using dunder variables (such as __version__). nusex manually hard-sets these variables to their placeholder alternatives, regardless of what they are currently set to. nusex uses a combination of the project name and user configuration information to regenerate this file when deploying templates. Other code below the dunder variables is preserved, but any code above them is not (this means the dunder variables should always be at the start of the file).

The following dunder variables are currently catered for (though not all of them need to exist for a template to be successfully built):

- __productname__
- __version__
- __description__
- __url__
- __docs__
- __author__
- __author_email__
- __license__
- __bugtracker__

If you plan to create a template using the simple_pkg template as a base, the generated setup.py file (lines 21-29) reads these variables to provide information for the package builder.
