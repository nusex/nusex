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

.. autoexception:: nusex.errors.NusexException

.. autoexception:: nusex.errors.NusexAPIException

.. autoexception:: nusex.errors.NusexCLIException

.. autoexception:: nusex.errors.NotSupported

.. autoexception:: nusex.errors.InvalidName

.. autoexception:: nusex.errors.TemplateError

.. autoexception:: nusex.errors.InvalidBlueprint

Exception hierarchy
-------------------

- :exc:`Exception`
    - :exc:`NusexException`
        - :exc:`NusexAPIException`
            - :exc:`InvalidName`
            - :exc:`TemplateError`
                - :exc:`InvalidBlueprint`
        - :exc:`NusexCLIException`
        - :exc:`NotSupported`
