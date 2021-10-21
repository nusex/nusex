Migrating to v1.0
#################

There are a LOT of changes between v0.x and v1.x, so many in fact that the following list likely isn't exhaustive.

To help mitigate this shift, a new command, `nusex migrate`, has been created, which should be able to transfer your config and templates to the new way of doing things If this messes up for whatever reason, your old config is backed up, and can be brought back with `nusex migrate --revert`.

The biggest changes lie in the backend with the new scripting API The CLI uses this API to perform operations, and you can now created scripts utilising it.

Big changes
===========

These changes are in no particular order

Configuration and usage
-----------------------

- The user configuration has been replaced with profiles
- Profile and template names can no longer exceed 24 characters
- The NSC and NSX file formats now use a custom specification
- Templates are now stored in a different directory
- Terminal messages are now far less verbose, and also prettier
- Raw tracebacks are no longer thrown
- nusex now exits with code 1 if something went wrong, and 2 if the user did something wrong
- Initialisation now downloads licenses as well as templates
- The ``nsx`` command has been deprecated
- Some configuration options are now validated
- The ``config`` command is now the ``profile`` command, and a different ``config`` command now exists

Templates
---------

- Premade templates now cannot be directly overwritten
- Premade templates now have different names
- Profiles and configurations can no longer be safely edited by the user
- The extension and directory ignoring system has been changed (you can use asterisks if you wish to use the old behaviour)
- Templates now store data as bytes, meaning anything can be stored in templates, not just text
- Far more files now have dynamic templating support
