# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.utils.helper
:Synopsis:       Module that allows the khorosjx library to leverage a helper file and/or script
:Usage:          ``from khorosjx.utils import helper``
:Example:        TBD
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  26 Nov 2019
"""

import sys
import os.path

import yaml

from .core_utils import eprint


# Define function to import a YAML helper file
def import_yaml_file(file_path):
    """This function imports a YAML (.yml) helper config file.

    :param file_path: The file path to the YAML file
    :type file_path: str
    :returns: The parsed configuration data
    """
    with open(file_path, 'r') as yml_file:
        helper_cfg = yaml.load(yml_file, Loader=yaml.BaseLoader)
    return helper_cfg


# Define function to parse the YAML helper file
def parse_helper_cfg(helper_cfg, file_type='yaml'):
    __get_connection_info(helper_cfg, file_type)
    __get_console_color_settings(helper_cfg, file_type)
    return


# Define function to get the connection information
def __get_connection_info(_helper_cfg, _file_type='yaml'):
    # Define the base URL as a global string variable
    global helper_base_url
    helper_base_url = _helper_cfg['connection']['base_url']

    # Define the API credentials as a global tuple variable
    # TODO: Add the ability to import credentials from a script or module
    global helper_api_credentials
    _helper_username = _helper_cfg['connection']['credentials']['username']
    _helper_password = _helper_cfg['connection']['credentials']['password']
    helper_api_credentials = (_helper_username, _helper_password)
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
    helper_settings = {
        'base_url': helper_base_url,
        'api_credentials': helper_api_credentials,
        'use_console_colors': helper_console_colors
    }
    return helper_settings


# Define class for dictionaries to help in parsing the configuration files
class HelperParsing:
    # Define dictionary to map YAML Boolean to Python Boolean
    yaml_boolean_values = {
        True: True,
        False: False,
        'yes': True,
        'no': False
    }
