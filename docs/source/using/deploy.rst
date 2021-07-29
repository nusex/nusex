Deploying templates
###################

This section will run through how to deploy templates with nusex.

Before you deploy a package, make sure the project's main directory is created, and it is your current directory. Much like :code:`git init`, or :code:`sphinx-quickstart`, files are created in the current directory.

To deploy a package, run the following command:

.. code-block:: bash

    nsx deploy template_name

where :code:`template_name` is the name of the template you wish to deploy.

.. warning::

    When deploying templates, any currently present files will be overwritten on conflict.

Premade templates
=================

simple_app
----------

The simple_app template contains the following files:

.. code-block::

    .
    ├── ./LICENSE
    ├── ./README.md
    ├── ./requirements-dev.txt
    ├── ./requirements.txt
    └── ./simple_app
        └── ./simple_app/__init__.py

simple_pkg
----------

The simple_pkg template contains the following files:

.. code-block::

    .
    ├── ./LICENSE
    ├── ./pyproject.toml
    ├── ./README.md
    ├── ./requirements-dev.txt
    ├── ./requirements.txt
    ├── ./setup.py
    └── ./simple_pkg
        ├── ./simple_pkg/errors.py
        └── ./simple_pkg/__init__.py

The main additions are the pyproject.toml and setup.py files, which contain information for building packages, and a fully fleshed out __init__.py file.
