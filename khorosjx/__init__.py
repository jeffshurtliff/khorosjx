# -*- coding: utf-8 -*-
"""
:Package:           khorosjx
:Synopsis:          This package includes custom exceptions and a function to call them with specific error messages
:Usage:             ``import khorosjx``
:Example:           ``khorosjx.init_helper('/home/user/jxhelper.yml')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     16 Mar 2020
"""

from . import core, errors
from .utils import version

# Define all modules that will be imported with the "import *" method
__all__ = ['core', 'admin', 'content', 'groups', 'news', 'places', 'spaces', 'users']

# Define the package version by pulling from the khorosjx.utils.version module
__version__ = version.get_full_version()


# Define function to initialize additional modules via the primary package
def init_module(*args):
    """This function imports select modules from the library.

    :param args: One or more module names to import
    :type args: str, tuple
    :returns: None
    :raises: ModuleNotFoundError, KhorosJXError, InvalidKhorosJXModuleError
    """
    # Get any arguments supplied in the function
    import_all = ['admin', 'content', 'groups', 'news', 'places', 'users']
    if 'all' in args:
        arguments = import_all
    else:
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
        if 'all' in arguments:
            arguments = import_all

    # Import any of the supplied modules
    for mod_entry in arguments:
        if mod_entry == "core":
            print("The module `khorosjx.core` is already imported and will not be imported again.")
        elif mod_entry == "admin":
            from . import admin
        elif mod_entry == "blogs":
            from .places import blogs
        elif mod_entry == "content":
            from . import content
        elif mod_entry == "content.base":
            from .content import base as content_base
        elif mod_entry == "docs":
            from .content import docs
        elif mod_entry == "events":
            from .content import events
        elif mod_entry == "groups":
            from . import groups
        elif mod_entry == "ideas":
            from .content import ideas
        elif mod_entry == "news":
            from . import news
        elif mod_entry == "places":
            from . import places
        elif mod_entry == "places.spaces":
            from .places import spaces
        elif mod_entry == "spaces":
            from . import spaces
        elif mod_entry == "threads":
            from .content import threads
        elif mod_entry == "users":
            from . import users
        elif mod_entry == "videos":
            from .content import videos
        else:
            raise errors.exceptions.InvalidKhorosJXModuleError
    return


# Define function to initialize a helper file
def init_helper(file_path, file_type='yaml'):
    """This function initializes a helper configuration file to define package settings including the API connection.

    :param file_path: Path to the helper configuration file
    :type file_path: str
    :param file_type: The type of file utilized as the configuration file (Default: ``yaml``)
    :type file_type: str
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
    else:
        exception_msg = f"The '{file_type}' file type is not currently supported and the '{file_path}' file cannot" + \
                        "be utilized as a Helper configuration file."
        raise errors.exceptions.InvalidFileTypeError(exception_msg)
    helper.parse_helper_cfg(helper_cfg)
    helper_settings = helper.retrieve_helper_settings()

    # Establish the API connection
    core.connect(helper_settings['base_url'], helper_settings['api_credentials'])

    # Define global variable for the console colors setting
    global use_console_colors
    use_console_colors = helper_settings['use_console_colors']

    # Import any specified modules
    if len(helper_settings['modules_to_import']) > 0:
        init_module(helper_settings['modules_to_import'])
    return


# Display a warning if the running version is not the latest stable version found on PyPI
version.warn_when_not_latest()
