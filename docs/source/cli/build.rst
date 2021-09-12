build
#####

Description
===========

Build a new template.

Arguments
=========

Required
--------

:code:`name`
    The name for the new template.

Optional
--------

:code:`-o` | :code:`--overwrite`
    Overwrite an existing template should it already exist. You will not be asked for confirmation when doing this. It is safe to use this flag even when not overwriting a template.

:code:`-c` | :code:`--check`
    Check the build manifest without building the template. This will display every file that would be in the template if the settings remained the same, and also shows every line that has been modified by nusex.

:code:`-r URL` | :code:`--from-repo URL`
    The repository URL to build a template from. This link can be for any repository provider, but Git must be installed before you can do this.

:code:`-e TEMPLATE` | :code:`--as-extension-for TEMPLATE`
    Build this template as an extension for another template. The template to build the extension for must already exist.

:code:`--ignore-exts EXTS`
    A comma-separated list of file extensions to ignore. The default is "pyc,pyd,pyo".

:code:`--extend-ignore-exts EXTS`
    A comma-separated list of file extensions to ignore on top of the defaults. This is useful if you just want to add file extensions.

:code:`--ignore-dirs DIRS`
    A comma-separated list of directories to ignore. You can prefix any directory with an asterisk (*) to ignore any files that contain that sequence of characters anywhere in the filepath. Otherwise, the default behaviour is to ignore files if the given value matches the name of any directory in the filepath. The default is ".direnv,.eggs,.git,.hg,.mypy_cache,.nox,.tox,.venv,venv,.svn,_build,build,dist,buck-out,*.egg-info".

:code:`--extend-ignore-dirs DIRS`
    A comma-separated list of directories to ignore on top of the defaults. The same asterisk (*) syntax applies here.
