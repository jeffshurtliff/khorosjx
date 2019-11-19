# -*- coding: utf-8 -*-
"""
:Package:        khorosjx
:Synopsis:       This package includes custom exceptions and a function to call them with specific error messages
:Usage:          import khorosjx.errors (Imported by default in primary package)
:Example:        khorosjx.core.connect(base_url, credentials)
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  19 Nov 2019
"""

# Define all modules that will be imported with the "import *" method
__all__ = ['core', 'admin', 'content', 'groups', 'spaces', 'users']

# Always import the core module and the errors package
from . import core
from . import errors


# Define function to initialize additional modules via the primary package
def init_module(*args):
    """This function imports select modules from the library.

    :param args: One or more module names to import
    :type args: str
    :returns: None
    :raises: ModuleNotFoundError, KhorosJXError, InvalidKhorosJXModuleError
    """
    # Get any arguments supplied in the function
    arguments = []
    for arg in args:
        if type(arg) == tuple or type(arg) == list:
            for item in arg:
                if type(item) == tuple or type(item) == list:
                    for subitem in item:
                        arguments.append(subitem)
                else:
                    arguments.append(item)
        else:
            arguments.append(arg)

    # Import any of the supplied modules
    for mod_entry in arguments:
        if mod_entry == "core":
            print("The module `khorosjx.core` is already imported and will not be imported again.")
        elif mod_entry == "admin":
            from . import admin
        elif mod_entry == "content":
            from . import content
        elif mod_entry == "groups":
            from . import groups
        elif mod_entry == "spaces":
            from . import spaces
        elif mod_entry == "users":
            from . import users
        else:
            errors.raise_exception('invalid_module')
    return
