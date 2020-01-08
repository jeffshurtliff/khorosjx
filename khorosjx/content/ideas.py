# -*- coding: utf-8 -*-
"""
:Module:            khorosjx.content.ideas
:Synopsis:          Collection of functions relating to ideas (e.g. https://community.example.com/idea/1234)
:Usage:             ``from khorosjx.content import ideas``
:Example:           ``content_id = ideas.get_content_id(url)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     05 Jan 2020
"""

from .. import core
from . import base


# Define function to verify the connection in the core module
def verify_core_connection():
    """This function verifies that the core connection information (Base URL and API credentials) has been defined.

    :returns: None
    :raises: NameError, KhorosJXError, NoCredentialsError
    """
    def __get_info():
        """This function initializes and defines the global variables for the connection information.

        :returns: None
        :raises: NameError, KhorosJXError, NoCredentialsError
        """
        # Initialize global variables
        global base_url
        global api_credentials

        # Define the global variables at this module level
        base_url, api_credentials = core.get_connection_info()
        return

    try:
        base_url
        api_credentials
    except NameError:
        __get_info()
    return


# Define function to get the content ID from a URL
def get_content_id(url):
    """This function obtains the Content ID for a particular idea.

    :param url: The URL of the idea
    :type url: str
    :returns: The Content ID for the idea
    :raises: ValueError
    """
    content_id = base.get_content_id(url, 'idea')
    return content_id
