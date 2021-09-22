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

.. autoexception:: nusex.errors.DownloadError

.. autoexception:: nusex.errors.BuildError

.. autoexception:: nusex.errors.DeploymentError

.. autoexception:: nusex.errors.UnsupportedFile

.. autoexception:: nusex.errors.NusexUserError

.. autoexception:: nusex.errors.EntityError

.. autoexception:: nusex.errors.AlreadyExists

.. autoexception:: nusex.errors.DoesNotExist

Exception hierarchy
-------------------

- :exc:`Exception`
    - :exc:`NusexError`
    - :exc:`DownloadError`
    - :exc:`BuildError`
    - :exc:`DeploymentError`
    - :exc:`UnsupportedFile`
    - :exc:`NusexUserError`
        - :exc:`EntityError`
        - :exc:`AlreadyExists`
        - :exc:`DoesNotExist`
