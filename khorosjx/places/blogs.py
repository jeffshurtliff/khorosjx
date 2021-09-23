# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.places.blogs
:Synopsis:       Collection of core places functions that are specific to blogs
:Usage:          ``import khorosjx.places.blogs``
:Example:        ``blog_info = khorosjx.places.blogs.get_blog_info(browse_id)``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  22 Sep 2021
"""

from .. import core
from . import base as places_core

# Define global variables
base_url, api_credentials = '', None


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

    .. versionadded:: 3.1.0

    :returns: None
    :raises: :py:exc:`khorosjx.errors.exceptions.KhorosJXError`,
             :py:exc:`khorosjx.errors.exceptions.NoCredentialsError`
    """
    # Define the global variables at this module level
    global base_url
    global api_credentials
    base_url, api_credentials = core.get_connection_info()
    return


# Define function to get space info
def get_blog_info(place_id, return_fields=None, ignore_exceptions=False):
    """This function obtains the blog information for a given Place ID. (aka Browse ID)

    .. versionchanged:: 3.1.0
       Changed the default ``return_fields`` value to ``None`` and adjusted the function accordingly.

    :param place_id: The Place ID (aka Browse ID) of the blog whose information will be requested
    :type place_id: int, str
    :param return_fields: Specific fields to return if not all of the default fields are needed (Optional)
    :type return_fields: list, None
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A dictionary with the blog information
    :raises: GETRequestError, InvalidDatasetError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Leverage the core module to retrieve the data
    blog_info = places_core.get_place_info(place_id, return_fields, ignore_exceptions)
    return blog_info
