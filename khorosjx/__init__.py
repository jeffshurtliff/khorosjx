# -*- coding: utf-8 -*-
"""
:Package:        khorosjx
:Synopsis:       This package includes custom exceptions and a function to call them with specific error messages
:Usage:          import khorosjx.errors (Imported by default in primary package)
:Example:        khorosjx.core.connect(base_url, credentials)
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  23 Nov 2019
"""

# Define all modules that will be imported with the "import *" method
__all__ = ['core', 'admin', 'content', 'groups', 'spaces', 'users', 'helper']

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
            raise errors.exceptions.InvalidKhorosJXModuleError
    return


# Define function to initialize a helper file
def init_helper(file_path, file_type='yaml'):
    """This function initializes a helper configuration file to define package settings including the API connection.

    :param file_path: Path to the helper configuration file
    :type file_path: str
    :param file_type: The type of file utilized as the configuration file (Default: ``yaml``)
    :returns: None (Defines global variables and establishes API connection)
    :raises: FileNotFoundError, CredentialsUnpackingError, InvalidHelperArgumentsError, HelperFunctionNotFoundError
    """
    # Import the helper module
    from .utils import helper

    # Initialize the global variable for the helper configuration data
    global helper_settings

    # Obtain the helper configuration settings
    if file_type == 'yaml':
        helper_cfg = helper.import_yaml_file(file_path)
    helper.parse_helper_cfg(helper_cfg)
    helper_settings = helper.retrieve_helper_settings()

    # Establish the API connection
    core.connect(helper_settings['base_url'], helper_settings['api_credentials'])

    # Define global variable for the console colors setting
    global use_console_colors
    use_console_colors = helper_settings['use_console_colors']
    return
