Profiles
########

Profiles are what nusex uses to determine what information to implant into files when deploying templates. Those who maintain both personal and organisation-owned projects can have multiple profiles, each with a different author name, email, etc. You can have as many profiles as you like, and can switch between them at any time.

Profile contents
================

Profiles store:

- An author name (this can be your own name, or an organisation name, or really anything)
- An author email (yours or your organisation's email)
- Your GitHub/Gitlab/BitBucket/etc. profile link (i.e. https://github.com/nusex)
- The version to initialise projects with (default: 0.1.0)
- The description to initialise projects with (default: My project, created using nusex)
- Your preferred license (default: unlicense)

Creating profiles
=================

You can create a new profile by using the following command:

.. code-block:: bash

    nsx profile -n <template_name>

When you create a profile in this way, you'll be prompted to provide everything in the **Profile contents** section. Once the new profile has been created, nusex will automatically switch to it.

Configuring profiles
====================

You can configure any existing profile at any time using the :code:`nsx profile` command. If you don't provide any flags, the setup sequence will run again, though this time the defaults will be set to what they currently are. You can also pass flags to quickly change one or more field; look at the command reference to find out how.
