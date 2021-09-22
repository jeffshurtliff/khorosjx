# -*- coding: utf-8 -*-
"""
:Module:            khorosjx.content.threads
:Synopsis:          Collection of functions relating to discussion and question threads
:Usage:             ``from khorosjx.content import threads``
:Example:           ``content_id = threads.get_content_id(url)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     22 Sep 2021
"""

from .. import core
from . import base

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


# Define function to get the content ID from a URL
def get_content_id(url):
    """This function obtains the Content ID for a particular discussion or question thread.

    :param url: The URL of the thread
    :type url: str
    :returns: The Content ID for the thread
    :raises: :py:exc:`ValueError`
    """
    content_id = base.get_content_id(url, 'thread')
    return content_id
