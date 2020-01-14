# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.utils.helper
:Synopsis:       Module that allows the khorosjx library to leverage a helper file and/or script
:Usage:          ``from khorosjx.utils import helper``
:Example:        ``helper_cfg = helper.import_yaml_file('/path/to/jxhelper.yml')``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  14 Jan 2020
"""

import importlib

import yaml

from .core_utils import eprint
from ..errors import exceptions


# Define function to import a YAML helper file
def import_yaml_file(file_path):
    """This function imports a YAML (.yml) helper config file.

    :param file_path: The file path to the YAML file
    :type file_path: str
    :returns: The parsed configuration data
    :raises: FileNotFoundError
    """
    with open(file_path, 'r') as yml_file:
        helper_cfg = yaml.load(yml_file, Loader=yaml.BaseLoader)
    return helper_cfg


# Define function to parse the YAML helper file
def parse_helper_cfg(helper_cfg, file_type='yaml'):
    """This is the primary function used to parse the helper config file.

    :param helper_cfg: The raw data loaded from the config file
    :param file_type: Indicates the type of configuration file (Default: ``yaml``)
    :returns: None (Defines global variables)
    :raises: CredentialsUnpackingError, InvalidHelperArgumentsError, HelperFunctionNotFoundError
    """
    __get_connection_info(helper_cfg, file_type)
    __get_console_color_settings(helper_cfg, file_type)
    __get_modules_to_import(helper_cfg, file_type)
    return


# Define function to covert a YAML Boolean value to a Python Boolean value
def __convert_yaml_to_bool(_yaml_bool_value):
    """This function converts the 'yes' and 'no' YAML values to traditional Boolean values."""
    true_values = ['yes', 'true']
    if _yaml_bool_value.lower() in true_values:
        _bool_value = True
    else:
        _bool_value = False
    return _bool_value


# Define function to parse the function arguments if present
def __parse_function_arguments(_function_args_string):
    if len(_function_args_string) == 0:
        _parsed_arguments = {}
    else:
        try:
            _parsed_arguments = dict(e.split('=') for e in _function_args_string.split(', '))
        except ValueError:
            raise exceptions.InvalidHelperArgumentsError

        # Update the data types as needed
        for _arg_key, _arg_value in _parsed_arguments.items():
            if ("\"" in _arg_value) or ("'" in _arg_value):
                _arg_value = str(_arg_value.replace("\"", "").replace("'", ""))
            elif _arg_value.lower() == "true" or _arg_value.lower() == "false":
                _arg_value = __convert_yaml_to_bool(_arg_value)
            elif _arg_value.isdigit():
                _arg_value = int(_arg_value)
            _parsed_arguments[_arg_key] = _arg_value
    return _parsed_arguments


# Define function to get the connection information
def __get_connection_info(_helper_cfg, _file_type='yaml'):
    # Define the base URL as a global string variable
    global helper_base_url
    helper_base_url = _helper_cfg['connection']['base_url']

    # Define the API credentials as a global tuple variable
    global helper_api_credentials
    _use_script = __convert_yaml_to_bool(_helper_cfg['connection']['credentials']['use_script'])
    if _use_script is False:
        _helper_username = _helper_cfg['connection']['credentials']['username']
        _helper_password = _helper_cfg['connection']['credentials']['password']
    else:
        _helper_username, _helper_password = __get_credentials_from_module(_helper_cfg)
    helper_api_credentials = (_helper_username, _helper_password)
    return


# Define function to get the API credentials from a module and function
def __get_credentials_from_module(_helper_cfg):
    # Define the module and function information
    _module_name = _helper_cfg['connection']['credentials']['module_name']
    _function_name = _helper_cfg['connection']['credentials']['function_name']
    _function_kwargs = _helper_cfg['connection']['credentials']['function_kwargs']

    # Import the supplied module
    _imported_module = importlib.import_module(_module_name)
    try:
        _function = getattr(_imported_module, _function_name)
    except AttributeError:
        raise exceptions.HelperFunctionNotFoundError

    # Parse the function arguments
    _arguments = __parse_function_arguments(_function_kwargs)

    # Retrieve the credentials using the module and function
    try:
        _helper_username, _helper_password = _function(**_arguments)
    except ValueError:
        raise exceptions.CredentialsUnpackingError("The function called by the helper module must return two " +
                                                   "values, one for the username and one for the password.")
    return _helper_username, _helper_password


# Define function to get the modules to import
def __get_modules_to_import(_helper_cfg, _file_type='yaml'):
    global modules_to_import
    modules_to_import = []
    if 'import_all' in _helper_cfg['modules'].keys():
        if __convert_yaml_to_bool(_helper_cfg['modules']['import_all']) is True:
            modules_to_import.append('all')
            return
    for _mod_name, _import_val in _helper_cfg['modules'].items():
        if _mod_name == 'import_all':
            break
        elif _mod_name not in HelperParsing.accepted_import_modules:
            _error_msg = f"The module '{_mod_name}' is not a valid option for the " + \
                         "'modules' setting. The entry will be ignored."
            eprint(_error_msg)
        elif _import_val not in HelperParsing.yaml_boolean_values.keys():
            _error_msg = f"The value '{_import_val}' is not a valid option for the " + \
                         f"'{_mod_name}' setting. The entry will be ignored."
            eprint(_error_msg)
        else:
            if __convert_yaml_to_bool(_helper_cfg['modules'][_import_val]) is True:
                modules_to_import.append(_mod_name)
    return


# Define function to get console color settings
def __get_console_color_settings(_helper_cfg, _file_type='yaml'):
    # Define the console colors setting as a Boolean global variable
    global helper_console_colors
    _cfg_val = _helper_cfg['styling']['use_console_colors']
    if _file_type == 'yaml' and _cfg_val in HelperParsing.yaml_boolean_values:
        helper_console_colors = HelperParsing.yaml_boolean_values.get(_cfg_val)
    else:
        _error_msg = f"The value '{_cfg_val}' is not a valid option for the " + \
                    "'use_console_colors' setting. The value will be set to False."
        eprint(_error_msg)
        helper_console_colors = False
    return


# Define function to retrieve the helper configuration settings
def retrieve_helper_settings():
    """This function returns a dictionary of the defined helper settings.

    :returns: Dictionary of helper variables with nicknames
    """
    helper_settings = {
        'base_url': helper_base_url,
        'api_credentials': helper_api_credentials,
        'use_console_colors': helper_console_colors,
        'modules_to_import': modules_to_import
    }
    return helper_settings


# Define class for dictionaries to help in parsing the configuration files
class HelperParsing:
    """This class is used to help parse values imported from a YAML configuration file."""
    # Define dictionary to map YAML Boolean to Python Boolean
    yaml_boolean_values = {
        True: True,
        False: False,
        'yes': True,
        'no': False
    }

    # Defined the acceptable import fields within the 'modules' section
    accepted_import_modules = ['all_modules', 'admin', 'blogs', 'content', 'content.base', 'docs', 'events', 'groups',
                               'ideas', 'places', 'places.spaces', 'spaces', 'threads', 'users', 'videos']
    all_modules = ['admin', 'content', 'groups', 'places', 'users']
