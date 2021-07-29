Initialising nusex
##################

This section will run through initialising nusex to make it ready to use.

In order to initialise nusex, run the following command:

.. code-block:: bash

    nsx init

You will be asked to provide some information to help nusex dynamically fill in information when deploying templates. You will need to provide:

- Your name (or the name you wish to be credited using)
- Your email (or a company/organisation email)
- Your GitHub/Gitlab/BitBucket (or other sevice) user profile link (for example: https://github.com/parafoxia)

nusex does store more configuration information, but you cannot set this through the CLI right now -- a command to allow you to do this is planned for version 0.2. You can find the created configuration file in **/home/[username]/.config/nusex/user.nsc** (Linux & macOS) or **C:/Users/[username]/.nusex/user.nsc** (Windows). It is safe to edit the file manually, so long as you don't change any of the keys.

After you've provided this information, nusex proceeds to download the latest premade templates from the `GitHub repository <https://github.com/parafoxia/nusex/tree/main/templates>`_. These templates are:

- **simple_app**, for general applications
- **simple_pkg**, for PyPI packages

You can deploy these templates by using the :doc:`deploy command <./deploy>`. They are stored as .nsx files in the same directory as the user configuration file.
