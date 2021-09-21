# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.admin
:Synopsis:       Collection of functions relating to security groups
:Usage:          ``from khorosjx import admin``
:Example:        Coming Soon
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  21 Sep 2021
"""

from . import core

# Define global variables
base_url, api_credentials = None, None


# Define function to verify the connection in the core module
def verify_core_connection():
    """This function verifies that the core connection information (Base URL and API credentials) has been defined.

    .. versionchanged:: 3.1.0
       Refactored the function to be more pythonic and to avoid depending on a try/except block.

    :returns: None
    :raises: :py:exc:`khorosjx.errors.exceptions.KhorosJXError`,
             :py:exc:`khorosjx.errors.exceptions.NoCredentialsError`
    """
    if not base_url or not api_credentials:
        retrieve_connection_info()
    return


def retrieve_connection_info():
    """This function initializes and defines the global variables for the connection information.

    .. versionchanged:: 3.1.0
       Refactored the function to be more efficient.

    :returns: None
    :raises: :py:exc:`khorosjx.errors.exceptions.KhorosJXError`,
             :py:exc:`khorosjx.errors.exceptions.NoCredentialsError`
    """
    # Define the global variables at this module level
    global base_url
    global api_credentials
    base_url, api_credentials = core.get_connection_info()
    return
