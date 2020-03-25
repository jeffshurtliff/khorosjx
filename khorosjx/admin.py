# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.admin
:Synopsis:       Collection of functions relating to security groups
:Usage:          ``from khorosjx import admin``
:Example:        Coming Soon
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  24 Mar 2020
"""

from . import core


# Define function to verify the connection in the core module
def verify_core_connection():
    """This function verifies that the core connection information (Base URL and API credentials) has been defined.

    :returns: None
    :raises: :py:exc:`NameError`, :py:exc:`khorosjx.errors.exceptions.KhorosJXError`,
             :py:exc:`khorosjx.errors.exceptions.NoCredentialsError`
    """
    try:
        base_url
        api_credentials
    except NameError:
        retrieve_connection_info()
    return


def retrieve_connection_info():
    """This function initializes and defines the global variables for the connection information.

    :returns: None
    :raises: :py:exc:`NameError`, :py:exc:`khorosjx.errors.exceptions.KhorosJXError`,
             :py:exc:`khorosjx.errors.exceptions.NoCredentialsError`
    """
    # Initialize global variables
    global base_url
    global api_credentials

    # Define the global variables at this module level
    base_url, api_credentials = core.get_connection_info()
    return
