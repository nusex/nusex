profile
#######

Description
===========

Create, modify and switch user profiles.

Passing no arguments to this command begins the profile setup sequence.

Arguments
=========

This command has no arguments.

Options
=======

``-c`` | ``--show-current``
    Show the currently selected profile. This will output the profile's name to the terminal and exit. This will override any other flag.

``-n NAME`` | ``--create-new NAME``
    Create a new profile. Once run, the profile setup process will start. This will override any below flags.

``-s NAME`` | ``--switch NAME``
    Switch to a different profile. This will override any below flags.

``-a NAME`` | ``--author-name NAME``
    Change the author name for this profile.

``-e EMAIL`` | ``--author-email EMAIL``
    Change the author email for this profile.

``-g URL`` | ``--git-profile-url URL``
    Change the Git profile URL for this profile.

``-v VERSION`` | ``--starting-version VERSION``
    Change the starting version for this profile.

``-d DESCRIPTION`` | ``--default-description DESCRIPTION``
    Change the default description for this profile.

``-l LICENSE`` | ``--license LICENSE``
    Change the preferred license for this profile.
