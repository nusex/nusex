.. currentmodule:: nusex

Library reference
#################

Data attributes
===============

.. data:: __productname__

.. data:: __version__

    The currently installed version, represented in the :pep:`440` format.

.. data:: __description__

.. data:: __url__

    A link to the GitHub repository.

.. data:: __docs__

    A link to the documentation.

.. data:: __author__

.. data:: __author_email__

.. data:: __license__

.. data:: __bugtracker__

    A link to the issues page on the GitHub repository.

.. data:: __ci__

    A link to the actions page on the GitHub repository.

Exceptions
==========

.. autoexception:: nusex.errors.NusexError

.. autoexception:: nusex.errors.NusexUserError

.. autoexception:: nusex.errors.ProfileError

.. autoexception:: nusex.errors.TemplateError

.. autoexception:: nusex.errors.BuildError

.. autoexception:: nusex.errors.DeploymentError

.. autoexception:: nusex.errors.AlreadyExists

.. autoexception:: nusex.errors.DoesNotExist

.. autoexception:: nusex.errors.DownloadError

.. autoexception:: nusex.errors.UnsupportedFile

.. autoexception:: nusex.errors.IncompatibilityError

.. autoexception:: nusex.errors.MigrationError

Exception hierarchy
-------------------

- :exc:`Exception`
    - :exc:`NusexError`
        - :exc:`NusexUserError`
            - :exc:`ProfileError`
            - :exc:`TemplateError`
                - :exc:`BuildError`
                - :exc:`DeploymentError`
            - :exc:`AlreadyExists`
            - :exc:`DoesNotExist`
            - :exc:`MigrationError
        - :exc:`DownloadError`
        - :exc:`UnsupportedFile`
        - :exc:`IncompatibilityError``
