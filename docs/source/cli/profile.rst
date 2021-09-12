profile
#######

Description
===========

Create, modify and switch user profiles.

Passing no arguments to this command begins the profile setup sequence.

Arguments
=========

Required
--------

This command has no required arguments.

Optional
--------

:code:`-c` | :code:`--show-current`
    Show the currently selected profile. This will output the profile's name to the terminal and exit. This will override any other flag.

:code:`-n NAME` | :code:`--create-new NAME`
    Create a new profile. Once run, the profile setup process will start. This will override any below flags.

:code:`-s NAME` | :code:`--switch NAME`
    Switch to a different profile. This will override any below flags.

:code:`-a NAME` | :code:`--author-name NAME`
    Change the author name for this profile.

:code:`-e EMAIL` | :code:`--author-email EMAIL`
    Change the author email for this profile.

:code:`-g URL` | :code:`--git-profile-url URL`
    Change the Git profile URL for this profile.

:code:`-v VERSION` | :code:`--starting-version VERSION`
    Change the starting version for this profile.

:code:`-d DESCRIPTION` | :code:`--default-description DESCRIPTION`
    Change the default description for this profile.

:code:`-l LICENSE` | :code:`--license LICENSE`
    Change the preferred license for this profile.
