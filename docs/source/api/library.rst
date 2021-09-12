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

.. autoexception:: nusex.errors.DownloadFailure

.. autoexception:: nusex.errors.BuildError

.. autoexception:: nusex.errors.InvalidFormat

.. autoexception:: nusex.errors.UnsupportedFile

.. autoexception:: nusex.errors.NusexUserError

.. autoexception:: nusex.errors.InvalidRequest

.. autoexception:: nusex.errors.InvalidConfiguration

.. autoexception:: nusex.errors.InvalidName

.. autoexception:: nusex.errors.AlreadyExists

Exception hierarchy
-------------------

- :exc:`Exception`
    - :exc:`NusexError`
    - :exc:`DownloadFailure`
    - :exc:`BuildError`
    - :exc:`UnsupportedFile`
    - :exc:`NusexUserError`
        - :exc:`InvalidRequest`
        - :exc:`InvalidConfiguration`
        - :exc:`InvalidName`
        - :exc:`AlreadyExists`
