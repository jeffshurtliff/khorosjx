# -*- coding: utf-8 -*-
"""
:Module:            khorosjx.content.events
:Synopsis:          Collection of functions relating to events (e.g. https://community.example.com/event/1234)
:Usage:             ``from khorosjx.content import events``
:Example:           ``content_id = events.get_content_id(url)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     24 Mar 2020
"""

from .. import core
from . import base


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


def get_content_id(url):
    """This function obtains the Content ID for a particular event.

    :param url: The URL of the event
    :type url: str
    :returns: The Content ID for the event
    :raises: :py:exc:`ValueError`
    """
    content_id = base.get_content_id(url, 'event')
    return content_id
