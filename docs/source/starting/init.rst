Initialising nusex
##################

This section will run through initialising nusex to make it ready to use.

In order to initialise nusex, run the following command:

.. code-block:: bash

    nusex init

You will be asked to provide some information to help nusex dynamically fill in information when deploying templates. You can find out what information is asked of you in the :doc:`profile guide <../guide/profiles>`.

You will find the created configuration file in a different directory depending on your OS:

- **Windows**: C:/Users/[username]/.nusex/config.nsc
- **UNIX**: /home/[username]/.config/nusex/config.nsc

After you've provided this information, nusex proceeds to download the latest premade templates from the `downloads repository <https://github.com/nusex/downloads/tree/main/templates1x>`_ and the latest selection of open source licenses from an `external repository <https://github.com/github/choosealicense.com/tree/gh-pages/_licenses>`_. The templates that are downloaded are:

- **nsx_simple_app**, for general applications
- **nsx_simple_pkg**, for PyPI packages

You can deploy these templates by using the :doc:`deploy command <../understanding/deploy>`. They are stored as .nsx files in a "templates" subdirectory.
