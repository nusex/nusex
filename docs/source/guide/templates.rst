Templates
#########

Templates are what nusex uses to generate files. You can have as many templates as you like.

Building templates
==================

The basics
----------

You can think of template building like screenshotting in a way – nusex scans the current directory for files, and constructs a file manifest containing the names of the files and the data contained within them. You can either build a template from scratch, or use one of the premade templates.

To build a template, run the following command:

.. code-block:: bash

    nsx build <template_name>

Ignoring files and directories
------------------------------

You can ignore certain file types and directories by using the respective options (you can read more about them in the command reference):

- :code:`--ignore-exts`
- :code:`--extend-ignore-exts`
- :code:`--ignore-dirs`
- :code:`--extend-ignore-dirs`

All four options take comma-separated lists of values. When passing file extensions to ignore, make sure to **not** include the dot (i.e. pass "py", not ".py").

There are two different ways to ignore directories:

- Passing a directory without any modifications will tell nusex to only ignore the directory if any part between the slashes perfectly matches the given value
- Passing a directory prefixed by an asterisk (*) will tell nusex to ignore the directory if the value appears anywhere in the filepath

The latter of these two options is the default behaviour in versions 0.x, though the asterisk did not need to be provided.

Deploying templates
===================

This feature isn't available in v1.x at the moment.

Dynamic templating
==================

The basics
----------

Dynamic templating, when referring to nusex, is the process of dynamically altering templates to implant different information into generated files depending on context. For example, nusex can implant the project name into generated files without you needing to go and change it. When building templates, nusex is able to detect what information needs to be changed in the future, so you don't need to worry about making sure you've accounted for everything.

The following files are altered when building templates, if present:

- LICENSE
- MANIFEST.in
- pyproject.toml
- README.md
- setup.cfg
- setup.py
- [project_name]/\_\_init\_\_.py
- [project_name]/error.py
- [project_name]/errors.py
- docs/conf.py
- docs/source/conf.py

These files are referred to internally as "special files".

Placeholder variable reference
------------------------------

This isn't available yet.

File modification reference
---------------------------

Here is a rundown of what gets modified in each file:

.. list-table::
    :widths: 1 5
    :header-rows: 1

    * - File
      - Changes
    * - COPYING
      - The entire file is replaced by "LICENSEBODY".
    * - COPYING.txt
      - The entire file is replaced by "LICENSEBODY".
    * - LICENSE
      - The entire file is replaced by "LICENSEBODY".
    * - LICENSE.txt
      - The entire file is replaced by "LICENSEBODY".
    * - MANIFEST.in
      - All mentions of the project's name are replaced by "PROJECTNAME".
    * - pyproject.toml
      - *Outlined below.*
    * - README.md
      - All mentions of the project's name are replaced by "PROJECTNAME", and an acknowledgement for nusex is added.
    * - setup.cfg
      - All mentions of the project's name are replaced by "PROJECTNAME".
    * - setup.py
      - All mentions of the project's name are replaced by "PROJECTNAME".
    * - [project_name]/\_\_init\_\_.py
      - *Outlined below*
    * - [project_name]/error.py
      - All mentions of the name of the first class found (assumed as the base error class) are replaced with "PROJECTBASEEXC".
    * - [project_name]/errors.py
      - All mentions of the name of the first class found (assumed as the base error class) are replaced with "PROJECTBASEEXC".
    * - docs/conf.py
      - *Outlined below*
    * - docs/source/conf.py
      - *Outlined below*

Modifications to the [project_name]/\_\_init\_\_.py file
--------------------------------------------------------

This file is normally where project information is held, more commonly in PyPI packages than general applications. Typically, this information is assigned to different `dunder variables <https://bic-berkeley.github.io/psych-214-fall-2016/two_dunders.html>`_.

The following dunder variables are handled (any quotes are also written to the file):

.. list-table::
    :header-rows: 1

    * - Variable name
      - Value it is assigned by nusex
    * - \_\_productname\_\_
      - "PROJECTNAME"
    * - \_\_version\_\_
      - "PROJECTVERSION"
    * - \_\_description\_\_
      - "PROJECTDESCRIPTION"
    * - \_\_url\_\_
      - "PROJECTURL"
    * - \_\_docs\_\_
      - "https://PROJECTNAME.readthedocs.io/en/latest"
    * - \_\_author\_\_
      - "PROJECTAUTHOR"
    * - \_\_author_email\_\_
      - "PROJECTAUTHOREMAIL"
    * - \_\_license\_\_
      - "PROJECTLICENSE"
    * - \_\_bug_tracker\_\_
      - "PROJECTURL/issues"

Any number of dunder variables can be present in the \_\_init\_\_.py file, and they do not need to be in the above order, or in the same code block.

Modifications to the pyproject.toml file
----------------------------------------

This file is generally used to store settings for various tools, including black and mypy. It can also be used as a replacement for any requirements files, or the \_\_init\_\_.py file with the use of the Poetry tool.

The following variables are handled (any quotes are also written to the file):

.. list-table::
    :header-rows: 1

    * - Variable name
      - Value it is assigned by nusex
    * - name
      - "PROJECTNAME"
    * - version
      - "PROJECTVERSION"
    * - description
      - "PROJECTDESCRIPTION"
    * - license
      - "PROJECTLICENSE"
    * - authors
      - ["PROJECTAUTHOR <PROJECTAUTHOREMAIL>"]
    * - maintainers
      - ["PROJECTAUTHOR <PROJECTAUTHOREMAIL>"]
    * - homepage
      - "PROJECTURL"
    * - repository
      - "PROJECTURL"
    * - documentation
      - "https://PROJECTNAME.readthedocs.io/en/latest"

Modifications to the docs[/source]/conf.py file
-----------------------------------------------

This file stores settings for rendering documentation using Sphinx.

The following variables are handled (any quotes are also written to the file):

.. list-table::
    :header-rows: 1

    * - Variable name
      - Value it is assigned by nusex
    * - project
      - "PROJECTNAME"
    * - copyright
      - "PROJECTYEAR, PROJECTAUTHOR"
    * - author
      - "PROJECTAUTHOR"
    * - release
      - "PROJECTNAME.\_\_version\_\_"

nusex also changes one of the import statements to "import PROJECTNAME".
