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

    nusex build <template_name>

.. important::

    Source files are not modified during this process. Instead, the copies that nusex writes to the template's .nsx file are modified.

Ignoring files and directories
------------------------------

You can ignore certain file types and directories by using the respective options (you can read more about them in the command reference):

- ``--ignore-exts``
- ``--extend-ignore-exts``
- ``--ignore-dirs``
- ``--extend-ignore-dirs``

All four options take comma-separated lists of values. When passing file extensions to ignore, make sure to **not** include the dot (i.e. pass "py", not ".py").

There are two different ways to ignore directories:

- Passing a directory without any modifications will tell nusex to only ignore the directory if any part between the slashes perfectly matches the given value
- Passing a directory prefixed by an asterisk (*) will tell nusex to ignore the directory if the value appears anywhere in the filepath

The latter of these two options is the default behaviour in versions 0.x, though the asterisk did not need to be provided.

Installing dependencies
-----------------------

You can specify dependencies to install with a template. To do this, use one or both of the following options:

- ``-i`` or ``--with-installs``
- ``-I`` or ``--with-requirements-file``

When manually specifying installs, they must be comma-separated. When providing a requirements file, it must exist in the directory you are building the template from (so the one you intend to include in the template itself, unless you manually ignore it). If you update this requirements file, the template is not automatically updated, and must be rebuilt with the new requirements.

Building for languages other than Python
----------------------------------------

Python is assumed as the language of choice if no other language is specified. However, nusex does have dynamic templating support for multiple languages.

You can select a language using the following option:

- ``-l`` or ``--language``

The currently supported languages are:

- Python (the default)
- Rust
- None (this tells nusex to only modify language-agnostic files, such as the README)

Deploying templates
===================

Deploying a template will generate all the files in the template manifest (along with their modified contents) in the current directory. You can only deploy one template in any given directory, though you can deploy additional templates in that directory's subdirectories.

To deploy a template, run the following command:

.. code-block:: bash

    nusex deploy <template_name>

Installing dependencies
-----------------------

After a template's files have been generated, nusex will attempt to download any dependencies declared when building the template. There will be no output during this process (except if you are using Python 3.6 on Windows), so if you've specified a lot of large dependencies, nusex might appear to hang.

If you don't want nusex to install dependencies when deploying, even if dependencies have been specified, you can pass the `--no-installs` option.

.. important::

    This does not work on PyPy distributions. The template will still appear to build successfully, but dependency installations will be skipped. If you don't know what this means, you likely don't need to worry.

Dynamic templating
==================

The basics
----------

Dynamic templating, when referring to nusex, is the process of dynamically altering template manifests to implant different information into generated files depending on context. For example, nusex can implant the project name into generated files without you needing to go and change it. When building templates, nusex is able to detect what information needs to be changed in the future, so you don't need to worry about making sure you've accounted for everything.

The following files are altered when building generic templates, if present:

- COPYING [#f1]_
- LICENSE [#f1]_
- README [#f1]_
- docs/conf.py
- docs/source/conf.py

.. [#f1] Any files with this name in the template's root directory are modified, regardless of the file extension.

The following files are altered along with the language-agnostic files when building Python templates:

- MANIFEST.in
- pyproject.toml
- setup.cfg
- setup.py
- [project_name]/\_\_init\_\_.py
- [project_name]/error.py
- [project_name]/errors.py

The following files are altered along with the language-agnostic files when building Rust templates:

- Cargo.lock
- Cargo.toml
- src/error.rs
- src/errors.rs

Placeholder variable reference
------------------------------

Here is a rundown of the placeholder variables nusex uses when creating manifests and what they resolve to when deployed:

.. list-table::
    :widths: 1 5
    :header-rows: 1

    * - Variables
      - Resolution
    * - PROJECTNAME
      - The project name (set to the root directory of the current directory)
    * - PROJECTAUTHOR
      - The name of the author in the currently selected profile
    * - PROJECTAUTHOREMAIL
      - The email of the author in the currently selected profile
    * - PROJECTURL
      - The Git profile URL of the author in the currently selected profile, followed by the project name (i.e. https://github.com/nusex/nusex)
    * - PROJECTVERSION
      - The starting version in the currently selected profile
    * - PROJECTDESCRIPTION
      - The default description in the currently selected profile
    * - PROJECTLICENSE
      - The title of the preferred license in the currently selected profile
    * - PROJECTYEAR
      - The current year
    * - LICENSEBODY
      - The body of the preferred license in the currently selected profile
    * - PROJECTBASEEXC
      - The project name with the first letter capitalised, followed by "Error"

You oftentimes don't need to worry about this, though you can open the template file in some text editors to make sure nusex has made the necessary modifications. Alternatively, you can pass the ``-c`` or ``--check`` options to output a preview to the terminal.
