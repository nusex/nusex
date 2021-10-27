build
#####

Description
===========

Build a new template.

.. versionchanged:: 1.1
    Added ``language`` option.

Arguments
=========

``name``
    The name for the new template.

Options
=======

``-o`` | ``--overwrite``
    Overwrite an existing template should it already exist. You will not be asked for confirmation when doing this. It is safe to use this flag even when not overwriting a template.

``-c`` | ``--check``
    Check the build manifest without building the template. This will display every file that would be in the template if the settings remained the same, and also shows every line that has been modified by nusex.

``-r URL`` | ``--from-repo URL``
    The repository URL to build a template from. This link can be for any repository provider, but Git must be installed before you can do this.

``-l LANGUAGE`` | ``--language LANGUAGE``
    the language to assume the project is using. This changes which files are modified in the template, and how those files are modified. The default is "python".

``-i DEPS`` | ``--with-installs DEPS``
    A comma-separated list of dependencies to install when deploying. This can include version restrictions, but will probably require quotes when doing so.

``-I FILENAME`` | ``--with-requirements-file``
    A file within the template to install dependencies from when deploying. Note that if you update the requirements file within the template, then dependencies do not get automatically updated, and you will need to re-specify the requirements when rebuilding.

``--ignore-exts EXTS``
    A comma-separated list of file extensions to ignore. The default is "pyc,pyd,pyo".

``--extend-ignore-exts EXTS``
    A comma-separated list of file extensions to ignore on top of the defaults. This is useful if you just want to add file extensions.

``--ignore-dirs DIRS``
    A comma-separated list of directories to ignore. You can prefix any directory with an asterisk (*) to ignore any files that contain that sequence of characters anywhere in the filepath. Otherwise, the default behaviour is to ignore files if the given value matches the name of any directory in the filepath. The default is ".direnv,.eggs,.git,.hg,.mypy_cache,.nox,.tox,.venv,venv,.svn,_build,build,dist,buck-out,.pytest-cache,.nusexmeta,*.egg-info".

``--extend-ignore-dirs DIRS``
    A comma-separated list of directories to ignore on top of the defaults. The same asterisk (*) syntax applies here.
