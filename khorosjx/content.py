# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.content
:Synopsis:       Collection of functions relating to content
:Usage:          ``from khorosjx import content``
:Example:        ``content_id = content.get_content_id(url, 'discussion')``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  17 Nov 2019
:Version:        1.0.0
"""

import re
import json

import requests

from . import core
from .utils.classes import Content


# Define function to verify the connection in the core module
def verify_core_connection():
    """This function verifies that the core connection information (Base URL and API credentials) has been defined.

    :returns: None
    :raises: NameError, KhorosJXError, NoCredentialsError
    """
    def get_info():
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
        get_info()
    return


# Define function to get the content ID from a URL
def get_content_id(url, content_type="document"):
    """This function obtains the Content ID for a particular content asset. (Supports all but blog posts)

    :param url: The URL to the content
    :type url: str
    :param content_type: THe content type for the URL for which to obtain the Content ID (Default: ``document``)
    :type content_type: str
    :returns: The Content ID for the content URL
    :raises: ValueError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Get the domain URL from the supplied content URL
    if content_type in Content.content_url_delimiters:
        platform_url = url.split(Content.content_url_delimiters.get(content_type))[0]
        if not platform_url.startswith('http'):
            platform_url = f"https://{platform_url}"
    else:
        error_msg = "Unable to identify the platform URL for the URL and defined content type."
        raise ValueError(error_msg)

    # Get the ID to be used in the GET request
    if content_type == "document":
        item_id = url.split('DOC-')[1]
    elif content_type == "blog post":
        raise ValueError(f"The get_content_id function does not currently support blog posts.")
    else:
        item_id = re.sub('^.*/', '', url)

    # Construct the appropriate query URL
    if content_type in Content.content_types:
        content_type_id = Content.content_types.get(content_type)
        query_url = f"{platform_url}/api/core/v3/contents?filter=entityDescriptor({content_type_id},{item_id})&count=1"
    else:
        error_msg = f"The content type {content_type} is unrecognized. Unable to perform the function."
        raise ValueError(f"{error_msg}")

    # Query the API to get the content ID
    response = core.get_request_with_retries(query_url)
    content_data = response.json()
    content_id = content_data['list'][0]['contentID']
    return content_id
